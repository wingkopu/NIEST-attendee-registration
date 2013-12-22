/*
 * main.cpp
 *
 *  Created on: Dec 14, 2013
 *      Author: nagato
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "OEM.h"

double GetTickCount2(void)
{
  struct timespec now;
  if (clock_gettime(CLOCK_MONOTONIC, &now))
    return 0;
  return now.tv_sec * 1000.0 + now.tv_nsec / 1000000.0;

}

int Capturing(BOOL bBest/* = FALSE*/)
{
	BOOL m_bContinue = true;
	double st = GetTickCount2();
	while(m_bContinue && GetTickCount2() - st < 5000)
	{
		if(oem_capture(bBest) < 0)
		{
			//m_strResult = _T("Communication error!");
			return -1;
		}
		else if(gwLastAck == ACK_OK)
		{
			return 0;
		}
	}

	return -1;
}

int main ()
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
			oem_cmos_led (true);
			usleep(3*1000000);
			oem_cmos_led (false);

			/*

			int cnt = oem_enroll_count();
			printf ("oem_enroll_count=[%d]\n", cnt);

			int nID = 1;
			int nTurn = 1;

			oem_cmos_led (true);
			for (nTurn=1; nTurn<= 3; nTurn++)
			{
				//Capturing (true);
				oem_enroll_nth (nID, nTurn);

				while (!oem_is_press_finger())
				{

				}

				printf ("nTurn=[%d]\n", nTurn);
			}

			oem_cmos_led (false);

			while(1)
			{

			}*/
			oem_close();
		}

	return 0;
}


