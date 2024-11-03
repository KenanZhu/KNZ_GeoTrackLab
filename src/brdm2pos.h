#pragma once

#ifndef _BRDM2POS_H_
#define _BRDM2POS_H_

#include <iostream>
#include <math.h>
#include <time.h>

#endif // _BRDM2POS_H_

#define KNZ_GTL_VER   "1.5.5.0"

/* CALCU CONST*/
#define C_V     299792458               /* Speed of light (m/s) */
#define GM      398600500000000         /*  */
#define math_e  2.718281828459          /* Natural constant e */
#define PI      3.141592653589793       /* Ratio of circumference to diameter */
#define Earth_e 7.2921151467e-5         /* Rotational angular velocity of the earths (omega/s) */
#define C20     1.0826257e-3            /*  */
#define DAYSEC  86400                   /* The total second of a day */
/*WGS-84 CONST*/
#define a       6378137.0
#define e2      (0.0033528106647475*(2 - 0.0033528106647475))
/*PZ-90 CONST*/
#define TSTEP   30.0                    /* RK-4 step */
/*GNSS OBSERV TYPE*/
#define FREQ1       1.57542E9           /* L1/E1/B1C  frequency (Hz) */
#define FREQ2       1.22760E9           /* L2         frequency (Hz) */
#define FREQ5       1.17645E9           /* L5/E5a/B2a frequency (Hz) */
#define FREQ6       1.27875E9           /* E6/L6  frequency (Hz) */
#define FREQ7       1.20714E9           /* E5b    frequency (Hz) */
#define FREQ8       1.191795E9          /* E5a+b  frequency (Hz) */
#define FREQ9       2.492028E9          /* S      frequency (Hz) */
#define FREQ1_GLO   1.60200E9           /* GLONASS G1 base frequency (Hz) */
#define DFRQ1_GLO   0.56250E6           /* GLONASS G1 bias frequency (Hz/n) */
#define FREQ2_GLO   1.24600E9           /* GLONASS G2 base frequency (Hz) */
#define DFRQ2_GLO   0.43750E6           /* GLONASS G2 bias frequency (Hz/n) */
#define FREQ3_GLO   1.202025E9          /* GLONASS G3 frequency (Hz) */
#define FREQ1a_GLO  1.600995E9          /* GLONASS G1a frequency (Hz) */
#define FREQ2a_GLO  1.248060E9          /* GLONASS G2a frequency (Hz) */
#define FREQ1_BDS   1.561098E9          /* BDS B1I     frequency (Hz) */
#define FREQ2_BDS   1.20714E9           /* BDS B2I/B2b frequency (Hz) */
#define FREQ3_BDS   1.26852E9           /* BDS B3      frequency (Hz) */
//frequency 1
#define C1      100
#define C1A     100
#define C1B     101
#define C1C     102
#define C1D     103
#define C1L     104
#define C1M     105
#define C1P     106
#define C1S     107
#define C1X     108
#define C1Y     109
#define C1Z     110
//frequency 2
#define C2      200
#define C2C     200
#define C2D     201
#define C2I     202
#define C2L     203
#define C2M     204
#define C2P     205
#define C2Q     206
#define C2R
#define C2S     207
#define C2X     208
#define C2Y     209
#define C2Z     210
//frequency 3
#define C3      300
#define C3I     300
#define C3Q     301
#define C3X     302
//frequency 4
#define C4      400
#define C4A     400
#define C4B     401
#define C4X     402
//frequency 5
#define C5      500
#define C5I     500
#define C5Q     501
#define C5X     502
//frequency 6
#define C6      600
#define C6A     600
#define C6B     601
#define C6C     602
#define C6X     603
#define C6Z     604
//frequency 7
#define C7      700
#define C7I     700
#define C7Q     701
#define C7X     702
//frequency 8
#define	C8      800
#define C8I     800
#define C8Q     801
#define C8X     802
/*GNSS CODE*/
#define GPS     01
#define BDS     02
#define GAL     03
#define GLO     04
#define SBAS    05

#define MAXRINEX    4096    /* Max length of line of rinex file */
#define MAXPATH     260     /* Max length of file path */

typedef struct pos_ts{//Satellite position
    double X;
    double Y;
    double Z;
    double deltat;
    double delta_t;
    double delta_clk;
}pos_ts;

typedef struct stations{//
    double X;
    double Y;
    double Z;
    double delta_TR;
}stations;

typedef struct rah{//
    double R;
    double A;
    double H;
}rah;

typedef struct enu{//East/North/Up coordinate system
    double E;
    double N;
    double U;
}enu;

