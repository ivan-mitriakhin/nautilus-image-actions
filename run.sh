#!/bin/bash

global_prefix=/usr/share/
local_prefix=~/.local/share/

EXTENSION_DIR=/nautilus-python/extensions

if test -d $global_prefix$EXTENSION_DIR; then
    sudo cp ./src/image_actions.py $global_prefix$EXTENSION_DIR
else
    sudo cp ./src/image_actions.py $local_prefix$EXTENSION_DIR
fi

nautilus -q