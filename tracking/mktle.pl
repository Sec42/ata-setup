#!/usr/bin/perl
system("curl -O https://www.celestrak.com/NORAD/elements/iridium-NEXT.txt");

open(my $f,"<","iridium-NEXT.txt");

while(<$f>){
	($name=$_);
	chomp($name);
	$name=~s/\r//;
	$name=~s/ *$//;
	$name=~s/ /-/g;
	print "Writing $name\n";
	open(my $o,">",$name);
	#print $o $_;
	print $o scalar(<$f>);
	print $o scalar(<$f>);
	close($o);
};