typedef struct blh{//Longitude/Latitude/Altitude coordinate system
    double B;
    double L;
    double H;
}blh;

typedef struct blhdms{//Longitude/Latitude/Altitude coordinate system 
                //With Degree/Minute/Second
    double B;
    int B_d;
    int B_m;
    int B_s;
    double L;
    int L_d;
    int L_m;
    int L_s;
    double H;
}blhdms;


typedef struct nav_head{//Header data of file of nav
    double ver;         /* RINEX version */
    char type[20];      /* RINEX file format */

    double ION_GPSA[4]; /* Ionosphere correction parameters alpha GPS */
    double ION_GPSB[4]; /* Ionosphere correction parameters belta GPS */
    double ION_BDSA[4]; /* Ionosphere correction parameters alpha BeiDou */
    double ION_BDSB[4]; /* Ionosphere correction parameters belta BeiDou */
    double ION_QZSA[4]; /* Ionosphere correction parameters alpha QZSS */
    double ION_QZSB[4]; /* Ionosphere correction parameters belta QZSS */
    double ION_IRNA[4]; /* Ionosphere correction parameters alpha */
    double ION_IRNB[4]; /* Ionosphere correction parameters belta */

    double GPUT[4];     /* Time system correction of GPST */
    double GLUT[4];     /* Time system correction of GLONASST */
    double GAUT[4];     /* Time system correction of GALT */
    double BDUT[4];     /* Time system correction of BDT */
    double QZUT[4];     /* Time system correction of QZST */
    double IRUT[4];     /* Time system correction of  */
    double SBUT[4];     /* Time system correction of SBAST */

    int leap;           /* Leap second */
}nav_head, * pnav_head;

typedef struct nav_body{//Body data of file of nav: GPS	BeiDou Galileo GLONASS

    /*  GPS             BeiDou          Galileo         GLONASS*/
    int sPRN_GPS;   int sPRN_BDS;   int sPRN_GAL;   int sPRN_GLO;/* System */
    int TOC_Y;
    int TOC_M;
    int TOC_D;
    int TOC_H;
    int TOC_Min;
    int TOC_Sec;
    double sa0;
    double sa1;
    double sa2;                                     double Dos;

    double IODE;    double AODE;                    double SatX;
    double Crs;                                     double SatXv;
    double deltan;                                  double SatXa;
    double M0;

    double Cuc;                                     double SatY;
    double e;                                       double SatYv;
    double Cus;                                     double SatYa;
    double sqrtA;                                   int FreN;

    double TOE;                                     double SatZ;
    double Cic;                                     double SatZv;
    double OMEGA;                                   double SatZa;
    double Cis;                                     int AOO;

    double i0;
    double Crc;
    double omega;
    double deltaomega;

    double IDOT;
    double L2code;                  int Datasource;
    double GPSweek; double BDTweek; double GALweek;
    double L2Pflag;

    double sACC;
    double sHEA;
    double TGD;     double TGD1;    double BGDa;
    double IODC;    double TGD2;    double BGDb;

    double TTN;
    double fit;     double AODC;
    double spare1;
    double spare2;

}nav_body, * pnav_body;

typedef struct obs_head{//Header data of file of obs
    double ver;
    char type[30];

    double apX;
    double apY;
    double apZ;

    double apB;
    double apL;
    double apH;

    double ANTH;
    double ANTdeltaE;
    double ANTdeltaN;

    int obstypenum_gps; /* Observation amount of GPS */
    int obstypenum_bds; /* Observation amount of BeiDou */
    int obstypenum_gal; /* Observation amount of Galilro */
    int obstypenum_glo; /* Observation amount of GLONASS */

    int obscode_gps[40];/* Observation code of GPS */
    int obscode_bds[40];/* Observation code of BeiDou */
    int obscode_gal[40];/* Observation code of Galileo */
    int obscode_glo[40];/* Observation code of GLONASS */

    double interval;	/*  */

    int f_y;            /* Year of first observe */
    int f_m;            /* Month of first observe */
    int f_d;            /* Day of first observe */
    int f_h;            /* Hour of first observe */
    int f_min;          /* Minute of first observe */
    double f_sec;       /* Second of first observe */

    int l_y;            /* Year of last observe */
    int l_m;            /* Month of last observe */
    int l_d;            /* Day of last observe */
    int l_h;            /* Hour of last observe */
    int l_min;          /* Minute of last observe */
    double l_sec;       /* Second of last observe */

    char tsys[5];       /* Time system of obs */
}obs_head, * pobs_head;

