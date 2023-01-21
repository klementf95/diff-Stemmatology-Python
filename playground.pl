#!/usr/bin/perl

use Algorithm::Diff qw(diff sdiff LCS traverse_sequences traverse_balanced);
use Data::Dumper;
use List::Util qw( min max );

my %mssHash;
my @msLabelArray;



# standardisation
my $numOfMss=0;
my $cut=0;


my $filename = './test_data/besoin-all.txt';

open(FH, '<', $filename) or die $!;

my $in;
my %ur;


while (<FH>)
{      
    $in = $_;    
    chop $in; # Chop off the last char/strip string

    $in=~s/[\,!\?"]//g; # remove punctuation
    # $in=~s/\./ /g; # remove . ?
    $in=~s/\s[^\s]*\*[^\s]*/ €/g; # convert word with a *-wildcard to €
    $in=~s/\s+$//;
    
    # label manuscripts (3 chars), or n chars make (n-1) dots in next line
    if ($in=~/^(\w..)[\w\s]{7}(.+)$/)
    {
        $mssHash{"$1       "}=$2;  #hash of all mss.
        $msLabelArray[$numOfMss]="$1       ";  #all mss. label, n: index

        $mssHash{$msLabelArray[$numOfMss]}=~s/\([^\)]+\)//g; # remove  ()
        $mssHash{$msLabelArray[$numOfMss]}=~s/\[[^\]]+\]//g; # remove  []
        
        $numOfMss++;
    }

}

##################################################################



