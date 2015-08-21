#!/bin/sh

wifi_network=`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/' | cut -d ":" -f 2`

if [[ "$wifi_network" == "" ]] 
then
	echo "$(echo '\033[31m'No connection'\033[0m')"
	exit 1
elif [[ "$wifi_network" == " Imperial-WPA" ]]
then
	ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Build Test" | awk 'BEGIN { }
	{ if (NR==2) {
	if ($0=="    build successful") {
		printf ("Build Test\t\t \033[32m%12s\033[0m\n", "Successful")} 
	else {
		printf ("Build Test\t\t \033[31m%12s\033[0m\n", "Failed")}
	}} END { }'
	ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Memory Leak Test" | awk 'BEGIN { }
	{ if (NR==2) {
	if ($0=="    build successful") {
		printf ("Memory Leak Test\t \033[32m%12s\033[0m\n", "Successful")} 
	else {
		printf ("Memory Leak Test\t \033[31m%12s\033[0m\n", "Failed")}
	}} END { }'
	ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Executable Test" | awk 'BEGIN { }
	{ if (NR==2) {
	if ($0=="    build successful") {
		printf ("Executable Test\t\t \033[32m%12s\033[0m\n", "Successful")} 
	else {
		printf ("Executable Test\t\t \033[31m%12s\033[0m\n", "Failed")}
	}} END { }'
	exit 0
else
	STATUS=`scutil --nc status "IC VPN" | sed -n 1p`
	if [[ "$STATUS" == "Connected" ]] 
	then
		VPN_already_connected=1
	else
		VPN_already_connected=0
	fi
	
	if [ $VPN_already_connected -eq 0 ]
	then
		/Users/fabien/Documents/Scripts/connect.sh | printf ""
	fi
	
	STATUS=`scutil --nc status "IC VPN" | sed -n 1p`
	if [[ "$STATUS" == "Connected" ]] 
	then
		ISCONNECTED=1
	else
		ISCONNECTED=0
	fi
	
	TIME=0;
	while [ $ISCONNECTED -eq 0 ]; do
		sleep 0.1
		STATUS=`scutil --nc status "IC VPN" | sed -n 1p`
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
		ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Build Test" | awk 'BEGIN { }
		{ if (NR==2) {
		if ($0=="    build successful") {
			printf ("Build Test\t\t \033[32m%12s\033[0m\n", "Successful")} 
		else {
			printf ("Build Test\t\t \033[31m%12s\033[0m\n", "Failed")}
		}} END { }'
		ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Memory Leak Test" | awk 'BEGIN { }
		{ if (NR==2) {
		if ($0=="    build successful") {
			printf ("Memory Leak Test\t \033[32m%12s\033[0m\n", "Successful")} 
		else {
			printf ("Memory Leak Test\t \033[31m%12s\033[0m\n", "Failed")}
		}} END { }'
		ssh fabien@solids8.me.ic.ac.uk curl -s "solidsserv:8010/waterfall" | grep -A1 "Executable Test" | awk 'BEGIN { }
		{ if (NR==2) {
		if ($0=="    build successful") {
			printf ("Executable Test\t\t \033[32m%12s\033[0m\n", "Successful")} 
		else {
			printf ("Executable Test\t\t \033[31m%12s\033[0m\n", "Failed")}
		}} END { }'
		if [ $VPN_already_connected -eq 0 ]
		then
			/Users/fabien/Documents/Scripts/disconnect.sh | printf ""
		fi
		exit 0
	else
		echo "$(echo '\033[31m'There is a connection but the Imperial VPN is unaccessible'\033[0m')"
		exit 1
	fi
fi

