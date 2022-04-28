#include "ltkcpp.h"
#include "impinj_ltkcpp.h"
#include <stdio.h>
#include <vector>
#include "MyData.h"
#include "StaticProperties.h"
#include "utils.h"
#include <ros/ros.h>
#include <string>
#include "phase_processing.hpp"
#include "std_msgs/Float32.h"

using namespace LLRP;

/*
** Sorry, we use this linux safe method
** to print buffers.  WIndows has the same
** method, but by a different name
*/
#if (WIN32)
#define snprintf _snprintf
#endif



class CMyApplication
{
private:
	unsigned int m_messageID;

public:
	ros::NodeHandle n;
	ros::Publisher DataVec_pub1 = n.advertise<std_msgs::Float32>("/DataDev_info1", 1);
	ros::Publisher DataVec_pub2 = n.advertise<std_msgs::Float32>("/DataDev_info2", 1);
	ros::Publisher DataVec_pub3 = n.advertise<std_msgs::Float32>("/DataDev_info3", 1);
	ros::Publisher DataVec_pub4 = n.advertise<std_msgs::Float32>("/DataDev_info4", 1);

	double antenna_xyz_data1[3] = {0.785  , 0.64      , 0.13 };
	double antenna_xyz_data2[3] = {-0.605 , 0.64      , 0.13 };
	double antenna_xyz_data3[3] = {0.155   , 0  , 0.121 };
	double antenna_xyz_data4[3] = {-0.155 , 0  , 0.121 };
	double label_xyz_data[3]    = {0.35       ,1.82 , 0.435 };
	/** Verbose level, incremented by each -v on command line */
	//int        					bDone = 0;
	int                         m_Verbose;
	//TagData                     leftdataArray[1500];
	//int                         leftdataIndex = 0;
	//TagData                     rightdataArray[1500];
	//int                         rightdataIndex = 0;
	std::vector<MyData>           DataVec1;
	std::vector<MyData>           DataVec2;
	std::vector<MyData>           DataVec3;
	std::vector<MyData>           DataVec4;
	unsigned int m_channelIndex; // frequency point (1-16), default to 1


	/** Connection to the LLRP reader */
	CConnection *               m_pConnectionToReader;

	inline
		CMyApplication(void)
		: m_Verbose(0), m_pConnectionToReader(NULL)
	{
		m_messageID = 0;
		m_channelIndex = 1;
	}

	int
		run(
		char *                    pReaderHostName);

	int
		checkConnectionStatus(void);

	int
		enableImpinjExtensions(void);

	int
		resetConfigurationToFactoryDefaults(void);

	int
		getReaderCapabilities(void);

	int
		setImpinjReaderConfig();

	int
		addROSpec(void);

	int
		enableROSpec(void);

	int
		startROSpec(void);

	int
		stopROSpec(void);

	int
		awaitAndPrintReport(int timeout);

	int numi;

	void
		printTagReportData(
		CRO_ACCESS_REPORT *       pRO_ACCESS_REPORT);

	void
		printOneTagReportData(
		CTagReportData *          pTagReportData);

	void
		formatOneEPC(
		CParameter *          pEpcParameter,
		char *                buf,
		int                   buflen);

	int getOnePhaseAngle(
		CImpinjRFPhaseAngle  *pRfPhase,
		double               *out);

	int
		getOnePeakRSSI(
		CImpinjPeakRSSI      *pPeakRSSI,
		double               *out);


	int
		getOneTimestamp(
		CParameter           *pTimestamp,
		unsigned long long   *out);

	int
		getOneAntenna(
		CAntennaID           *pAntenna,
		unsigned short       *out);

	int
		getOneChannelIndex(
		CChannelIndex        *pChannelIndex,
		unsigned short       *out);

	int
		estimateVelocity(
		char *                epcStr,
		double                rssi,
		double                phase,
		unsigned short        channelIndex,
		unsigned short        antenna,
		unsigned long long    time,
		double                *outVelocity);

	void
		handleReaderEventNotification(
		CReaderEventNotificationData *pNtfData);

	void
		handleAntennaEvent(
		CAntennaEvent *           pAntennaEvent);

	void
		handleReaderExceptionEvent(
		CReaderExceptionEvent *   pReaderExceptionEvent);

	int
		checkLLRPStatus(
		CLLRPStatus *             pLLRPStatus,
		char *                    pWhatStr);

	CMessage *
		transact(
		CMessage *                pSendMsg);

	CMessage *
		recvMessage(
		int                       nMaxMS);

	int
		sendMessage(
		CMessage *                pSendMsg);

	void
		printXMLMessage(
		CMessage *                pMessage);

};
