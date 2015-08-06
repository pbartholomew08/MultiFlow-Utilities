#!/bin/sh

wifi_network=`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/' | cut -d ":" -f 2`

if [[ "$wifi_network" == "" ]] 
then
	echo "$(echo '\033[31m'No connection'\033[0m')"
	exit 1
elif [[ "$wifi_network" == " Imperial-WPA" ]]
then
	ssh YOUR_USERNAME@login.cx1.hpc.ic.ac.uk /opt/pbs/default/bin/qstat -a | process_qstat.sh
	exit 0
else
	ruby ./connect.rb
	STATUS=`scutil --nc status "YOUR_VPN_ID_NAME" | sed -n 1p`
	if [[ "$STATUS" == "Connected" ]] 
	then
		ISCONNECTED=1
	else
		ISCONNECTED=0
	fi
	
	TIME=0;
	while [ $ISCONNECTED -eq 0 ]; do
		sleep 0.1
		STATUS=`scutil --nc status "YOUR_VPN_ID_NAME" | sed -n 1p`
		if [[ "$STATUS" == "Connected" ]] 
		then
			ISCONNECTED=1
		else
			ISCONNECTED=0
		fi
		let TIME=TIME+1
		if [ $TIME -eq 100 ]
		then
			ISCONNECTED=2
		fi
	done
	
	if [ $ISCONNECTED -eq 1 ]
	then
	  ssh YOUR_USERNAME@login.cx1.hpc.ic.ac.uk /opt/pbs/default/bin/qstat -a | process_qstat.sh
		ruby ./disconnect.rb
		exit 0
	else
		echo "$(echo '\033[31m'There is a connection but the Imperial VPN is unaccessible'\033[0m')"
		exit 1
	fi
fi

