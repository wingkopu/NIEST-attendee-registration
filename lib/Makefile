c++ -Wall -fPIC -c sb_protocol_oem.cpp CommBase.cpp OEM.cpp
c++ -shared -Wl,-soname,fp.so -o libfp.so OEM.o CommBase.o sb_protocol_oem.o
