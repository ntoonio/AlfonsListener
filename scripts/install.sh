#!/bin/bash

# Clear old
rm -rf rc-switch WiringPi *.o switch outlet

if [ "$1" = "remove" ]
then
	echo "Only removing old files"
	exit
fi

# wiringPi
git clone https://github.com/WiringPi/WiringPi
WiringPi/build

# rc-switch
git clone https://github.com/sui77/rc-switch

make
