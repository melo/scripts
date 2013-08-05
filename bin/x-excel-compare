#!/usr/bin/env perl
#
# Compare two excel sheets
#

use strict;
use warnings;
use Spreadsheet::XLSX;
use Getopt::Long;

my $is_diff = 0;
my %opts;
GetOptions(\%opts, "file1=s", "key1=i", "file2=s", "key2=i", "has-headers", "ignore-whitespace|b", "debug", "help",)
  or usage('Bad options');
usage('Help wanted') if $opts{help};


for ($opts{file1}, $opts{file2}) {
  usage("Cannot read file '$_'") unless -r $_;
}


my $excel1 = Spreadsheet::XLSX->new($opts{file1});
my ($sheet1) = @{ $excel1->{Worksheet} };

my $excel2 = Spreadsheet::XLSX->new($opts{file2});
my ($sheet2) = @{ $excel2->{Worksheet} };

my $row = $sheet1->{MinRow};
if ($opts{'has-headers'}) {
  my $equal = compare_row($row, $sheet1, $sheet2);
  exit(5) if $is_diff;
  $row++;
}

my $max = $sheet1->{MaxRow};
if ($max != $sheet2->{MaxRow}) {
  diff($row, undef, "different row counts - $max and $sheet2->{MaxRow}");
  $max = $sheet2->{MaxRow} if $max > $sheet2->{MaxRow};
}
 
while ($row < $max) {
  compare_row($row, $sheet1, $sheet2);
  $row++;
}

debug("Found $is_diff differences");

exit($is_diff ? 5 : 0);


sub compare_row {
  my ($row, $sheet1, $sheet2) = @_;

  my @r1 = extract_row_from($row, $sheet1);
  my @r2 = extract_row_from($row, $sheet2);

  debug("* Comparing row '$row'");
  my $l1 = @r1;
  my $l2 = @r2;
  if ($l1 != $l2) {
    diff($row, undef, "different lengths - $l1 and $l2");
    $l1 = $l2 if $l2 < $l1;
  }

  my $col = $sheet1->{MinCol};
  while ($col < $l1) {
    my ($v1, $v2) = ($r1[$col], $r2[$col]);

    $v1 = defined $v1 ? "'$v1'" : '<undef>';
    $v2 = defined $v2 ? "'$v2'" : '<undef>';

    if ($v1 eq $v2) {
      debug("... ", _prefix($row, $col), ": equal $v1 == $v2");
    }
    else {
      diff($row, $col, "$v1 <=> $v2");
    }

    $col++;
  }
}

sub extract_row_from {
  my ($row, $sheet) = @_;

  my @data;
  for (my $col = $sheet->{MinCol}; $col <= $sheet->{MaxCol}; $col++) {
    my $v = $sheet->{Cells}[$row][$col];
    if ($v and defined $v->{Val}) {
      push @data, $v->{Val};
      if ($opts{'ignore-whitespace'}) {
        $data[-1] =~ s/^\s+|\s+$//;
        $data[-1] =~ s/\s+/ /g;
      }
    }
    else {
      push @data, undef;
    }
  }

  return @data;
}

sub diff {
  my ($r, $c, @rest) = @_;
  my $prefix = _prefix($r, $c) . ': ';

  print $prefix, @rest, "\n";
  debug("... ", $prefix, @rest);

  $is_diff++;
}

sub debug {
  return unless $opts{debug};
  print STDERR @_, "\n";
}

sub _prefix {
  my ($r, $c) = @_;

  my $prefix = "r$r";
  $prefix .= ":c$c" if defined $c;

  return $prefix;
}

sub usage {
  print STDERR "FATAL: ", @_, "\n" if @_;
  print STDERR "Usage: x-excel-compare --file1=FILE1 --file2=FILE2 [--has-headers] [--ignore-whitespace] [--help]";
  exit(1);
}
