#!/usr/bin/perl

use strict;
use Encode;

binmode STDOUT, ":utf8";

$|=1;

my %w = ();
my @clseg = ();
my $segmodname = shift;

sub loadModel {
    my $modname = shift;
    my $c = shift;
    
    open FP, "$modname" or die "Cannot open model $modname\n";

    my $clstr = <FP>;
    @{$c} = split ' ', $clstr;
    shift @{$c};

    while(<FP>) {
	my $estr = decode('utf8', $_);
	my @arr = split ' ', $estr;
	my $fname = shift @arr;
	my $i = 0;
	foreach my $fw (@arr) {
	    if( $fw != 0 ) {
		$w{$fname}{$i} = $fw;
	    }
	    $i++;
	}
    }
    
    close FP;
}

sub classify {
    my $feats = shift;
    my $c = shift;
    
    my @res = ();
    my @ff = @{$feats};
    unshift @ff, "**BIAS**";

    foreach my $f (@ff) {
        if (exists $w{$f}) {
            for (my $i = 0; $i < @{$c}; $i++) {
		if( exists $w{$f}{$i} ) {
		    $res[$i] += $w{$f}{$i};
		}
            }
        }
    }

    my @fres = ();
    for (my $i = 0; $i < @res; $i++) {
        $fres[$i] = {
            cname => $c->[$i],
            weight => $res[$i],
        };
    }

    @fres = sort {$b->{weight} <=> $a->{weight}} @fres;
    my $bestlabel = $fres[0]->{cname};
    if ($bestlabel eq "") {
        $bestlabel = "NONE";
    }
    
    return $bestlabel;
}

&loadModel( $segmodname, \@clseg );
 
while( <> ) {
    s/[\n\r]*//g;
    s/  +/ /g;

    my $estr = decode('utf8', $_);
    my @a1 = split /(?<=.)/, $estr;

    push @a1, " ";

    my @w = ();

    my $pw = "BOS";
    my $pw2 = "BOS";
    my $currw = "";
    unshift @a1, "BOS";
    push @a1, "EOS";
 
    for( my $i = 1; $i < @a1 - 1; $i++ ) {
	my @f = ();
	$currw .= $a1[$i];

        push @f, "currchar:$a1[$i]";
        push @f, "nextchar:$a1[$i+1]"; 
	push @f, "ccnc:$a1[$i]:$a1[$i+1]";
        push @f, "prevchar:$a1[$i-1]"; 
	push @f, "ccpc:$a1[$i]:$a1[$i-1]";
        push @f, "w:$currw";
        push @f, "prevw:$pw";
	push @f, "prevw2:$pw2";
	push @f, "w:pw:$currw:$pw";
	push @f, "w:pw:pw2:$currw:$pw:$pw2";

	my $lab = &classify( \@f, \@clseg );
	
	if( $lab eq "BRK" ) {
	    push @w, $currw;
	    $pw2 = $pw;
	    $pw = $currw;
	    $currw = "";
	}
    }
    
    push @w, $currw;
    $pw2 = $pw;
    $pw = $currw;
    $currw = "";

    my $str = join " ", @w;
    print "$str\n";
}

