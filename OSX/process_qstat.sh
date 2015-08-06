#!/bin/sh

PROC=0
MEM=0

awk -v proc=$PROC 'BEGIN { }
{ if (NR==1) {
	print "    Name   |  Np |  Mem |    Time    "
	print "-----------|-----|------|------------" 
	procrun = 0
	memrun = 0
	procq = 0
 	memq = 0}
}
{ if (NR>5) {
	if ($11=="--") {
		printf ("\033[31m%11s\033[0m",substr($4,0,11)) }
	else {
		printf ("\033[32m%11s\033[0m",substr($4,0,11)) }
	printf ("| %4i| %5s| ", $7, $8) 
	if ($11=="--") {
		printf ("\033[31m%5s\033[0m\/%5s\n", $11, $9)
		procq+=$7
		memq+=substr($8, 0, length($8)-2) }
	else {
		printf ("%5s\/%5s\n", $11, $9)
		procrun+=$7
		memrun+=substr($8, 0, length($8)-2) }
}
}
END { 
	if (NR>1) {
		print "-----------|-----|------|------------" 
		printf ("    Running|%5i|%4igb|\n",procrun,memrun)
		printf ("   Queueing|%5i|%4igb|",procq,memq)}
	else
		print "No science occuring soz!"
}'