typedef struct obs_epoch{//Epoch data of file of obs
    int y;          /* Epoch year */
    int m;          /* Epoch month */
    int d;          /* Epoch day */
    int h;          /* Epoch hour */
    int min;        /* Epoch minute */
    double sec;     /* Epoch second */
    int p_flag;     /* Epoch flag */
    int sat_num;    /* The total number of obsable sat */
    int gps_num;    /* The total GPS satellite */
    int bds_num;    /* The total BeiDou satellite */
    int gal_num;    /* The total Galileo satellite */
    int glo_num;    /* The total GLONASS satellite */
    int sPRN[84];   /* Total sprn of obs satellite */
    int sPRN_GPS[32];/* Total sprn of GPS satellite in this epoch */
    int sPRN_BDS[60];/* Total sprn of BeiDou satellite in this epoch */
    int sPRN_GAL[30];/* Total sprn of Galileo satellite in this epoch */
    int sPRN_GLO[24];/* Total sprn of GLONASS satellite in this epoch */
}obs_epoch, * pobs_epoch;

typedef struct obs_body{//Body data of file of obs
    double obs_gps[30][26];/* GPS obs data */
    double obs_bds[40][26];/* BeiDou obs data */
    double obs_gal[30][26];/* Galileo obs data */
    double obs_glo[30][26];/* GLONASS obs data */
}obs_body, * pobs_body;

typedef struct lsq_part {
    double* l;
    double* m;
    double* n;
    double* o;
    double* B;
    double* P;
    double* L;
    double* x;
}lsq_part;

typedef struct acct_obs {
    double Per1[30];
    double Per2[30];
    double sclk[30];
    int freq1;
    int freq2;

    acct_obs() = default;
}acct_obs;

//Contain in timesys.cpp
extern double jdutc2gpst(double JD_UTCSU);
extern double time2gpst(int y, int m, int d, double h, int min, double sec);
extern double utctime2jd(int y, int m, int d, double h, int min, double sec);
//Contain in martix.cpp
extern double* mat(int n, int m);
extern int* imat(int n, int m);
extern double* zeros(int n, int m);
extern double* eye(int n);
extern double dot(const double* va, const double* vb, int n);
extern double norm(const double* va, int n);
extern void cross3(const double* va, const double* vb, double* vc);
extern int normv3(const double* va, double* vb);
extern void matcpy(double* A, const double* B, int n, int m);
extern void matmul(const char* tr, int n, int k, int m, double alpha,
    const double* A, const double* B, double beta, double* C);
extern int matinv(double* A, int n);
extern int solve(const char* tr, const double* A, const double* Y, int n,
    int m, double* X);
extern stations designmat(pobs_head obs_h, acct_obs obs,
    double* l, double* m, double* n, double* o,
    double* B, double* P, double* L,
    double X, double Y, double Z, int satnum, int ionopt, int tropopt,
    int GNSS);
extern int lsq(const double* BtP, const double* L, const double* B, int n, int m, double* x,
    double* Q);
extern void matprint(const double A[], int n, int m, int p, int q);
//Contain in coordtrans.cpp
extern double deg2rad(double deg);
extern double rad2deg(double rad);
extern rah rahcal(rah rah, double E, double N, double U);
extern enu blh2enu(enu enu, double stationB, double stationL,
    double deltax, double deltay, double deltaz);
extern blh xyz2blh(blh blh, double X, double Y, double Z);
extern rah xyz2rah(pos_ts pos_t, pobs_head obs_h);
extern void pz90towgs84(double X, double Y, double Z);
//Contain in readrnx.cpp
extern int getsatnum(FILE*);
extern int get_epochnum(FILE*);
extern void freeobs_e(pobs_epoch, pobs_body);
extern int type2code(int, char buff[MAXRINEX]);
extern int code2type(int, int, int typearr[36]);
extern int select_epoch(double, int, pnav_body, int, int);
//Contain in readrnx.cpp/read
extern void read_n_h(FILE*, pnav_head);
extern void read_n_b(FILE*, pnav_body);
extern void read_o_h(FILE*, pobs_head);
extern void read_o_eb(FILE*, pobs_head, pobs_epoch, pobs_body);
//Contain in solutionout.cpp
extern FILE* headerout(pobs_head obs_h, char obs_path[MAXPATH], char nav_path[MAXPATH], char res_path[MAXPATH]);
extern void solution(FILE* res_file, pobs_head obs_h, double X, double Y, double Z);
extern void outdata(blh blh, FILE* res_file, int sPRN, int GNSS);
//Entry function
extern "C" _declspec(dllexport) double brdm2pos(
    char nav_path[MAXPATH],
    char obs_path[MAXPATH],
    char res_path[MAXPATH],
    int GNSS,
    int Hangle,
    int ionopt,
    int tropopt);

