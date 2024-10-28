#pragma once

#ifndef _BRDM2POS_H_
#define _BRDM2POS_H_

#include <iostream>
#include <math.h>
#include <time.h>

#endif // _BRDM2POS_H_

/* CALCU CONST*/
#define C_V     299792458
#define GM      398600500000000
#define math_e  2.718281828459
#define PI      3.141592653589793
#define Earth_e 7.2921151467e-5
#define C20		1.0826257e-3
/*WGS-84 CONST*/
#define a       6378137.0
#define e2      (0.0033528106647475*(2 - 0.0033528106647475))
/*PZ-90 CONST*/
#define TSTEP	30.0
/*GNSS OBSERV TYPE*/
//frequency 1
#define C1		100
#define C1A		100
#define C1B		101
#define C1C		102
#define C1D		103
#define C1E
#define C1F
#define C1G
#define C1H
#define C1I
#define C1J
#define C1K
#define C1L		104
#define C1M		105
#define C1N
#define C1O
#define C1P		106
#define C1Q
#define C1R
#define C1S		107
#define C1T
#define C1U
#define C1V
#define C1W
#define C1X		108
#define C1Y		109
#define C1Z		110
//frequency 2
#define C2		200
#define C2A
#define C2B
#define C2C		200
#define C2D		201
#define C2E
#define C2F
#define C2G
#define C2H
#define C2I		202
#define C2J
#define C2K
#define C2L		203
#define C2M		204
#define C2N
#define C2O
#define C2P		205
#define C2Q		206
#define C2R
#define C2S		207
#define C2T
#define C2U
#define C2V
#define C2W
#define C2X		208
#define C2Y		209
#define C2Z		210
//frequency 3
#define C3		300
#define C3I		300
#define C3Q		301
#define C3X		302
//frequency 4
#define C4		400
#define C4A		400
#define C4B		401
#define C4X		402
//frequency 5
#define C5		500
#define C5A
#define C5B
#define C5C
#define C5D
#define C5E
#define C5F
#define C5G
#define C5H
#define C5I		500
#define C5J
#define C5K
#define C5L
#define C5M
#define C5N
#define C5O
#define C5P
#define C5Q		501
#define C5R
#define C5S
#define C5T
#define C5U
#define C5V
#define C5W
#define C5X		502
#define C5Y
#define C5Z
//frequency 6
#define C6		600
#define C6A		600
#define C6B		601
#define C6C		602
#define C6D
#define C6E
#define C6F
#define C6G
#define C6H
#define C6I
#define C6J
#define C6K
#define C6L
#define C6M
#define C6N
#define C6O
#define C6P
#define C6Q
#define C6R
#define C6S
#define C6T
#define C6U
#define C6V
#define C6W
#define C6X		603
#define C6Y
#define C6Z		604
//frequency 7
#define C7		700
#define C7A
#define C7B
#define C7C
#define C7D
#define C7E
#define C7F
#define C7G
#define C7H
#define C7I		700
#define C7J
#define C7K
#define C7L
#define C7M
#define C7N
#define C7O
#define C7P
#define C7Q		701
#define C7R
#define C7S
#define C7T
#define C7U
#define C7V
#define C7W
#define C7X		702
#define C7Y
#define C7Z
//frequency 8
#define	C8		800
#define C8I		800
#define C8Q		801
#define C8X		802
/*GNSS CODE*/
#define GPS		01
#define BDS		02
#define GAL		03
#define GLO		04
#define SBAS	05

#define MAXRINEX 1000
#define DAYSEC	 86400
//satellite position & clock bias structure
typedef struct
{
	double X;
	double Y;
	double Z;
	double deltat;
	double delta_t;
	double delta_clk;
}pos_ts;
//receiver station position & clock bias structure
typedef struct
{
	double X;
	double Y;
	double Z;
	double B;
	double L;
	double H;
	double delta_TR;
}stations;
//longitude & latitude structure
typedef struct
{
	double B;
	int B_d;
	int B_m;
	int B_s;
	double L;
	int L_d;
	int L_m;
	int L_s;
	double H;
}blhs;
//satellite azimuth angle structure
typedef struct
{
	double R;
	double A;
	double H;
}rahcal;
//local Cartesian coordinates coordinate system structure
typedef struct
{
	double E;
	double N;
	double U;
}blh2enu;

typedef struct
{
	double B;
	double L;
	double H;
}xyz2blh;
//header data of file of nav
typedef struct nav_head
{
	double ver;//rinex 
	char type[20];
	double ION_GPSA[4];
	double ION_GPSB[4];
	double ION_BDSA[4];
	double ION_BDSB[4];
	double ION_QZSA[4];
	double ION_QZSB[4];
	double ION_IRNA[4];
	double ION_IRNB[4];
	double GPUT[4];
	double GLUT[4];
	double GAUT[4];
	double BDUT[4];
	double QZUT[4];
	double IRUT[4];
	double SBUT[4];
	int leap;
}nav_head, * pnav_head;
//body data of file of nav: GPS	BeiDou	Galileo
typedef struct nav_body
{
	int sPRN_GPS;	int sPRN_BDS;	int sPRN_GAL;	int sPRN_GLO;
	int TOC_Y;
	int TOC_M;
	int TOC_D;
	int TOC_H;
	int TOC_Min;
	int TOC_Sec;
	double sa0;
	double sa1;
	double sa2;										double Dos;

	double IODE;	double AODE;					double SatX;
	double Crs;										double SatXv;
	double deltan;									double SatXa;
	double M0;

	double Cuc;										double SatY;
	double e;										double SatYv;
	double Cus;										double SatYa;
	double sqrtA;									int FreN;

	double TOE;										double SatZ;
	double Cic;										double SatZv;
	double OMEGA;									double SatZa;
	double Cis;										int AOO;

	double i0;
	double Crc;
	double omega;
	double deltaomega;

	double IDOT;
	double L2code;					int Datasource;
	double GPSweek;	double BDTweek;	double GALweek;
	double L2Pflag;

	double sACC;
	double sHEA;
	double TGD;		double TGD1;	double BGDa;
	double IODC;	double TGD2;	double BGDb;

	double TTN;
	double fit;		double AODC;
	double spare1;
	double spare2;

}nav_body, * pnav_body;
//header data of file of obs
typedef struct obs_head
{
	double ver;
	char type[30];
	double apX;
	double apY;
	double apZ;
	double ANTH;
	double ANTdeltaE;
	double ANTdeltaN;
	int obstypenum_gps;
	int obstypenum_bds;
	int obstypenum_gal;
	int obstypenum_glo;
	int obscode_gps[40];
	int obscode_bds[40];
	int obscode_gal[40];
	int obscode_glo[40];
	double interval;
	int f_y;
	int f_m;
	int f_d;
	int f_h;
	int f_min;
	double f_sec;
	int l_y;
	int l_m;
	int l_d;
	int l_h;
	int l_min;
	double l_sec;
	char tsys[5];//time system
}obs_head, * pobs_head;
//epoch data of file of obs
typedef struct obs_epoch
{
	int y;
	int m;
	int d;
	int h;
	int min;
	double sec;//epoch time
	int p_flag;//epoch flag
	int sat_num;//the total number of obsable sat
	int gps_num;//the total gps sat
	int bds_num;//the total bds sat
	int gal_num;//the total galileo sat
	int glo_num;//the total glonass sat
	int sPRN[84];//total sprn of obs sat
	int sPRN_GPS[32];
	int sPRN_BDS[60];
	int sPRN_GAL[30];
	int sPRN_GLO[24];
}obs_epoch, * pobs_epoch;
//body data of file of obs
typedef struct obs_body
{
	double obs_gps[20][26];//GPS obs data
	double obs_bds[30][26];//BDS obs data
	double obs_gal[20][26];//GALILEO obs data
	double obs_glo[20][26];//GLONASS obs data
}obs_body, * pobs_body;
//
extern double JDUTC2GPST(double);
extern double Time2GPST(int, int, int, double, int, double);
extern double UTCTime2JD(int, int, int, double, int, double);
//
extern double deg2rad(double);
extern double rad2deg(double);
//
extern rahcal RAHCAL(rahcal, double, double, double);
extern blh2enu BLH2ENU(blh2enu, double, double, double, double, double);
extern xyz2blh XYZ2BLH(xyz2blh, double, double, double);
//
extern int getsatnum(FILE*);
extern int get_epochnum(FILE*);
extern void initobs_e(pobs_epoch, pobs_body);
extern void freeobs_e(pobs_epoch, pobs_body);
extern int Type2Code(int, char buff[MAXRINEX]);
extern int Code2Type(int, int, int typearr[36]);
extern int select_epoch(double, int, pnav_body, int, int);
//
extern void read_n_h(FILE*, pnav_head);
extern void read_n_b(FILE*, pnav_body);
extern void read_o_h(FILE*, pobs_head);
extern void read_o_eb(FILE*, pobs_head, pobs_epoch, pobs_body);
//
extern "C" _declspec(dllexport) double brdm2pos(char nav_path[260], char obs_path[260], char res_path[260], int gnsscode);

