#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "OEM.h"

int main (int argc,char **argv)
{
		{
			char filename[18],str[50];
			strcpy(filename,argv[1]);
			filename[13]='.';
			filename[14]='t';
			filename[15]='x';
			filename[16]='t';
			filename[17]='\0';
			FILE *f;
			strcpy(str,"db/");
			strcat(str,filename);
			f=fopen(str,"rb");
			fseek(f,13,SEEK_SET);
			fread(gbyTemplate,498,1,f);
			fclose(f);

			if( !comm_open_usb() ){
				//m_strResult = _T("Device is not connected to usb port.");
				perror ("Device is not connected to usb port.");
				return 0;
			}
			if(oem_open() < 0)
			{
				//m_strResult = _T("Cannot connect to the device !");
				perror ("Cannot connect to the device !");
				return 0;
			}
			
			oem_delete(1);
			int o=oem_add_template(1);
			oem_cmos_led (true);
			int count=0,x;
			oem_is_press_finger();
			while(gwLastAckParam!=0)
			{
				oem_is_press_finger();
				usleep(5*100000);
				count++;
				if(count>20)
				{
					oem_cmos_led(false);
					printf("to");
					return -1;
				}
			}
			oem_capture(0);
			oem_verify(1);
			char r='f';
			if(gwLastAck!=NACK_INFO)
				r='p';
			else
				r='f';
			oem_cmos_led (false);
			oem_close();

			printf("%c",r);
		}

	return 0;
}


