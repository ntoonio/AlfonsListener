CXXFLAGS=-DRPI

all: outlet
all: switch

switch: rc-switch/RCSwitch.o switch.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi

outlet: NewRemoteTransmitter.o outlet.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi
