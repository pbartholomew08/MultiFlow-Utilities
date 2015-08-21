#!/bin/bash

awk -v proc=$PROC 'BEGIN { }
{ if (NR==1) {
	print "     JobID     |    Name    |   Queue   |  Np  |  Mem  |    Time    "
	print "---------------|------------|-----------|------|-------|-------------" 
	procrun = 0
	memrun = 0
	procq = 0
 	memq = 0
	lines = 2}
}
{ if (NR>5) {

	if ($11=="--") {
		printf ("\033[31m%14s\033[0m |\033[31m%11s\033[0m ",substr($1,0,14),substr($4,0,11)) }
	else {
		printf ("\033[32m%14s\033[0m |\033[32m%11s\033[0m ",substr($1,0,14),substr($4,0,11)) }
	printf ("| %9s | %4i | %5s | ", substr($3,0,9), $7, $8) 
	if ($11=="--") {
		printf ("\033[31m%5s\033[0m/%5s\n", $11, $9)
		procq+=$7
		memq+=substr($8, 0, length($8)-2) }
	else {
		printf ("%5s/%5s\n", $11, $9)
		procrun+=$7
		memrun+=substr($8, 0, length($8)-2) }
	lines+=1
}
}
END { 
	if (NR>1) {
		print   "---------------|------------|-----------|------|-------|-------------" 
		printf ("                                Running |%5i |%4igb |\n",procrun,memrun)
		printf ("                               Queueing |%5i |%4igb |\n",procq,memq)
		lines+=4
		system("echo "lines" > ~/.qslines")}
	else      {
		print "No science occuring soz!"
		lines=2
		system("echo "lines" > ~/.qslines")}
}'

