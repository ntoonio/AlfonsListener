#include "NewRemoteTransmitter.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])  {   
    int unitCode = atoi(argv[1]);
    int command  = atoi(argv[2]);
    if(unitCode > 16 || unitCode < 1 || command > 1 || command < 0)
    	return 1;
 
    if (wiringPiSetup() == -1)
    	 return 1;
	
	NewRemoteTransmitter transmitter(67234623, 0, 263, 1);
    transmitter.sendUnit(unitCode, command);
    
    printf("Done!\n");
	return 0;
}
