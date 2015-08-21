#!/bin/sh

CALLED_BEFORE=`tail -2 ~/.bash_history | awk '{if (NR==1) {if ($1=="qs") {print 1} else {print 0}}}'`

if [ $CALLED_BEFORE -eq 0 ]; then
	qstat -a | ~/src/pegasus_script/process_qstat.sh
else
	LINES=`tail -1 ~/.qslines`
	for (( i=1; i <= $LINES; i++ ))
	do
		tput cuu1
	done
	tput ed	
	qstat -a | ~/src/pegasus_script/process_qstat.sh
fi

exit 0
