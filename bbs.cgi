#!/usr/bin/perl

use strict;
use warnings;

my $CHARSET   = "Shift_JIS";
my $DATAFILE  = "./board.dat";
my $PAGEVIEW  = 5;

my %FORM = ();

loadFormData();

#�L���f�[�^�̓ǂݍ���

open my $FILE, "<", "$DATAFILE" or printErrorPage("�L���t�@�C�����J���܂���");

eval{ flock($FILE, 1) };

my @DATA = <$FILE>;

printPage();

exit;

#�L���y�[�W�o��
sub printPage
{
	my $begin = $FORM{'page'} * $PAGEVIEW;
	my $end = $begin + $PAGEVIEW;

	if($end > @DATA){
		$end = @DATA;
	}

	print<<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLKC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>�f����</title></head>
<body>
<h1>�f����</h1>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
���O:<input type="text" name="author" size="40"><br>
�d�q���[��:<input type="text" name="email" size="40"<br>
�薼:<input type="text" name="title" size="60"><br>
���e:<textarea cols="60" rows="5" name="text"></textarea><br>
<input type="hidden" name="mode" value="write">
<input type="submit" value="��������">
<input type="reset" value="���Z�b�g">
</form>
<hr>
END

	my($i,$nextpage,$nextlink);

	for($i = $begin;$i < $end; ++$i){
		my ($date,$title,$author,$email,$text) = split(/\t/,$DATA[$i]);
		print "<h2>$title</h2>\n";
		if($email){
			print "<strong>";
			print "<a href=\"mailto:$email\">$author</a>";
			print "</strong>";
		}
		else{
			print "<strong>$author</strong>";
		}
		print "[ $date ] ";
		print "<p>$text</p>";
		print "<hr>\n";
	}

	if($end < @DATA){
		$nextpage = $FORM{'page'} + 1;
		$nextlink = "$ENV{'SCRIPT_NAME'}?page=$nextpage";
		print "<p><a href=\"$nextlink\">NEXT PAGE</a></p>\n";
	}

	print <<END;
</body>
</html>
END
}

#�G���[�y�[�W�o��

sub printErrorPage
{
	print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>�f����</title></head>
<body><h1>�G���[</h1>$_[0]</p></body>
</html>
END
    exit;
}


#�t�H�[���f�[�^��荞��
sub loadFormData
{
	my ($query,$pair);

	if($ENV{'REQUEST_METHOD'} eq 'POST'){
		read(STDIN,$query,$ENV{'CONTENT_LENGTH'});
	}
	else{
		$query = $ENV{'QUERY_STRING'};
	}

	foreach $pair (split(/&/,$query)){
		my ($key,$value) = split(/=/,$pair);

		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9-a-fA-F])/chr(hex($1))/eg;

		$FORM{$key}= $value;
	}
}
