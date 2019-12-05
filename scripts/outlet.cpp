#include "rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	if (wiringPiSetup() == -1) {
		return 1;
	}

	int PIN = 0;

	if (argc == 1) {
		printf("Usage: %s protocol mode ...\n", argv[0]);
		printf("protocol A\n");
		printf("\t - group\t- 1-5\n");
		printf("\t - device\t- 6-10\n");

		printf("protocol B\n");
		printf("\t - address\t- 1-4\n");
		printf("\t - channel\t- 1-4\n");

		printf("protocol C\n");
		printf("\t - family\t- a-f\n");
		printf("\t - group\t- 1-4\n");
		printf("\t - device\t- 1-4\n");

		printf("protocol D\n");
		printf("\t - group\t- a-f\n");
		printf("\t - device\t- 1-3\n");
		printf("\nmode\t- 0-1\n");
		return -1;
	}
		
	int type = int(argv[1][0]) - int('A') + 1;
	bool mode = atoi(argv[2]) ? true : false;

	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN);

	if (type == 1) {
		char* group = argv[3];
		char* device = argv[4];
		
		if (mode) {
			mySwitch.switchOn(group, device);
		}
		else {
			mySwitch.switchOff(group, device);
		}
	}
	else if (type == 2) {
		int address = atoi(argv[3]);
		int channel = atoi(argv[4]);
		
		if (mode) {
			mySwitch.switchOn(address, channel);
		}
		else {
			mySwitch.switchOff(address, channel);
		}
	}
	else if (type == 3) {
		char family = argv[3][0];
		int group = atoi(argv[4]);
		int device = atoi(argv[5]);
		
		if (mode) {
			mySwitch.switchOn(family, group, device);
		}
		else {
			mySwitch.switchOff(family, group, device);
		}
	}
	else if (type == 4) {
		char group = argv[3][0];
		int device = atoi(argv[4]);
		
		if (mode) {
			mySwitch.switchOn(group, device);
		}
		else {
			mySwitch.switchOff(group, device);
		}
	}
	
	return 0;
}