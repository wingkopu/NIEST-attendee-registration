#! /usr/bin/env python
#-*-coding: utf-8 -*-
import sys
from smartcard.scard import *
import smartcard.util
import cStringIO as StringIO
import urllib
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import *

class thaiNationIDCard(object):
    def __init__(self):

        cardtype = AnyCardType()
        self.resetCmd = [0x0, 0xA4, 0x4, 0x0, 0x8, 0xA0, 0x0, 0x0, 0x0, 0x54, 0x48, 0x0, 0x1]
        self.resetCmd1 = [0x0, 0xC0, 0x0, 0x0, 0xA]

        self.citizenCmd = [0x80, 0xB0, 0x0, 0x4, 0x2, 0x0, 0xD]
        self.citizenResponse = [0x0, 0xC0, 0x0, 0x0, 0xD]

        try:
            # request card insertion
            cardrequest = CardRequest(timeout=5, cardType=cardtype)
            self.cardservice = cardrequest.waitforcard()
            # attach the console tracer
            # observer = ConsoleCardConnectionObserver()
            # self.cardservice.connection.addObserver(observer)

            # connect to the card and perform a few transmits
            self.cardservice.connection.connect()
        except CardRequestTimeoutException:
            print 'time-out: no card inserted during last 5s'

        except:
            import sys
            print sys.exc_info()[1]

    def hexToThaiDecoder(self,listHex):
        
        hex  = ['','20','21','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F','40','41','42','43','44','45','46','47','48','49','4A','4B','4C','4D','4E','4F','50','51','52','53','54','55','56','57','58','59','5A','5B','5C','5D','5E','5F','60','61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74','75','76','77','78','79','7A','7B','7C','7D','7E','80','91','92','93','94','95','96','97','A0','A1','A2','A3','A4','A5','A6','A7','A8','A9','AA','AB','AC','AD','AE','AF','B0','B1','B2','B3','B4','B5','B6','B7','B8','B9','BA','BB','BC','BD','BE','BF','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','CA','CB','CC','CD','CE','CF','D0','D1','D2','D3','D4','D5','D6','D7','D8','D9','DA','DF','E0','E1','E2','E3','E4','E5','E6','E7','E8','E9','EA','EB','EC','ED','EE','EF','F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','FA','FB']
        thai = ['',' ','!','"',' ','$','%','&','\\','(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[','',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','{','|','}','~','','\'','\'','"','"','','-','_',' ','ก','ข','ฃ','ค','ฅ','ฆ','ง','จ','ฉ','ช','ซ','ฌ','ญ','ฎ','ฏ','ฐ','ฑ','ฒ','ณ','ด','ต','ถ','ท','ธ','น','บ','ป','ผ','ฝ','พ','ฟ','ภ','ม','ย','ร','ฤ','ล','ฦ','ว','ศ','ษ','ส','ห','ฬ','อ','ฮ','ฯ','ะ','ั','า','ำ','ิ','ี','ึ','ื','ุ','ู','ฺ','฿','เ','แ','โ','ใ','ไ','ๅ','ๆ','็','่','้','๊','๋','์','ํ','','๏','๐','๑','๒','๓','๔','๕','๖','๗','๘','๙','๚','๛']

        result = ''
        for x in listHex:
            result = result + thai[hex.index(x)]
        return result

    def getCitizenID(self):
        self.cardservice.connection.transmit(self.resetCmd)
        self.cardservice.connection.transmit(self.resetCmd1)

        response, sw1, sw2 = self.cardservice.connection.transmit(self.citizenCmd)
        response, sw1, sw2 = self.cardservice.connection.transmit(self.citizenResponse)
        hexString = toHexString(response,UPPERCASE).split(" ")
        return self.hexToThaiDecoder(hexString)

def main():
    reload(sys)
    try :
        sys.setdefaultencoding("utf-8")
        # print sys.getdefaultencoding()
        scard = thaiNationIDCard()
        citizenID = scard.getCitizenID()
        print citizenID
    except:
        print "error"

if __name__ == '__main__':
    main()
