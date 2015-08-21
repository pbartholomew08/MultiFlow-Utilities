#!/bin/sh

/opt/local/bin/sshfs -o IdentityFile=/Users/fabien/.ssh/id_rsa -p 22 fabien@solids8.me.ic.ac.uk:/mnt/SHARE/ /Users/fabien/SHARE -oauto_cache,reconnect,defer_permissions,negative_vncache,allow_other,volname=solids8/mnt/SHARE