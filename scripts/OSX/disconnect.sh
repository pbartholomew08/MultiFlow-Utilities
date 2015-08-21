#!/usr/bin/osascript
tell application "System Events"
	tell current location of network preferences
		set VPN to service "IC VPN"
		if exists VPN then disconnect VPN
	end tell
end tell