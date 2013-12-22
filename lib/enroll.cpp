#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "OEM.h"

int main (int argc,char **argv)
{
		{
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
			
			if(oem_enroll_start(-1)<0)
			{
				return -1;
			}
			if(gwLastAck==NACK_INFO)
			{
				return -1;
			}

			oem_cmos_led (true);
			for(int i=1;i<4;i++)
			{
				int count=0;
				while(count<50)
				{
					if(oem_capture(1)<0)
						return -1;
					else if(gwLastAck==ACK_OK)
						break;
					usleep(5*10000);
					count++;
				}
				if(count==50)
					return -1;
				
				oem_enroll_nth(-1,i);
				if(gwLastAck==NACK_INFO)
				{
					//printf("enroll fail");
					oem_cmos_led (false);
					return -1;
				}
				count=0;
				//printf("take off\n");
				if(i<3)
				while(1)
				{
					oem_is_press_finger();
					if(gwLastAckParam==0)
						break;
					usleep(5*100000);
					count++;
					if(count>50)
					{
						oem_cmos_led (false);
						return -1;
					}
				}
			}

			oem_cmos_led (false);

			FILE *f;
			f=fopen("tmpfp","wb");
			fwrite(gbyTemplate,FP_TEMPLATE_SIZE,1,f);
			fclose(f);

			oem_close();

			printf("1,tmpfp");
		}

	return 0;
}


