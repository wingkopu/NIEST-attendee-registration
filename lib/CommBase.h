//SHW080926

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

#include <linux/hdreg.h>


#define FALSE   0
#define TRUE    1

typedef unsigned int       DWORD;
typedef int                 BOOL;
typedef unsigned char       BYTE;
typedef unsigned short      WORD;
typedef float               FLOAT;
typedef FLOAT               *PFLOAT;


typedef int                 INT;
typedef unsigned int        UINT;
typedef unsigned int        *PUINT;

typedef unsigned long ULONG;
typedef ULONG *PULONG;
typedef unsigned short USHORT;
typedef USHORT *PUSHORT;
typedef unsigned char UCHAR;
typedef UCHAR *PUCHAR;

typedef void *PVOID;

typedef void *HANDLE;

#define INVALID_HANDLE_VALUE (HANDLE)-1
#define INVALID_FILE_SIZE (DWORD)0xFFFFFFFF

#define _T(x)      x

#define METHOD_BUFFERED                 0
#define FILE_DEVICE_CONTROLLER          0x00000004
#define FILE_READ_ACCESS          ( 0x0001 )    // file & pipe
#define FILE_WRITE_ACCESS         ( 0x0002 )    // file & pipe

#define CTL_CODE( DeviceType, Function, Method, Access ) (                 \
((DeviceType) << 16) | ((Access) << 14) | ((Function) << 2) | (Method) \
)

#pragma once

//////////////////////////////////////////////////////////////////////////
inline void ui_polling()
{
	/*MSG msg;

	while ( PeekMessage(&msg,NULL,0,0,PM_REMOVE)) 
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}*/
}
void debug_printf(char *fmt,...);

//////////////////////////////////////////////////////////////////////////
extern double comm_percent;
extern int gn_comm_type;


int comm_send(BYTE* pbuf, int nsize, int ntimeout);
int comm_recv(BYTE* pbuf, int nsize, int ntimeout);
BOOL comm_open_serial(int nComNumber, int nComBaudRate);
BOOL comm_open_usb();
void comm_close();

/************************************************************************/
/*     USB Communication Definitions                                    */
/************************************************************************/
//////////////////////////////////////////////////////////////////////////
typedef struct _SCSI_PASS_THROUGH_DIRECT {
	USHORT  Length;
	UCHAR  ScsiStatus;
	UCHAR  PathId;
	UCHAR  TargetId;
	UCHAR  Lun;
	UCHAR  CdbLength;
	UCHAR  SenseInfoLength;
	UCHAR  DataIn;
	ULONG  DataTransferLength;
	ULONG  TimeOutValue;
	PVOID  DataBuffer;
	ULONG  SenseInfoOffset;
	UCHAR  Cdb[16];
}SCSI_PASS_THROUGH_DIRECT, *PSCSI_PASS_THROUGH_DIRECT;

typedef struct _SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER {
    SCSI_PASS_THROUGH_DIRECT sptd;
    ULONG             Filler;      // realign buffer to double word boundary
    UCHAR             ucSenseBuf[32];
} SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER, *PSCSI_PASS_THROUGH_DIRECT_WITH_BUFFER;

#define CDB10GENERIC_LENGTH                  10
#define SCSI_IOCTL_DATA_OUT          0
#define SCSI_IOCTL_DATA_IN           1
#define SCSI_IOCTL_DATA_UNSPECIFIED  2
#define IOCTL_SCSI_BASE                 FILE_DEVICE_CONTROLLER
#define IOCTL_SCSI_PASS_THROUGH_DIRECT  CTL_CODE(IOCTL_SCSI_BASE, 0x0405, METHOD_BUFFERED, FILE_READ_ACCESS | FILE_WRITE_ACCESS)

int CDROM_ScsiPassThroughDirect(int fd, PSCSI_PASS_THROUGH_DIRECT pPacket);

class CCommUSB
{
public:
	CCommUSB();
	virtual ~CCommUSB();
	
	BOOL Open();
	void Close();
	int SendData(BYTE *pBuf, int nSize, DWORD dwTimeOut);
	int RecvData(BYTE *pBuf, int nSize, DWORD dwTimeOut);
	
private:
	BOOL	SCSI_Open();
	void	SCSI_Close();
	int		SCSI_Operation(BYTE *pBuf, int nSize, DWORD dwTimeOut, BOOL bRead);
	int		OperationInternal(BYTE *pBuf, int nSize, DWORD dwTimeOut, BOOL bRead);
	
	//HANDLE	m_hDevice;
	int 	m_hDevice;
};

enum
{
	COMM_MODE_SERIAL,
	COMM_MODE_USB,
};
