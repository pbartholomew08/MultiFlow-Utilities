class Functions

def turn_on
  `/usr/bin/env osascript <<-EOF
      tell application "System Events"
        tell current location of network preferences
            set VPN to service "YOUR_IMPERIAL_VPN_ID"
            if exists VPN then connect VPN
      end tell
    end tell
  EOF` 
end
self

end.new.turn_on
