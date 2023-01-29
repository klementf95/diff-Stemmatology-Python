#!/usr/bin/perl
use strict;

use lib "./Algorithm-Diff-1.201/lib";
use Algorithm::Diff qw(diff sdiff LCS traverse_sequences traverse_balanced);
use List::Util qw( min max );
use Time::HiRes;

my $start_time = Time::HiRes::gettimeofday();

# authorship: Dieter Bachmann (script), Philipp Roelli; rewritten by Eva Sediki.

# Debug level CHANGE
# 0 : only matrix
# 1 : .. and a list of pot. leitfehler (lf) and their score
# 2 : ..... and a list of pot. lf and the ms. the occur in
# 3 : ....... and a list of matches of pot. lf
my $debug=2;


my $cut=0; # threshold for globalLeit, currently not used
my $weight=20; # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

my $scoremax=1;
my %ur;
my %score;
my %mssHash;
my @msLabelArray;



# standardisation
my $numOfMss=0;

# my $filename = './test_data/besoin-all.txt';

# open(FH, '<', $filename) or die $!;

my $in;

while (my $in=<>)
{      
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


wlist();
# remove to get a fast result without calculating the lff

##########

print scalar @msLabelArray; # print length of array
print "\n".$msLabelArray[0]."\n";

foreach my $msIndex (1 .. $#msLabelArray)
{
    print $msLabelArray[$msIndex];
    foreach my $otherMsIndex (0 .. $msIndex-1)
    {
        my @wordArrayMs1 = split(' ',$mssHash{$msLabelArray[$msIndex]}); # split content of this ms into words
        my @wordArrayMs2 = split(' ',$mssHash{$msLabelArray[$otherMsIndex]});# split content of the other ms into words
 

        #diff
        my $el=dodiff(\@wordArrayMs1, \@wordArrayMs2);
        print " ".$el." ";
        #$matrix->assign($msIndex+1,$otherMsIndex+1,$el); 
        #$matrix->assign($otherMsIndex+1,$msIndex+1,$el); 
  
    }
    print "\n";
}



##################################################################

sub dodiff
{
    # Copy the two arrays passed to this subroutine into the variables wordArrMs1 and wordArrMs2
    my ($a1, $a2) = @_;
    my @wordArrMs1=@$a1;
    my @wordArrMs2=@$a2;

    # diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
    # and returns a 2-dim array of differences (hunks with sequences); 
    # each difference is a list of 3 elements (-/+, position of the change, string), e.g.:
    # [ 
    #   [ 
    #      [ '-', 0, 'a' ] 
    #   ],
    #   [ 
    #      [ '-', 8, 'n' ], 
    #      [ '+', 9, 'p' ]
    #   ]
    # ]

    # Create the 2-dim array of differences between the two arrays
    my @diffArray = diff( \@wordArrMs1, \@wordArrMs2 );

    my $dist=0;

    foreach my $hunk (@diffArray)
    {
        my @sequenceArray=@$hunk; 
        my $distInHunk=0;
        foreach my $sequence (@sequenceArray)
        {
            # assigning a score to the pot. leitfehler in wlist();
            my $word="@$sequence"; # Concatenate 3 elements of the list
            # Remove +/- at the beginning and the digits (\d) of the position; leave only the char string
            $word=~s/^. \d+ (.+)/$1/; # $1 contains the first match: (.+)

            #handpicked lf
            #if($word=~/(definitio|tumore|cognoscere|proiciunt|afixia|introrsum|irruit|uisceribus|retentione|aperiant|molitam|catarticum|efficitur|sursum)/){$distInHunk+=$weight} # handpicked lf

            #if($word=~/€/){$distInHunk=-2} # €-wildcard matches anything
            
            # calibration to $weight.
            if($score{$word} && $scoremax*$weight != 0)
            {
                $distInHunk+= $score{$word}/$scoremax*$weight;
            }

            $distInHunk++;
        }

        $dist+=$distInHunk;
    }
    #$dist=$#diffArray+1;
    return int($dist+0.5);
}


# sub outdiff
# {
#     my $a="Zz";
#     my $b="Br";

#     #print $mssHash{$a}."\n";
#     #print $mssHash{$b}."\n";

#     my @arr1 = split('',$mssHash{$a});
#     my @arr2 = split('',$mssHash{$b});

#     my @diffArray =  diff( \@arr1, \@arr2 );

#     foreach my $i (@diffArray)
#     {
#         print "(".@$i."): ";
#         foreach my $j (@$i)
#         {
#             foreach my $k (@$j)
#             {
#                 print $k.",";
#             }
#         }
#         print "\n";
#     }
# }

sub wlist
{
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
 
    # leitfehler output with relevance for stemma
    if($debug==2)
    {
        open LOG2, ">log2";
        foreach my $word (keys %globalLeit)
        {
            if ($globalLeit{$word} > $cut) # Show only leitfehler word, if its global leitfehler counter is higher than cut
            {
                print LOG2 $word." (".$globalLeit{$word}.") : ";
                foreach my $msIndex (1 .. $#msLabelArray)
                {
                    my $currMsLabel = $msLabelArray[$msIndex];

                    if($mssWordCountHash{$currMsLabel}{$word})
                    {
                        $currMsLabel=~/^[^ ]{1,4}/; # match the first 4 chars of currMsLabel
                        print LOG2 $&.":".$mssWordCountHash{$currMsLabel}{$word}." "; # $&: last successful match; here: ms label without trailing blanks
                    }
                } 
                print LOG2 "\n";
            }
        } 
    }
    close LOG2;

# combination of any two potential lf (word and otherWord) and determining how many combination get only three out of four combinations 
# and weighting them by the square of the smallest non-zero entry.
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

# %ur counts and weights cases with only 3 combinations; %scoremax is its maximum

# ADDED calculate counter: number of occurences of word 
    foreach my $word (keys %globalLeit)
    {
        my $counter=0;

        # Iterate over all mss and 
        # count the number of mss that contain word
        foreach my $msIndex (1 .. $#msLabelArray)
        {
            my $currMsLabel = $msLabelArray[$msIndex];

            if($mssWordCountHash{$currMsLabel}{$word}) # if not 0
            {
                $counter++;
            }
        }
		if($counter > $numOfMss/2)
        {
            $counter=$numOfMss-$counter;
        }

        if($globalLeit{$word}*$counter) # if (globalLeit counter for this word * counter) not 0
        {
            $score{$word}=$ur{$word}/$counter;
        }
        else
		{
		    $score{$word}=$ur{$word};
		}
    }
# calculate scoremax   
        foreach my $word (keys %ur)
    {
        $scoremax = ($scoremax < $score{$word} ? $score{$word} : $scoremax);
    }
# print %ur if debug=1
    #logfile
    if($debug>0)
    {
        open LOG, ">log";
        my $k=0;
        foreach $k (sort  {$score{$b}<=>$score{$a}}  keys %score)
        {
            if ($ur{$k}>0&&$score{$k}>$scoremax/100)
            {
                print LOG "$k  --  " . int($score{$k}) . " - $ur{$k} " . int($score{$k}/$scoremax*100) . "% \n";
            }
        } 
        close LOG;
    }

} # sub wlist()

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
    if($debug==1)
    {
        if ($t0 ne 1 && $t1 ne 1 && $t2 ne 1 && $t3 ne 1)
        {
            print "$word/$otherWord ".$t0." ".$t1." ".$t2." ".$t3." \n";
        }
    }   
}



#Neue Idee fuer LF:
#- vierer als Grundlage
#- entferne alle mit 1
#- gebe jedem Wort score des min. Wertes unter den vier (ohne 0)
#- summiere fuer jedes Wort den Minimalwert (hoch 2)
#- setze den Maxwert dieser = $weight  

my $stop_time = Time::HiRes::gettimeofday();
printf("Executed the perl script in %.4f\n", $stop_time - $start_time);