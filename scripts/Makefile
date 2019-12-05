CXXFLAGS=-DRPI

all: outlet
all: switch

outlet: rc-switch/RCSwitch.o outlet.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi

switch: NewRemoteTransmitter.o switch.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi
