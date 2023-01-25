#!/usr/bin/perl
use strict;

use lib "./Algorithm-Diff-1.201/lib";
use Algorithm::Diff qw(diff sdiff LCS traverse_sequences traverse_balanced);
use List::Util qw( min max );
use Data::Dumper;

# authorship: Dieter Bachmann (script), Philipp Roelli; rewritten by Eva Sediki.

# Debug level CHANGE
# 0 : only matrix
# 1 : .. and a list of pot. leitfehler (lf) and their score
# 2 : ..... and a list of pot. lf and the ms. the occur in
# 3 : ....... and a list of matches of pot. lf
my $debug=1;


my $cut=0; # threshold for globalLeit, currently not used
my $weight=20; # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

my $scoremax=1;
my %ur;
my %score;
my %mssHash;
my @msLabelArray;



# standardisation
my $numOfMss=0;

my $filename = './test_data/besoin-all_test.txt';

open(FH, '<', $filename) or die $!;

my $in;

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


#wlist();
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
         print Dumper(@sequenceArray) }}
        foreach my $sequence (@sequenceArray)
        { 
            # assigning a score to the pot. leitfehler in wlist();
           #my $word="@$sequence"; 
                #print Dumper($word)}
    # Concatenate 3 elements of the list
    #         # Remove +/- at the beginning and the digits (\d) of the position; leave only the char string
    #         $word=~s/^. \d+ (.+)/$1/; # $1 contains the first match: (.+)

    #         #handpicked lf
    #         #if($word=~/(definitio|tumore|cognoscere|proiciunt|afixia|introrsum|irruit|uisceribus|retentione|aperiant|molitam|catarticum|efficitur|sursum)/){$distInHunk+=$weight} # handpicked lf

    #         #if($word=~/€/){$distInHunk=-2} # €-wildcard matches anything
            
    #         # calibration to $weight.
    #         if($score{$word} && $scoremax*$weight != 0)
    #         {
    #             $distInHunk+= $score{$word}/$scoremax*$weight;
    #         }

    #         $distInHunk++;
    #     }

    #     $dist+=$distInHunk;
        #}
    # #$dist=$#diffArray+1;
    # return int($dist+0.5);
#}