#sub wlist
#{
    $cut=$cut*$numOfMss*$numOfMss/2500; 

    # Hash map that contains a hash for each ms; the keys of the inner hash map are words, 
    # the value of each word is the number of occurrences of the word in the ms
    my %mssWordCountHash=();  

    # Hash map over all words in the mss; the key of the hash map are words, 
    # the value of each word is the number of occurrences of the word over all mss
    my %globalWordCountHash=();

    for my $msIndex (keys %mssHash)
    {
        my $msContent=$mssHash{$msIndex};
        $msContent=~s/[\s\|]+/ /g;
        while ($msContent=~s/^\s*([^\s]+)//) # while a word can be found in $msContent
        {  
            # $1: the word found
            # increment counter for the word found in the ms specific word hash map and in the global word hash map
            $mssWordCountHash{$msIndex}{$1}++;
            $globalWordCountHash{$1}++;
             
        }
    }

#######################hier wird weitergeharzt

    # finding candidates for leitfehler

    # Matrix of mss that contains a hash map; the keys of the hash map are words
    # and the value is a bool: 1=is a leitfehler candidate, 0=is not a leitfehler candidate
    my @leit;

    # Hash map over all words in the mss; the keys of the hash map are words, 
    # and the value is a counter: how often the word is a leitfehler candidate over all mss
    my %globalLeit; 

    foreach my $msIndex (1 .. $#msLabelArray)
    {
        my $currMsLabel = $msLabelArray[$msIndex];

        foreach my $otherMsIndex (0 .. $msIndex-1)
        {
            my $otherMsLabel = $msLabelArray[$otherMsIndex];

            for my $word (keys %globalWordCountHash) 
            {
                if ($word=~/.../  #only words with at least 3 characters are considered
                    && abs($mssWordCountHash{$currMsLabel}{$word} - $mssWordCountHash{$otherMsLabel}{$word}) >0 
                    && $mssWordCountHash{$currMsLabel}{$word}+$mssWordCountHash{$otherMsLabel}{$word} <2)
                {
                    $leit[$msIndex][$otherMsIndex]{$word}=1;  # leitfehler-candidate 1 iff yes between 2 mss.
                    $globalLeit{$word}++; # leitfehler counter total for each word
            
                    #print "$currMsLabel $otherMsLabel: $word ".$mssWordCountHash{$currMsLabel}{$word}."/".$mssWordCountHash{$otherMsLabel}{$word}."\n"
                }
            }
        }
    }

#my @tab = (0,0,0,0);
foreach my $word (keys %globalLeit)
{
    if ($globalLeit{$word} > $cut) # Consider only leitfehler, if its global leitfehler counter is heigher than cut
    {
        foreach my $otherWord (keys %globalLeit)
        {
            if ($globalLeit{$otherWord} > $cut &&  # Consider only leitfehler, if its global leitfehler counter is heigher than cut
                $word lt $otherWord) # word less than otherWord
            {
                my @tab=(0,0,0,0);

                # Iterate over all mss and 
                # count the "relations" between the counter of word and otherWord in each ms
                foreach my $msIndex (1 .. $#msLabelArray)
                {
                    my $currMsLabel = $msLabelArray[$msIndex];

                    # Both, word and otherWord are in the current ms
                    if($mssWordCountHash{$currMsLabel}{$word} && $mssWordCountHash{$currMsLabel}{$otherWord})
                    {
                        $tab[0]++; 
                    }
                    # Only word is in the the current ms
                    elsif($mssWordCountHash{$currMsLabel}{$word} && !$mssWordCountHash{$currMsLabel}{$otherWord})
                    {
                        $tab[1]++; 
                    }
                    # Only otherWord is in the the current ms
                    elsif(!$mssWordCountHash{$currMsLabel}{$word} && $mssWordCountHash{$currMsLabel}{$otherWord})
                    {
                        $tab[2]++; 
                    }
                    # Neither word nor otherWord are in the the current ms
                    else
                    {
                        $tab[3]++; 
                    }
                }

# Both words occur together in no ms
                    if ($tab[0]==0 && $tab[1]>0 && $tab[2]>0 && $tab[3]>0)
                    {
                        if ($debug)
                        {
                            vierer($tab[1],$tab[2],$tab[3], @tab, $word, $otherWord);
                        }
                        my $r = rating($tab[1],$tab[2],$tab[3], $word, $otherWord);
                        my $s = ratings($tab[1],$tab[2],$tab[3], $word, $otherWord);
                        if ($r>1)
                        {
                            $ur{$word} = $ur{$word}+($r-1)**2*$s;
                            $ur{$otherWord} = $ur{$otherWord}+($r-1)**2*$s;
                        }
                    }
                    # Absence of word and presence of otherWord in no ms
                    elsif ($tab[1]==0 && $tab[0]>0 && $tab[2]>0 && $tab[3]>0)
                    {
                        if ($debug)
                        {
                            vierer($tab[0],$tab[2],$tab[3], @tab, $word,  $otherWord);
                        }
                        my $r = rating($tab[0],$tab[2],$tab[3], $word, $otherWord);
                        my $s = ratings($tab[0],$tab[2],$tab[3], $word, $otherWord);
                        if ($r>1)
                        {
                            $ur{$word} = $ur{$word}+($r-1)**2*$s;
                            $ur{$otherWord} = $ur{$otherWord}+($r-1)**2*$s;
                        }
                    }
                    # Presence of word and absence of otherWord in no ms
                    elsif ($tab[2]==0 && $tab[0]>0 && $tab[1]>0 && $tab[3]>0)
                    {
                        if ($debug)
                        {
                            vierer($tab[0],$tab[1],$tab[3], @tab, $word,  $otherWord);
                        }
                        my $r = rating($tab[0],$tab[1],$tab[3], $word, $otherWord);
                        my $s = ratings($tab[0],$tab[1],$tab[3], $word, $otherWord);
                        if ($r>1)
                        {
                            $ur{$word} = $ur{$word}+($r-1)**2*$s;
                            $ur{$otherWord} = $ur{$otherWord}+($r-1)**2*$s;
                        }
                    }
                    # Absence of word and otherWord in no ms
                    elsif ($tab[3]==0 && $tab[0]>0 && $tab[1]>0 && $tab[2]>0)
                    {
                        if ($debug)
                        {
                            vierer($tab[0],$tab[1],$tab[2], @tab, $word,  $otherWord);
                        }
                        my $r = rating($tab[0],$tab[1],$tab[2], $word, $otherWord);
                        my $s = ratings($tab[0],$tab[1],$tab[2], $word, $otherWord);
                        if ($r>1)
                        {
                            $ur{$word} = $ur{$word}+($r-1)**2*$s;
                            $ur{$otherWord} = $ur{$otherWord}+($r-1)**2*$s;
                        }
                    }
				} # if ($globalLeit{$otherWord} > $cut && $word lt $otherWord)
		    } # foreach my $otherWord (keys %globalLeit)
        } # if ($globalLeit{$word} > $cut)
    } # foreach my $word (keys %globalLeit)          



sub rating 
{
    my ($a1, $a2, $a3, $word, $otherWord) = @_;
    my @a = ($a1, $a2, $a3);
    my $r = min @a;
    
    return $r;
}
sub ratings 
{
    my ($a1, $a2, $a3, $word, $otherWord) = @_;
    my @a = ($a1, $a2, $a3);
    my $s = @msLabelArray-(max @a)-(min @a);
    
    return $s;
}

sub vierer 
{
    my ($a1, $a2, $a3, $t0, $t1, $t2, $t3, $word, $otherWord) = @_;
    if($debug==3)
    {
        if ($t0 ne 1 && $t1 ne 1 && $t2 ne 1 && $t3 ne 1)
        {
            print "$word/$otherWord ".$t0." ".$t1." ".$t2." ".$t3." \n";
        }
    }   
}

print Dumper(%ur);