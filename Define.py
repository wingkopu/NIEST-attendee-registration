class DataType:
    DEVINFO=24
    TEMPLATESIZE=498
    ACK=chr(0x30)+chr(0)
    NACK=chr(0x31)+chr(0)
    RAWIMAGESIZE=19600

class DevInfoDescription:
    FirmwareVersion=""
    IsoAreaMaxSize=0
    DeviceSerialNumber=""

    def __init__(self,msg):
        self.FirmwareVersion=msg[0:4]
        self.IsoAreaMaxSize=Convert.toInt(msg[4:8])
        self.DeviceSerialNumber=msg[8:24]

class Convert:
    @staticmethod
    def toInt(data):
        leng=len(data)
        result=0
        for i in range(leng):
            result=result+(ord(data[i])<<8*i)
        return result

    @staticmethod
    def toByte(data,size):
        result=""
        for i in range(size):
            result+=chr((data>>8*i)&0b11111111)
        return result

class NACKTABLE:
    NACK_DB_IS_FULL=chr(0x09)+chr(0x10)+chr(0)+chr(0)
    NACK_DB_IS_EMPTY=chr(0x0A)+chr(0x10)+chr(0)+chr(0)
    NACK_IS_ALREADY_USED=chr(0x05)+chr(0x10)+chr(0)+chr(0)
    NACK_INVALID_POS=chr(0x03)+chr(0x10)+chr(0)+chr(0)
