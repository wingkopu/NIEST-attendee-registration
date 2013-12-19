c++ -Wall -fPIC -c sb_protocol_oem.cpp CommBase.cpp OEM.cpp
c++ -shared -Wl,-soname,libfp.so -o libfp.so sb_protocol_oem.o CommBase.o OEM.o -lrt
export LD_LIBRARY_PATH=.
