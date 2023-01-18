#!/usr/bin/perl

my %mssHash;
my @msLabelArray;



# standardisation
my $numOfMss=0;

my $filename = './test_data/besoin-all.txt';

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

#pprint %mssHash;
#print %mssHash->['V'];
print %mssHash{'U         '};
#print "$_\n" for keys %mssHash;
#my @items = %mssHash{A};

