#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: $0 path-to-gimp-plugins"
	exit 1
fi
if [ -d "$1" ]; then
	stow -t "$1" src/
else
	echo "$1 doesn't seem to be a directory"
	exit 1
fi
