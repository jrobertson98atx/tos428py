#! /bin/bash

set -u
set -e

# https://retropie.org.uk/docs/Runcommand/

# All the error messages from these scripts will be logged in
# /dev/shm/runcommand.log. If you want to log something to this file you
# have to redirect the output to the standard error. 

exec 1>&2

#   $1 - the system (eg: atari2600, nes, snes, megadrive, fba, etc).
#   $2 - the emulator (eg: lr-stella, lr-fceumm, lr-picodrive, pifba, etc).
#   $3 - the full path to the rom file.
#   $4 - the full command line used to launch the emulator.

if [ $# != 4 ]; then
    echo "ERROR: $0 - Expected 4 arguments; got $#"
    exit 1
fi

system="$1"
emulator="$2"
romfile="$3"
cmdline="$4"

exec /home/pi/tos428py/tos428.py setuprom "$romfile"

exit $?
