/*
 * @Author: KenanZhu111 3471685733@qq.com
 * @Date: 2024-09-20 21:47:22
 * @LastEditors: KenanZhu111 3471685733@qq.com
 * @LastEditTime: 2024-10-26 10:13:40
*/
#include "pch.h"
#include <iostream>
#include <math.h>
#include <time.h>
using namespace std;
/* -------------------------------------------------------------------------- */
/// @brief Convert UTC to GPS Second of week
/// @param y Year
/// @param m Month
/// @param d Day
/// @param h Hour
/// @param min Minute
/// @param sec Second
/// @return Return GPS Second of week
/* -------------------------------------------------------------------------- */
double Time2GPST(int y, int m, int d, double h, int min, double sec)
{
	if (m > 2){
		y = y;
		m = m;
	}
	if (m <= 2){
		y = y - 1;
		m = m + 12;
	}
	h = h + min / 60.0 + sec / 3600.0;
	double JD = (int)(365.25 * y) + (int)(30.6001 * (m + 1)) + d + h / 24.0 + 1720981.5;
	double MJD = JD - 2400000.5;
	int gpsweek = (int)((MJD - 44244) / 7);
	double secofweek = (MJD - 44244.0 - gpsweek * 7.0) * 86400.0;
	return secofweek;
}
double JDUTC2GPST(double JD_UTCSU)
{
	double n;//Leap second

	if (2451179.5000000 < JD_UTCSU && JD_UTCSU < 2453736.5000000) { n = 32.0; }
	else if (2453736.5000000 < JD_UTCSU && JD_UTCSU < 2454832.5000000) { n = 33.0; }
	else if (2454832.5000000 < JD_UTCSU && JD_UTCSU < 2455927.5000000) { n = 34.0; }
	else if (2455927.5000000 < JD_UTCSU && JD_UTCSU < 2457023.5000000) { n = 35.0; }
	else if (2457023.5000000 < JD_UTCSU && JD_UTCSU < 2457754.5000000) { n = 36.0; }
	else if (2457754.5000000 < JD_UTCSU) { n = 37.0; }

	JD_UTCSU += ((n * 1 - 19) / 3600.0) / 24.0;
	double MJD = JD_UTCSU - 2400000.5;
	int gpsweek = (int)((MJD - 44244) / 7);
	double secofweek = (MJD - 44244.0 - gpsweek * 7.0) * 86400.0;
	return secofweek;
}
double UTCTime2JD(int y, int m, int d, double h, int min, double sec)
{
	if (m > 2){
		y = y;
		m = m;
	}
	if (m <= 2){
		y = y - 1;
		m = m + 12;
	}
	h = h + min / 60.0 + sec / 3600.0;
	double JD = (int)(365.25 * y) + (int)(30.6001 * (m + 1)) + d + h / 24.0 + 1720981.5;
	return JD;
}

/* -------------------------------------------------------------------------- */
/// @brief Degree to radian
/// @param deg 
/// @return Return radian
/* -------------------------------------------------------------------------- */
double deg2rad(double deg)
{
	double rad = (PI / 180) * deg;
	return rad;
}

/* -------------------------------------------------------------------------- */
/// @brief Radian to degree                      
/// @param rad 
/// @return Return degree
/* -------------------------------------------------------------------------- */
double rad2deg(double rad)
{
	double deg = (180 / PI) * rad;
	return deg;
}

/* -------------------------------------------------------------------------- */
/// @brief Satellite azimuth angle calculation
/// @param rahcal Parameter transfer structure
/// @param E East
/// @param N North
/// @param U Up
/// @return Return structure contain R, A, H members                      
/* -------------------------------------------------------------------------- */
rahcal RAHCAL(rahcal rahcal,
	double E, double N, double U)
{
	rahcal.H = atan2(U, sqrt(E * E + N * N));
	rahcal.A = atan2(E, U);
	if (rahcal.A < 0)
		rahcal.A += 2 * PI;
	if (rahcal.A > 2 * PI)
		rahcal.A -= 2 * PI;
	rahcal.R = sqrt(E * E + N * N + U * U);

	return rahcal;
}

/* -------------------------------------------------------------------------- */
/// @brief Convert BLH coordinates to ENU coordinates
/// @param blh2enu Parameter transfer structure
/// @param stationB Latitude of receiver station
/// @param stationL Longitude of receiver station
/// @param deltax X-coordinate difference of satellite arrival center
/// @param deltay Y-coordinate difference of satellite arrival center
/// @param deltaz Z-coordinate difference of satellite arrival center
/// @return Return type of structure contain E, N, U members
/* -------------------------------------------------------------------------- */
blh2enu BLH2ENU(blh2enu blh2enu,
	double stationB, double stationL,
	double deltax, double deltay, double deltaz)
{
	double sinB = sin(stationB);
	double cosB = cos(stationB);
	double sinL = sin(stationL);
	double cosL = cos(stationL);
	blh2enu.E = -sinL * (deltax)+cosL * (deltay);
	blh2enu.N = -sinB * cosL * (deltax)-sinB * sinL * (deltay)+cosB * (deltaz);
	blh2enu.U = cosB * cosL * (deltax)+cosB * sinL * (deltay)+sinB * (deltaz);

	return blh2enu;
}

/* -------------------------------------------------------------------------- */
/// @brief Convert ECEF geostationary coordinates to BLH coordinates
/// @param xyz2blh parameter transfer structure
/// @param X X coordinates of ECEF
/// @param Y Y coordinates of ECEF
/// @param Z Z coordinates of ECEF
/// @param a Major semiaxis of WGS-84 ellipsoid
/// @param e2 The square of the first eccentricity of WGS-84 ellipsoid
/// @return Return type of structure contain B, L, H members
/* -------------------------------------------------------------------------- */
xyz2blh XYZ2BLH(xyz2blh xyz2blh,
	double X, double Y, double Z)
{
	double B = 0.0, N = 0.0, H = 0.0, R0, R1, deltaH, deltaB;
	R0 = sqrt(pow(X, 2) + pow(Y, 2));
	R1 = sqrt(pow(X, 2) + pow(Y, 2) + pow(Z, 2));
	xyz2blh.L = atan2(Y, X);
	N = a;
	H = R1 - a;
	B = atan2(Z * (N + H), R0 * (N * (1 - e2) + H));
	do{
		deltaH = N;
		deltaB = B;
		N = a / sqrt(1 - e2 * pow(sin(B), 2));
		H = R0 / cos(B) - N;
		B = atan2(Z * (N + H), R0 * (N * (1 - e2) + H));
	} while (fabs(deltaH - H) > 1.0e-3 && fabs(deltaB - B) > 1.0e-9);
	xyz2blh.B = B;
	xyz2blh.H = H;

	return xyz2blh;
}

/* -------------------------------------------------------------------------- */
/// @brief Find the nearest obs epoch with boardcast
/// @param SecofWeek Second of week of obs epoch time
/// @param sPRN The satellite PRN which need to match
/// @param nav_b Nav data file structure
/// @param satnum Total number of boardcast satellite 
/// @param syscode GNSS code, more on PPUBLIC.H
/// @return Return the absolute epoch number of the best epoch 
///			When there is no matching satellite number, the function returns -1
/* -------------------------------------------------------------------------- */
int select_epoch(double SecofWeek, int sPRN, pnav_body nav_b, int satnum, int syscode)
{
	int best_epoch = -1;
	double min = 10000;//Initialize the minimum value
	double Min;
	if (syscode == GPS){ //Be judged as GPS
		for (int i = 0; i < satnum; i++){
			if (sPRN == nav_b[i].sPRN_GPS){
				Min = fabs(SecofWeek - nav_b[i].TOE);
				if (Min <= min){
					best_epoch = i;
					min = Min;
				}
			}
		}return best_epoch;
	}
	if (syscode == BDS){ //Be judged as BeiDou
		for (int i = 0; i < satnum; i++){
			if (sPRN == nav_b[i].sPRN_BDS){
				Min = fabs(SecofWeek - nav_b[i].TOE);
				if (Min <= min){
					best_epoch = i;
					min = Min;
				}
			}
		}return best_epoch;
	}
	if (syscode == GAL){ //Be judged as Galileo
		for (int i = 0; i < satnum; i++){
			if (sPRN == nav_b[i].sPRN_GAL){
				Min = fabs(SecofWeek - nav_b[i].TOE);
				if (Min <= min){
					best_epoch = i;
					min = Min;
				}
			}
		}return best_epoch;
	}
	if (syscode == GLO){ //Be judged as GLONASS
		for (int i = 0; i < satnum; i++){
			if (sPRN == nav_b[i].sPRN_GLO){
				Min = fabs(SecofWeek - nav_b[i].TOE);
				if (Min <= min){
					best_epoch = i;
					min = Min;
				}
			}
		}return best_epoch;
	}return best_epoch;
}

/* -------------------------------------------------------------------------- */
/// @brief Converts the observation type to the numeric code defined in PUBLIC.H
/// @param i Reads the number of incoming loops in the loop
/// @param buff Type of incoming observation
/// @return Returns the obs code
/* -------------------------------------------------------------------------- */
int Type2Code(int i, char buff[1000])
{
	int  code_return = 0;
	char code_contrast[4];
	char code_original[4];

	const char L1codeindex[] = "C1AC1BC1CC1DC1LC1MC1PC1SC1XC1YC1Z";//obs type of different frequency 
	const char L2codeindex[] = "C2CC2DC2IC2LC2MC2PC2QC2SC2XC2YC2Z";
	const char L3codeindex[] = "C3IC3QC3X";
	const char L4codeindex[] = "C5IC5QC5X";
	const char L5codeindex[] = "C5IC5QC5X";
	const char L6codeindex[] = "C6AC6BC6CC6XC6Z";
	const char L7codeindex[] = "C7IC7QC7XC7DC7PC7Z";
	const char L8codeindex[] = "C8IC8QC8X";

	memset(code_contrast, 0, sizeof(code_contrast));
	memset(code_original, 0, sizeof(code_original));

	strncpy(code_original, buff + 7 + 4 * i, 3);

	if (strstr(code_original, "1")){
		for (int j = 0; j < (strlen(L1codeindex) / 3); j++){
			strncpy(code_contrast, L1codeindex + 0 + j * 3, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 100;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "2")){
		for (int j = 0; j < (strlen(L2codeindex) / 3); j++){
			strncpy(code_contrast, L2codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 200;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "3")){
		for (int j = 0; j < (strlen(L3codeindex) / 3); j++){
			strncpy(code_contrast, L3codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 500;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "4")){
		for (int j = 0; j < (strlen(L3codeindex) / 3); j++){
			strncpy(code_contrast, L3codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 500;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "5")){
		for (int j = 0; j < (strlen(L5codeindex) / 3); j++){
			strncpy(code_contrast, L5codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 500;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "6")){
		for (int j = 0; j < (strlen(L6codeindex) / 3); j++){
			strncpy(code_contrast, L6codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 600;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "7")){
		for (int j = 0; j < (strlen(L7codeindex) / 3); j++){
			strncpy(code_contrast, L7codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 700;
				return code_return;
				break;
			}
		}
	}
	if (strstr(code_original, "8")){
		for (int j = 0; j < (strlen(L8codeindex) / 3); j++){
			strncpy(code_contrast, L8codeindex + 0 + j * 3, 3);
			strncpy(code_original, buff + 7 + 4 * i, 3);
			if (strcmp(code_contrast, code_original) == 0){
				code_return = j + 800;
				return code_return;
				break;
			}
		}
	}return code_return;
}

/* -------------------------------------------------------------------------- */
/// @brief The type of the obs value read matches the type code stored in an array
/// @param typecode Obs type that you want to match
/// @param typenum The total number of obs types
/// @param typearr Type codes store arrays
/// @return Returns the array position of the corresponding obs type code
/* -------------------------------------------------------------------------- */
int Code2Type(int typecode, int typenum, int typearr[36])
{
	int pos;
	for (pos = 0; pos < typenum; pos++) {
		if ((typearr[pos] - typearr[pos] % 100) == typecode) {
			return pos;
		}
	}return pos;
}

/*Allocate the memory of observation structure*/
void initobs_e(pobs_epoch obs_e, pobs_body obs_b)
{
	obs_e = (pobs_epoch)malloc(sizeof(obs_epoch));
	obs_b = (pobs_body)malloc(sizeof(obs_body));
}

/*Free the memory of observation structure*/
void freeobs_e(pobs_epoch obs_e, pobs_body obs_b)
{
	free(obs_e); free(obs_b);
}

/* -------------------------------------------------------------------------- */
/// @brief Convert the string to number
/// @param buff 
/// @param i Position of begin to read
/// @param n The number of character will to capture
/// @return Number of string you captured
/* -------------------------------------------------------------------------- */
double strtonum(const char* buff, int i, int n)
{
	double value = 0.0;
	char str[256] = { 0 };
	char* p = str;
	/* ---------------------------------- */
	/// Function will return 0.0 as error code when three occasion are below:
	/// 1.Begining position < 0
	/// 2.The number of Byte of read < i
	/// 3.The Byte size of string < n
	/* ---------------------------------- */
	if (i < 0 || (int)strlen(buff) < i || (int)sizeof(str) - 1 < n){
		return 0.0;
	}
	for (buff += i; *buff && --n >= 0; buff++){
		*p++ = ((*buff == 'D' || *buff == 'd') ? 'e' : *buff);
	}
	*p = '\0';
	return sscanf(str, "%lf", &value) == 1 ? value : 0.0;
}

/* -------------------------- Read the file of nav -------------------------- */
/* -------------------------------------------------------------------------- */
/// @brief get the total number of satellite boardcast data of nav file 
/// @param fp_nav the file pointer of nav file
/// @return total number of satellite boardcast data
/* -------------------------------------------------------------------------- */
int getsatnum(FILE* fp_nav)
{
	int satnum = 0;
	int flag = 0;
	char buff[MAXRINEX];
	char satvar;
	char* lable = buff + 60;

	while (fgets(buff, MAXRINEX, fp_nav)){
		if (strstr(lable, "END OF HEADER")){
			flag = 1;
		}
		if (flag == 1){
			while (fgets(buff, MAXRINEX, fp_nav)){
				strncpy(&satvar, buff + 0, 1);
				if (satvar == 'G' || satvar == 'E' || satvar == 'R' || satvar == 'S' || satvar == 'C' || satvar == 'I' || satvar == 'J'){
					satnum++;
				}
				else{
					continue;
				}
			}
		}
	}return satnum;
}

/*Read the header data of file of nav*/
void read_n_h(FILE* fp_nav, pnav_head nav_h)
{
	char buff[MAXRINEX] = { 0 };
	char* lable = buff;
	int i = 0;
	int j = 0;
	while (fgets(buff, MAXRINEX, fp_nav)){
		if (strstr(lable, "RINEX VERSION / TYPE")){
			nav_h->ver = strtonum(buff, 0, 9);
			strncpy((nav_h->type), buff + 20, 15);
			continue;
		}
		else if (strstr(lable, "GPSA")){
			nav_h->ION_GPSA[0] = strtonum(buff, 6, 12);
			nav_h->ION_GPSA[1] = strtonum(buff, 6 + 12, 12);
			nav_h->ION_GPSA[2] = strtonum(buff, 6 + 12 + 12, 12);
			nav_h->ION_GPSA[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
			continue;
		}
		else if (strstr(lable, "GPSB")){
			nav_h->ION_GPSB[0] = strtonum(buff, 6, 12);
			nav_h->ION_GPSB[1] = strtonum(buff, 6 + 12, 12);
			nav_h->ION_GPSB[2] = strtonum(buff, 6 + 12 + 12, 12);
			nav_h->ION_GPSB[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
			continue;
		}
		else if (strstr(lable, "BDSA")){
			nav_h->ION_BDSA[0] = strtonum(buff, 6, 12);
			nav_h->ION_BDSA[1] = strtonum(buff, 6 + 12, 12);
			nav_h->ION_BDSA[2] = strtonum(buff, 6 + 12 + 12, 12);
			nav_h->ION_BDSA[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
			continue;
		}
		else if (strstr(lable, "BDSB")){
			nav_h->ION_BDSB[0] = strtonum(buff, 6, 12);
			nav_h->ION_BDSB[1] = strtonum(buff, 6 + 12, 12);
			nav_h->ION_BDSB[2] = strtonum(buff, 6 + 12 + 12, 12);
			nav_h->ION_BDSB[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
			continue;
		}
		else if (strstr(lable, "BDUT")){
			nav_h->BDUT[0] = strtonum(buff, 5, 17);
			nav_h->BDUT[1] = strtonum(buff, 5 + 17, 16);
			nav_h->BDUT[2] = strtonum(buff, 5 + 17 + 16, 7);
			nav_h->BDUT[3] = strtonum(buff, 5 + 17 + 16 + 7, 5);
			continue;
		}
		else if (strstr(lable, "GPUT")){
			nav_h->GPUT[0] = strtonum(buff, 5, 17);
			nav_h->GPUT[1] = strtonum(buff, 5 + 17, 16);
			nav_h->GPUT[2] = strtonum(buff, 5 + 17 + 16, 7);
			nav_h->GPUT[3] = strtonum(buff, 5 + 17 + 16 + 7, 5);
			continue;
		}
		else if (strstr(lable, "LEAP SECONDS")){
			nav_h->leap = (int)strtonum(buff, 4, 2);
		}
		else if (strstr(lable, "END OF HEADER"))
			break;
	}
}

/*Read the body data of file of nav*/
void read_n_b(FILE* fp_nav, pnav_body nav_b)
{
	int i_g = 0;
	char buff[MAXRINEX] = { 0 };
	char flag = { 0 };
	while (fgets(buff, MAXRINEX, fp_nav)){
		int j_g = 0;
		int j_c = 0;
		int j_ga = 0;
		int j_gl = 0;
		strncpy(&flag, buff + 0, 1);
		//GPS SATELLITE
		if (flag == 'G'){
			for (j_g = 0; j_g < 8; j_g++){
				switch (j_g){
				case 0:
					nav_b[i_g].sPRN_BDS = -1;
					nav_b[i_g].sPRN_GAL = -1;
					nav_b[i_g].sPRN_GPS = (int)strtonum(buff, 1, 2);
					nav_b[i_g].TOC_Y = (int)strtonum(buff, 4, 4);
					nav_b[i_g].TOC_M = (int)strtonum(buff, 9, 2);
					nav_b[i_g].TOC_D = (int)strtonum(buff, 12, 2);
					nav_b[i_g].TOC_H = (int)strtonum(buff, 15, 2);
					nav_b[i_g].TOC_Min = (int)strtonum(buff, 18, 2);
					nav_b[i_g].TOC_Sec = strtonum(buff, 21, 2);
					nav_b[i_g].sa0 = strtonum(buff, 23, 19);
					nav_b[i_g].sa1 = strtonum(buff, 23 + 19, 19);
					nav_b[i_g].sa2 = strtonum(buff, 23 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 1:
					nav_b[i_g].IODE = strtonum(buff, 4, 19);
					nav_b[i_g].Crs = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].deltan = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].M0 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 2:
					nav_b[i_g].Cuc = strtonum(buff, 4, 19);
					nav_b[i_g].e = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].Cus = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].sqrtA = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 3:
					nav_b[i_g].TOE = strtonum(buff, 4, 19);
					nav_b[i_g].Cic = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].OMEGA = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].Cis = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 4:
					nav_b[i_g].i0 = strtonum(buff, 4, 19);
					nav_b[i_g].Crc = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].omega = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].deltaomega = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 5:
					nav_b[i_g].IDOT = strtonum(buff, 4, 19);
					nav_b[i_g].L2code = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].GPSweek = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].L2Pflag = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 6:
					nav_b[i_g].sACC = strtonum(buff, 4, 19);
					nav_b[i_g].sHEA = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].TGD = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].IODC = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 7:
					nav_b[i_g].TTN = strtonum(buff, 4, 19);
					nav_b[i_g].fit = strtonum(buff, 4 + 19, 19);
					//nav_b[i_g].spare1 = strtonum(buff, 4 + 19 + 19, 19);
					//nav_b[i_g].spare2 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					break;
				}
			}
			i_g++;
			continue;
		}
		//BDS SATELLITE
		if (flag == 'C'){
			for (j_c = 0; j_c < 8; j_c++){
				switch (j_c){
				case 0:
					nav_b[i_g].sPRN_GPS = -1;
					nav_b[i_g].sPRN_GAL = -1;
					nav_b[i_g].sPRN_BDS = (int)strtonum(buff, 1, 2);
					nav_b[i_g].TOC_Y = (int)strtonum(buff, 4, 4);
					nav_b[i_g].TOC_M = (int)strtonum(buff, 9, 2);
					nav_b[i_g].TOC_D = (int)strtonum(buff, 12, 2);
					nav_b[i_g].TOC_H = (int)strtonum(buff, 15, 2);
					nav_b[i_g].TOC_Min = (int)strtonum(buff, 18, 2);
					nav_b[i_g].TOC_Sec = strtonum(buff, 21, 2);
					nav_b[i_g].sa0 = strtonum(buff, 23, 19);
					nav_b[i_g].sa1 = strtonum(buff, 23 + 19, 19);
					nav_b[i_g].sa2 = strtonum(buff, 23 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 1:
					nav_b[i_g].AODE = strtonum(buff, 4, 19);
					nav_b[i_g].Crs = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].deltan = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].M0 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 2:
					nav_b[i_g].Cuc = strtonum(buff, 4, 19);
					nav_b[i_g].e = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].Cus = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].sqrtA = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 3:
					nav_b[i_g].TOE = strtonum(buff, 4, 19);
					nav_b[i_g].Cic = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].OMEGA = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].Cis = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 4:
					nav_b[i_g].i0 = strtonum(buff, 4, 19);
					nav_b[i_g].Crc = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].omega = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].deltaomega = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 5:
					nav_b[i_g].IDOT = strtonum(buff, 4, 19);
					//nav_b[i_g].L2code = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].BDTweek = strtonum(buff, 4 + 19 + 19, 19);
					//nav_b[i_g].L2Pflag = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 6:
					nav_b[i_g].sACC = strtonum(buff, 4, 19);
					nav_b[i_g].sHEA = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].TGD1 = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].TGD2 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 7:
					//nav_b[i_g].TTN = strtonum(buff, 4, 19);
					nav_b[i_g].AODC = strtonum(buff, 4 + 19, 19);
					//nav_b[i_g].spare1 = strtonum(buff, 4 + 19 + 19, 19);
					//nav_b[i_g].spare2 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					break;
				}
			}
			i_g++;
			continue;
		}
		//GAL SATELLITE
		if (flag == 'E'){
			for (j_ga = 0; j_ga < 8; j_ga++){
				switch (j_ga){
				case 0:
					nav_b[i_g].sPRN_BDS = -1;
					nav_b[i_g].sPRN_GPS = -1;
					nav_b[i_g].sPRN_GAL = (int)strtonum(buff, 1, 2);
					nav_b[i_g].TOC_Y = (int)strtonum(buff, 4, 4);
					nav_b[i_g].TOC_M = (int)strtonum(buff, 9, 2);
					nav_b[i_g].TOC_D = (int)strtonum(buff, 12, 2);
					nav_b[i_g].TOC_H = (int)strtonum(buff, 15, 2);
					nav_b[i_g].TOC_Min = (int)strtonum(buff, 18, 2);
					nav_b[i_g].TOC_Sec = strtonum(buff, 21, 2);
					nav_b[i_g].sa0 = strtonum(buff, 23, 19);
					nav_b[i_g].sa1 = strtonum(buff, 23 + 19, 19);
					nav_b[i_g].sa2 = strtonum(buff, 23 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 1:
					nav_b[i_g].IODE = strtonum(buff, 4, 19);
					nav_b[i_g].Crs = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].deltan = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].M0 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 2:
					nav_b[i_g].Cuc = strtonum(buff, 4, 19);
					nav_b[i_g].e = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].Cus = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].sqrtA = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 3:
					nav_b[i_g].TOE = strtonum(buff, 4, 19);
					nav_b[i_g].Cic = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].OMEGA = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].Cis = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 4:
					nav_b[i_g].i0 = strtonum(buff, 4, 19);
					nav_b[i_g].Crc = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].omega = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].deltaomega = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 5:
					nav_b[i_g].IDOT = strtonum(buff, 4, 19);
					//nav_b[i_g].L2code = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].GALweek = strtonum(buff, 4 + 19 + 19, 19);
					//nav_b[i_g].L2Pflag = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 6:
					nav_b[i_g].sACC = strtonum(buff, 4, 19);
					nav_b[i_g].sHEA = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].BGDa = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].BGDb = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 7:
					//nav_b[i_g].TTN = strtonum(buff, 4, 19);
					//nav_b[i_g].fit = strtonum(buff, 4 + 19, 19);
					//nav_b[i_g].spare1 = strtonum(buff, 4 + 19 + 19, 19);
					//nav_b[i_g].spare2 = strtonum(buff, 4 + 19 + 19 + 19, 19);
					break;
				}
			}
			i_g++;
			continue;
		}
		//GLO SATELLITE
		if (flag == 'R'){
			for (j_gl = 0; j_gl < 4; j_gl++){
				switch (j_gl){
				case 0:
					nav_b[i_g].sPRN_BDS = -1;
					nav_b[i_g].sPRN_GPS = -1;
					nav_b[i_g].sPRN_GAL = -1;
					nav_b[i_g].sPRN_GLO = (int)strtonum(buff, 1, 2);
					nav_b[i_g].TOC_Y = (int)strtonum(buff, 4, 4);
					nav_b[i_g].TOC_M = (int)strtonum(buff, 9, 2);
					nav_b[i_g].TOC_D = (int)strtonum(buff, 12, 2);
					nav_b[i_g].TOC_H = (int)strtonum(buff, 15, 2);
					nav_b[i_g].TOC_Min = (int)strtonum(buff, 18, 2);
					nav_b[i_g].TOC_Sec = strtonum(buff, 21, 2);
					nav_b[i_g].sa0 = strtonum(buff, 23, 19);
					nav_b[i_g].sa1 = strtonum(buff, 23 + 19, 19);
					nav_b[i_g].Dos = strtonum(buff, 23 + 19 + 19, 19);

					nav_b[i_g].TOE = JDUTC2GPST(
						UTCTime2JD(nav_b[i_g].TOC_Y, nav_b[i_g].TOC_M, nav_b[i_g].TOC_D,
							nav_b[i_g].TOC_H, nav_b[i_g].TOC_Min, nav_b[i_g].TOC_Sec)
					);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 1:
					nav_b[i_g].SatX = strtonum(buff, 4, 19);
					nav_b[i_g].SatXv = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].SatXa = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].sHEA = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 2:
					nav_b[i_g].SatY = strtonum(buff, 4, 19);
					nav_b[i_g].SatYv = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].SatYa = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].FreN = strtonum(buff, 4 + 19 + 19 + 19, 19);
					fgets(buff, MAXRINEX, fp_nav);
					break;
				case 3:
					nav_b[i_g].SatZ = strtonum(buff, 4, 19);
					nav_b[i_g].SatZv = strtonum(buff, 4 + 19, 19);
					nav_b[i_g].SatZa = strtonum(buff, 4 + 19 + 19, 19);
					nav_b[i_g].AOO = strtonum(buff, 4 + 19 + 19 + 19, 19);
					break;
				}
			}
			i_g++;
			continue;
		}
	}
}

/* -------------------------- Read the file of obs -------------------------- */
/* -------------------------------------------------------------------------- */
/// @brief get the total number of epoch of obs
/// @param fp_obs the file pointer of obs
/// @return epoch number
/* -------------------------------------------------------------------------- */
int get_epochnum(FILE* fp_obs)
{
	int n = 0;
	int satnum = 0;
	char flag;
	char buff[MAXRINEX];
	while (fgets(buff, MAXRINEX, fp_obs)){
		satnum = (int)strtonum(buff, 33, 2);
		strncpy(&flag, buff + 0, 1);
		if (flag == '>'){
			n++;
		}
	}
	return n;
}

/*Read the header data of file of obs*/
void read_o_h(FILE* fp_obs, pobs_head obs_h)
{
	char buff[MAXRINEX] = { 0 };
	char flag = { 0 };
	char* lable = buff + 60;
	int i = 0;
	int j = 0;

	obs_h->interval = 30;
	obs_h->f_y = obs_h->f_m = obs_h->f_d = obs_h->f_h = obs_h->f_min = obs_h->f_sec = 0;
	obs_h->l_y = obs_h->l_m = obs_h->l_d = obs_h->l_h = obs_h->l_min = obs_h->l_sec = 0;

	while (fgets(buff, MAXRINEX, fp_obs)){
		if (strstr(lable, "RINEX VERSION / TYPE")){
			obs_h->ver = strtonum(buff, 0, 9);
			strncpy(obs_h->type, buff + 20, 30);
			continue;
		}
		else if (strstr(lable, "APPROX POSITION XYZ")){
			obs_h->apX = strtonum(buff, 0, 14);
			obs_h->apY = strtonum(buff, 0 + 14, 14);
			obs_h->apZ = strtonum(buff, 0 + 14 + 14, 14);
			continue;
		}
		else if (strstr(lable, "ANTENNA: DELTA H/E/N")){
			obs_h->ANTH = strtonum(buff, 0, 14);
			obs_h->ANTdeltaE = strtonum(buff, 14, 14);
			obs_h->ANTdeltaN = strtonum(buff, 14 + 14, 14);
			continue;
		}
		else if (strstr(lable, "SYS / # / OBS TYPES")){
			char flag = { 0 };
			strncpy(&flag, buff + 0, 1);
			if (flag == 'G'){
				obs_h->obstypenum_gps = (int)strtonum(buff, 4, 2);
				if (obs_h->obstypenum_gps <= 13){
					for (i = 0; i < obs_h->obstypenum_gps; i++){
						obs_h->obscode_gps[i + 1] = Type2Code(i, buff);
					}
				}
				else if (obs_h->obstypenum_gps > 13){
					for (i = 0; i < 13; i++){
						obs_h->obscode_gps[i] = Type2Code(i, buff);
					}
					fgets(buff, MAXRINEX, fp_obs);
					for (i = 0; i < obs_h->obstypenum_gps - 13; i++){
						obs_h->obscode_gps[i + 13] = Type2Code(i, buff);
					}
				}continue;
			}
			else if (flag == 'C'){
				obs_h->obstypenum_bds = (int)strtonum(buff, 4, 2);
				if (obs_h->obstypenum_bds <= 13){
					for (i = 0; i < obs_h->obstypenum_bds; i++){
						obs_h->obscode_bds[i] = Type2Code(i, buff);
					}
				}
				else if (obs_h->obstypenum_bds > 13){
					for (i = 0; i < 13; i++){
						obs_h->obscode_bds[i] = Type2Code(i, buff);
					}
					fgets(buff, MAXRINEX, fp_obs);
					for (i = 0; i < obs_h->obstypenum_bds - 13; i++){
						obs_h->obscode_bds[i + 13] = Type2Code(i, buff);
					}
				}continue;
			}
			else if (flag == 'E'){
				obs_h->obstypenum_gal = (int)strtonum(buff, 4, 2);
				if (obs_h->obstypenum_gal <= 13){
					for (i = 0; i < obs_h->obstypenum_gal; i++){
						obs_h->obscode_gal[i] = Type2Code(i, buff);
					}
				}
				else if (obs_h->obstypenum_gal > 13){
					for (i = 0; i < 13; i++){
						obs_h->obscode_gal[i] = Type2Code(i, buff);
					}
					fgets(buff, MAXRINEX, fp_obs);
					for (i = 0; i < obs_h->obstypenum_gal - 13; i++){
						obs_h->obscode_gal[i + 13] = Type2Code(i, buff);
					}
				}continue;
			}
			else if (flag == 'R'){
				obs_h->obstypenum_glo = (int)strtonum(buff, 4, 2);
				if (obs_h->obstypenum_glo <= 13){
					for (i = 0; i < obs_h->obstypenum_glo; i++){
						obs_h->obscode_glo[i] = Type2Code(i, buff);
					}
				}
				else if (obs_h->obstypenum_glo > 13){
					for (i = 0; i < 13; i++){
						obs_h->obscode_glo[i] = Type2Code(i, buff);
					}
					fgets(buff, MAXRINEX, fp_obs);
					for (i = 0; i < obs_h->obstypenum_glo - 13; i++){
						obs_h->obscode_glo[i + 13] = Type2Code(i, buff);
					}
				}continue;
			}continue;
		}
		else if (strstr(lable, "INTERVAL")){
			obs_h->interval = strtonum(buff, 0, 10);
			continue;
		}
		else if (strstr(lable, "TIME OF FIRST OBS")){
			obs_h->f_y = (int)strtonum(buff, 2, 4);
			obs_h->f_m = (int)strtonum(buff, 2 + 6, 4);
			obs_h->f_d = (int)strtonum(buff, 2 + 6 + 6, 4);
			obs_h->f_h = (int)strtonum(buff, 2 + 6 + 6 + 6, 4);
			obs_h->f_min = (int)strtonum(buff, 2 + 6 + 6 + 6 + 6, 4);
			obs_h->f_sec = strtonum(buff, 2 + 6 + 6 + 6 + 6 + 6, 9);
			strncpy(obs_h->tsys, buff + 6 + 6 + 6 + 6 + 6 + 18, 3);
			continue;
		}
		else if (strstr(lable, "TIME OF LAST OBS")){
			obs_h->l_y = (int)strtonum(buff, 2, 4);
			obs_h->l_m = (int)strtonum(buff, 2 + 6, 4);
			obs_h->l_d = (int)strtonum(buff, 2 + 6 + 6, 4);
			obs_h->l_h = (int)strtonum(buff, 2 + 6 + 6 + 6, 4);
			obs_h->l_min = (int)strtonum(buff, 2 + 6 + 6 + 6 + 6, 4);
			obs_h->l_sec = strtonum(buff, 2 + 6 + 6 + 6 + 6 + 6, 9);
			continue;
		}
		else if (strstr(lable, "END OF HEADER")){
			break;
		}
	}
}

/*Read the body data of file of obs*/
void read_o_eb(FILE* fp_obs, pobs_head obs_h, pobs_epoch obs_e, pobs_body obs_b)
{
	initobs_e(obs_e, obs_b);
	char buff[MAXRINEX] = { 0 };
	char flag = { 0 };
	while (fgets(buff, MAXRINEX, fp_obs)) {
		strncpy(&flag, buff + 0, 1);
		if (flag == '>') {
			int j_g = 0;   int k_g = 0;
			int j_c = 0;   int k_c = 0;
			int j_ga = 0;	int k_ga = 0;
			int j_gl = 0;	int k_gl = 0;

			obs_e->gps_num = 0;
			obs_e->bds_num = 0;
			obs_e->gal_num = 0;
			obs_e->glo_num = 0;

			obs_e->y = (int)strtonum(buff, 2, 4);
			obs_e->m = (int)strtonum(buff, 7, 2);
			obs_e->d = (int)strtonum(buff, 10, 2);
			obs_e->h = (int)strtonum(buff, 13, 2);
			obs_e->min = (int)strtonum(buff, 16, 2);
			obs_e->sec = strtonum(buff, 19, 10);
			obs_e->p_flag = (int)strtonum(buff, 31, 1);
			obs_e->sat_num = strtonum(buff, 33, 3);
			strncpy(&flag, buff + 0, 1);

			memset(obs_e->sPRN, 0, sizeof(obs_e->sPRN));
			memset(obs_e->sPRN_GPS, 0, sizeof(obs_e->sPRN_GPS));
			memset(obs_e->sPRN_BDS, 0, sizeof(obs_e->sPRN_BDS));
			memset(obs_e->sPRN_GAL, 0, sizeof(obs_e->sPRN_GAL));
			memset(obs_e->sPRN_GLO, 0, sizeof(obs_e->sPRN_GLO));
			memset(obs_b->obs_gps, 0, sizeof(obs_b->obs_gps));
			memset(obs_b->obs_bds, 0, sizeof(obs_b->obs_bds));
			memset(obs_b->obs_gal, 0, sizeof(obs_b->obs_gal));
			memset(obs_b->obs_glo, 0, sizeof(obs_b->obs_glo));

			for (int i = 0; i < obs_e->sat_num; i++) {
				if (flag == 'G') {
					obs_e->sPRN[i] = strtonum(buff, 1, 2);
					obs_e->sPRN_GPS[j_g] = obs_e->sPRN[i];
					for (k_g = 0; k_g < obs_h->obstypenum_gps; k_g++) {
						obs_b->obs_gps[j_g][k_g] = strtonum(buff, 3 + 16 * k_g, 14);
					}
					obs_e->gps_num++; j_g++;
					fgets(buff, MAXRINEX, fp_obs);
					strncpy(&flag, buff + 0, 1);
				}
				else if (flag == 'C') {
					obs_e->sPRN[i] = strtonum(buff, 1, 2);
					obs_e->sPRN_BDS[j_c] = obs_e->sPRN[i];
					for (k_c = 0; k_c < obs_h->obstypenum_bds; k_c++) {
						obs_b->obs_bds[j_c][k_c] = strtonum(buff, 3 + 16 * k_c, 14);
					}
					obs_e->bds_num++; j_c++;
					fgets(buff, MAXRINEX, fp_obs);
					strncpy(&flag, buff + 0, 1);
				}
				else if (flag == 'E') {
					obs_e->sPRN[i] = strtonum(buff, 1, 2);
					obs_e->sPRN_GAL[j_ga] = obs_e->sPRN[i];
					for (k_ga = 0; k_ga < obs_h->obstypenum_gal; k_ga++) {
						obs_b->obs_gal[j_ga][k_ga] = strtonum(buff, 3 + 16 * k_ga, 14);
					}
					obs_e->gal_num++; j_ga++;
					fgets(buff, MAXRINEX, fp_obs);
					strncpy(&flag, buff + 0, 1);
				}
				else if (flag == 'R') {
					obs_e->sPRN[i] = strtonum(buff, 1, 2);
					obs_e->sPRN_GLO[j_gl] = obs_e->sPRN[i];
					for (k_gl = 0; k_gl < obs_h->obstypenum_glo; k_gl++) {
						obs_b->obs_glo[j_gl][k_gl] = strtonum(buff, 3 + 16 * k_gl, 14);
					}
					obs_e->glo_num++; j_gl++;
					fgets(buff, MAXRINEX, fp_obs);
					strncpy(&flag, buff + 0, 1);
				}
				else {
					fgets(buff, MAXRINEX, fp_obs);
					strncpy(&flag, buff + 0, 1);
				}
			}
		}break;
	}
}

/*Obatain the intergral term of acceleraction of each component*/
void pz90deq(double X[6], double K[6], double acc[3])
{
	double r = sqrt(pow(X[0], 2) + pow(X[1], 2) + pow(X[2], 2));
	double coef0 = -GM / pow(r, 3);
	double coef1 = 1.5 * C20 * (GM * pow(a, 2) / pow(r, 5));

	K[0] = X[3]; K[1] = X[4]; K[2] = X[5];
	K[3] =
		coef0 * X[0] +
		coef1 * (1 - 5 * pow((X[2] / r), 2)) * X[0] +
		pow(Earth_e, 2) * X[0] +
		2 * Earth_e * X[4] +
		acc[0];
	K[4] =
		coef0 * X[1] +
		coef1 * (1 - 5 * pow((X[2] / r), 2)) * X[1] +
		pow(Earth_e, 2) * X[1] -
		2 * Earth_e * X[3] +
		acc[1];
	K[5] =
		coef0 * X[2] +
		coef1 * (3 - 5 * pow((X[2] / r), 2)) * X[2] +
		acc[2];
}

/*Construct the RK-4 method*/
void pz90pos(double tstep, double X[6], double acc[3])
{
	double K1[6], K2[6], K3[6], K4[6], W[6];

	pz90deq(X, K1, acc); for (int i = 0; i < 6; i++) W[i] = X[i] + K1[i] * tstep / 2.0;
	pz90deq(W, K2, acc); for (int i = 0; i < 6; i++) W[i] = X[i] + K2[i] * tstep / 2.0;
	pz90deq(W, K3, acc); for (int i = 0; i < 6; i++) W[i] = X[i] + K3[i] * tstep;
	pz90deq(W, K4, acc);
	for (int i = 0; i < 6; i++) X[i] += (K1[i] + 2.0 * K2[i] + 2.0 * K3[i] + K4[i]) * tstep / 6.0;
}

/*Calculate the satellite position of GLONASS on this epoch*/
pos_ts glo_pos(int best_epoch, double Weeksec,
				pnav_body nav_b, pobs_head obs_h, pos_ts pos_t)
{
	double X[6], acc[3]; double R = 0.0;
	double tdist = Weeksec - pos_t.delta_t - nav_b[best_epoch].TOE, tstep = 0.0;
	pos_t.delta_clk = -nav_b[best_epoch].sa0 + nav_b[best_epoch].sa1 * tdist;

	X[0] = nav_b[best_epoch].SatX * 1e3;
	X[1] = nav_b[best_epoch].SatY * 1e3;
	X[2] = nav_b[best_epoch].SatZ * 1e3;//Position

	X[3] = nav_b[best_epoch].SatXv * 1e3;
	X[4] = nav_b[best_epoch].SatYv * 1e3;
	X[5] = nav_b[best_epoch].SatZv * 1e3;//Velocity

	acc[0] = nav_b[best_epoch].SatXa * 1e3;
	acc[1] = nav_b[best_epoch].SatYa * 1e3;
	acc[2] = nav_b[best_epoch].SatZa * 1e3;//Acclerate

	for (tstep = tdist < 0.0 ? TSTEP : -TSTEP; fabs(tdist) > 1.0e-9; tdist += tstep) {
		if (fabs(tdist) < TSTEP) tstep = -tdist;
		pz90pos(tstep, X, acc);
	}

	X[0] = -0.47 + (X[0] * 1 + X[1] * 1.728e-6 + X[2] * -0.017e-6) * (1 + 22e-9);
	X[1] = -0.51 + (X[0] * 1.728e-6 + X[1] * 1 + X[2] * -0.076e-6) * (1 + 22e-9);
	X[2] = -1.56 + (X[0] * 0.0178e-6 + X[1] * -0.076e-6 + X[2] * 1) * (1 + 22e-9);//PZ90 Convert to WGS-84

	pos_t.X = X[0];
	pos_t.Y = X[1];
	pos_t.Z = X[2];

	R = sqrt(pow(pos_t.X - obs_h->apX, 2) + pow(pos_t.Y - obs_h->apY, 2) + pow(pos_t.Z - obs_h->apZ, 2));
	pos_t.deltat = pos_t.delta_t;
	pos_t.delta_t = R / C_V + pos_t.delta_clk;

	return pos_t;
}

/*Calculate the satellite position of other systems on this epoch*/
pos_ts sat_pos(int sPRN, int best_epoch, double	Weeksec, int gnsscode,
				pnav_body nav_b, pobs_head obs_h, pos_ts pos_t)
{
	double T_S = Weeksec - pos_t.delta_t;
	double n_0 = sqrt(GM) / pow(nav_b[best_epoch].sqrtA, 3);
	double n = n_0 + nav_b[best_epoch].deltan;
	double tk;
	if (gnsscode == BDS) tk = T_S - nav_b[best_epoch].TOE - 14;
	else tk = T_S - nav_b[best_epoch].TOE;
	
	if (tk > 32400)tk -= 604800;
	else if (tk < -32400)tk += 604800;

	double Ms = nav_b[best_epoch].M0 + n * tk;

	double Es = Ms, E0;
	do
	{
		E0 = Es;
		Es = Ms + nav_b[best_epoch].e * sin(Es);
	} while (fabs(Es - E0) > 1.0e-10);

	double cosfs = (cos(Es) - nav_b[best_epoch].e) / (1 - nav_b[best_epoch].e * cos(Es));
	double sinfs = (sqrt(1 - pow(nav_b[best_epoch].e, 2)) * sin(Es)) / (1 - nav_b[best_epoch].e * cos(Es));
	double fs = atan2(sinfs, cosfs);
	double u0 = fs + nav_b[best_epoch].omega;

	double epsilon_u = nav_b[best_epoch].Cus * sin(2 * u0) + nav_b[best_epoch].Cuc * cos(2 * u0);
	double epsilon_r = nav_b[best_epoch].Crs * sin(2 * u0) + nav_b[best_epoch].Crc * cos(2 * u0);
	double epsilon_i = nav_b[best_epoch].Cis * sin(2 * u0) + nav_b[best_epoch].Cic * cos(2 * u0);

	double u = u0 + epsilon_u;
	double r = pow(nav_b[best_epoch].sqrtA, 2) * (1 - nav_b[best_epoch].e * cos(Es)) + epsilon_r;
	double i = nav_b[best_epoch].i0 + epsilon_i + nav_b[best_epoch].IDOT * tk;

	double x = r * cos(u);
	double y = r * sin(u);

	double l, X, Y, Z;
	if (gnsscode == BDS){
		if (sPRN > 5 && sPRN < 59) //BDS IGSO & MEO Satellites
		{
			l = nav_b[best_epoch].OMEGA + (nav_b[best_epoch].deltaomega - Earth_e) * tk - Earth_e * nav_b[best_epoch].TOE;
			X = x * cos(l) - y * cos(i) * sin(l);
			Y = x * sin(l) + y * cos(i) * cos(l);
			Z =              y * sin(i);
		}
		else //BDS GEO Satellites
		{
			l = nav_b[best_epoch].OMEGA + nav_b[best_epoch].deltaomega * tk - Earth_e * nav_b[best_epoch].TOE;
			X = x * cos(l) - y * cos(i) * sin(l);
			Y = x * sin(l) + y * cos(i) * cos(l);
			Z = y * sin(i);

			double f = deg2rad(-5);
			double p = Earth_e * tk;

			X = X *  cos(p) + Y * sin(p) * cos(f) + Z * sin(p) * sin(f);
			Y = X * -sin(p) + Y * cos(p) * cos(f) + Z * cos(p) * sin(f);
			Z = Y * -sin(f) + Z * cos(f);
		}
	}
	else{
		l = nav_b[best_epoch].OMEGA + (nav_b[best_epoch].deltaomega - Earth_e) * tk - Earth_e * nav_b[best_epoch].TOE;
		X = x * cos(l) - y * cos(i) * sin(l);
		Y = x * sin(l) + y * cos(i) * cos(l);
		Z = y * sin(i);
	}
	pos_t.X =  cos(Earth_e * pos_t.delta_t) * X + sin(Earth_e * pos_t.delta_t) * Y;
	pos_t.Y = -sin(Earth_e * pos_t.delta_t) * X + cos(Earth_e * pos_t.delta_t) * Y;
	pos_t.Z = Z;//Correction of earth rotation

	double TGD;
	if (gnsscode == GPS) TGD = nav_b[best_epoch].TGD;
	else if (gnsscode == GAL) TGD = nav_b[best_epoch].BGDa;
	else if (gnsscode == BDS) TGD = 0;

	double R = sqrt(pow(pos_t.X - obs_h->apX, 2) + pow(pos_t.Y - obs_h->apY, 2) + pow(pos_t.Z - obs_h->apZ, 2));
	double rela = 2 * sqrt(GM) * nav_b[best_epoch].e * nav_b[best_epoch].sqrtA * sin(Es) / pow(C_V, 2);//Relativistic effect
	pos_t.delta_clk = nav_b[best_epoch].sa0 + nav_b[best_epoch].sa1 * tk + nav_b[best_epoch].sa2 * pow(tk, 2) - rela - TGD;
	pos_t.deltat = pos_t.delta_t;
	pos_t.delta_t = R / C_V + pos_t.delta_clk;

	return pos_t;
}

/* -------------------------------------------------------------------------- */
/// @brief Calculate the position of satellite in the ECEF coordinate system by the broadcast ephemeris and epoch information
/// @param obs_h Observation header data
/// @param obs_e Observation epoch data
/// @param obs_b Observation data
/// @param nav_b Navigation data
/// @param res_file The file path of result file of satellite position
/// @param station Prior information about station location
/// @param gnsscode GNSS system code
/// @param satnum The total number of satellite of designated satellite system
/// @return 1 refer OK 
/* -------------------------------------------------------------------------- */
int sat_pos_cal(pobs_head obs_h, pobs_epoch obs_e, pobs_body obs_b,
				pnav_body nav_b,
				FILE* res_file, stations station,
				int gnsscode, int satnum)
{
	//the beginning second of observation
	double beginsec = Time2GPST(obs_h->f_y, obs_h->f_m, obs_h->f_d, obs_h->f_h, obs_h->f_min, obs_h->f_sec);
	//the ending second of observation
	double endinsec = Time2GPST(obs_h->l_y, obs_h->l_m, obs_h->l_d, obs_h->l_h, obs_h->l_min, obs_h->l_sec);

	blhs blh = { 0 }; blh2enu enu = { 0 };
	rahcal rah = { 0 }; pos_ts pos_t = { 0 };
	xyz2blh tem1 = { 0 }; blh2enu tem2 = { 0 }; rahcal tem3 = { 0 };

	int y = obs_e->y; int m = obs_e->m; int d = obs_e->d;
	double h = obs_e->h; int min = obs_e->min; double sec = obs_e->sec;

	double Weeksec = Time2GPST(y, m, d, h, min, sec);
	int epochcount = round((Weeksec - beginsec) / obs_h->interval) + 1;
	fprintf(res_file, "\n>%04d %04d %02d %02d %02d %02d %07.04f"
		, epochcount, obs_e->y, obs_e->m, obs_e->d, obs_e->h, obs_e->min, obs_e->sec);
	int sat_num = 0, sPRN = 0, SIGN = 0, PERS = 0;
	double detat_toc;
	//Check the GNSS and assign the satellite number
	if (gnsscode == GPS)sat_num = obs_e->gps_num;
	else if (gnsscode == GAL)sat_num = obs_e->gal_num;
	else if (gnsscode == BDS)sat_num = obs_e->bds_num;
	else if (gnsscode == GLO)sat_num = obs_e->glo_num;

	for (int j = 0; j < sat_num; j++) {
		if (gnsscode == GPS) {
			sPRN = obs_e->sPRN_GPS[j]; SIGN = GPS;
			PERS = obs_b->obs_gps[j][Code2Type(C1, obs_h->obstypenum_gps, obs_h->obscode_gps)] / C_V;
		}
		else if (gnsscode == GAL) {
			sPRN = obs_e->sPRN_GAL[j]; SIGN = GAL;
			PERS = obs_b->obs_gal[j][Code2Type(C1, obs_h->obstypenum_gal, obs_h->obscode_gal)] / C_V;
		}
		else if (gnsscode == BDS) {
			sPRN = obs_e->sPRN_BDS[j]; SIGN = BDS;
			PERS = obs_b->obs_bds[j][Code2Type(C2, obs_h->obstypenum_bds, obs_h->obscode_bds)] / C_V;
		}
		else if (gnsscode == GLO) {
			sPRN = obs_e->sPRN_GLO[j]; SIGN = GLO;
			PERS = obs_b->obs_glo[j][Code2Type(C1, obs_h->obstypenum_glo, obs_h->obscode_glo)] / C_V;
		}

		int best_epoch = select_epoch(Weeksec, sPRN, nav_b, satnum, SIGN);
		if (best_epoch == -1)//when the sPRN is not exist function will return -1
			break;
		if (SIGN == BDS) detat_toc = Weeksec - nav_b[best_epoch].TOE - 14;
		else detat_toc = Weeksec - nav_b[best_epoch].TOE;

		//Iterative approximate propagation time
		//Exclude GLONASS
		if (SIGN == GLO) {
			pos_t.delta_t = PERS -
				station.delta_TR +
				nav_b[best_epoch].sa0 +
				nav_b[best_epoch].sa1 * detat_toc;
			pos_t.deltat = 0.0;

			while (fabs(pos_t.delta_t - pos_t.deltat) > 1.0e-9){
				pos_t = glo_pos(best_epoch, Weeksec, nav_b, obs_h, pos_t);
			}
		}
		else {
			pos_t.delta_t = PERS -
				station.delta_TR +
				nav_b[best_epoch].sa0 +
				nav_b[best_epoch].sa1 * detat_toc +
				nav_b[best_epoch].sa2 * pow(detat_toc, 2);
			pos_t.deltat = 0.0;
			while (fabs(pos_t.delta_t - pos_t.deltat) > 1.0e-9) {
				pos_t = sat_pos(sPRN, best_epoch, Weeksec, gnsscode, nav_b, obs_h, pos_t);
			}
		}
		//Satellite blh position calculation
		tem1 = XYZ2BLH(tem1, pos_t.X, pos_t.Y, pos_t.Z);
		blh.B = rad2deg(tem1.B);
		blh.L = rad2deg(tem1.L);
		blh.H = tem1.H;

		double deltax = pos_t.X - obs_h->apX;
		double deltay = pos_t.Y - obs_h->apY;
		double deltaz = pos_t.Z - obs_h->apZ;

		tem2 = BLH2ENU(tem2, station.B, station.L, deltax, deltay, deltaz);
		enu.E = tem2.E;
		enu.N = tem2.N;
		enu.U = tem2.U;
		//Satellite elevation Angle calculation
		tem3 = RAHCAL(tem3, enu.E, enu.N, enu.U);
		rah.R = tem3.R;
		rah.A = rad2deg(tem3.A);
		rah.H = rad2deg(tem3.H);
		if (blh.H < 0 || rah.H < 10 || nav_b[best_epoch].sHEA != 0) {
			continue;
		}
		else {
			if (SIGN == GPS) {
				fprintf(res_file, "\nG %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
					, sPRN, pos_t.X, pos_t.Y, pos_t.Z
					, obs_b->obs_gps[j][Code2Type(C1, obs_h->obstypenum_gps, obs_h->obscode_gps)]
					, obs_b->obs_gps[j][Code2Type(C2, obs_h->obstypenum_gps, obs_h->obscode_gps)]
					, rah.H, pos_t.delta_clk);//GPS satellite pos output
			}
			else if (SIGN == GAL) {
				fprintf(res_file, "\nE %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
					, sPRN, pos_t.X, pos_t.Y, pos_t.Z
					, obs_b->obs_gal[j][Code2Type(C1, obs_h->obstypenum_gal, obs_h->obscode_gal)]
					, obs_b->obs_gal[j][Code2Type(C6, obs_h->obstypenum_gal, obs_h->obscode_gal)]
					, rah.H, pos_t.delta_clk);//Galileo satellite pos output
			}
			else if (SIGN == BDS) {
				if (sPRN >= 19) {
					fprintf(res_file, "\nCC%02d| %15.05f %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
						, sPRN, pos_t.X, pos_t.Y, pos_t.Z
						, obs_b->obs_bds[j][Code2Type(C2, obs_h->obstypenum_bds, obs_h->obscode_bds)]
						, obs_b->obs_bds[j][Code2Type(C7, obs_h->obstypenum_bds, obs_h->obscode_bds)]
						, rah.H, pos_t.delta_clk);//BDS-3 satellite pos output
				}
				else {
					fprintf(res_file, "\nCB%02d| %15.05f %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
						, sPRN, pos_t.X, pos_t.Y, pos_t.Z
						, obs_b->obs_bds[j][Code2Type(C2, obs_h->obstypenum_bds, obs_h->obscode_bds)]
						, obs_b->obs_bds[j][Code2Type(C7, obs_h->obstypenum_bds, obs_h->obscode_bds)]
						, rah.H, pos_t.delta_clk);//BDS-2 satellite pos output
				}
			}
			else if (SIGN == GLO) {
				fprintf(res_file, "\nR %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
					, sPRN, pos_t.X, pos_t.Y, pos_t.Z
					, obs_b->obs_glo[j][Code2Type(C1, obs_h->obstypenum_glo, obs_h->obscode_glo)]
					, obs_b->obs_glo[j][Code2Type(C2, obs_h->obstypenum_glo, obs_h->obscode_glo)]
					, rah.H, pos_t.delta_clk);//Galileo satellite pos output
			}
		}
	}return 1;
}
/* -------------------------------------------------------------------------- */
/// @brief The entry function of full .dll package,
/// @param nav_path The RINEX navigation file's path
/// @param obs_path The RINEX observation file's path
/// @param res_path The Satellite output file's path
/// @param gnsscode The GNSS position you want to calculate
/// @return 0 refer complete solution; -1 refer fail to complete solution
/// @return > 0 refer partlt complete solution
/* -------------------------------------------------------------------------- */
double Start(char nav_path[260], char obs_path[260], char res_path[260], int gnsscode)
{
	int satnum, epochunum, result = 0;
	pos_ts pos_t = { 0 };
	xyz2blh tem2 = { 0 };
	stations station = { 0 };
	time_t gen_time; time(&gen_time);

	pnav_head nav_h = NULL;
	pnav_body nav_b = NULL;
	pobs_head obs_h = NULL;
	pobs_body obs_b = NULL;
	pobs_epoch obs_e = NULL;

	FILE* fp_nav = fopen(nav_path, "r");
	satnum = getsatnum(fp_nav); rewind(fp_nav);
	nav_h = (pnav_head)malloc(sizeof(nav_head));
	nav_b = (pnav_body)malloc(sizeof(nav_body) * (satnum));
	if (nav_h && nav_b){
		read_n_h(fp_nav, nav_h); read_n_b(fp_nav, nav_b);
	}
	fclose(fp_nav);

	FILE* fp_obs = fopen(obs_path, "r");
	epochunum = get_epochnum(fp_obs);
	rewind(fp_obs);
	obs_h = (pobs_head)malloc(sizeof(obs_head));
	obs_e = (pobs_epoch)malloc(sizeof(obs_epoch));
	obs_b = (pobs_body)malloc(sizeof(obs_body));
	if (obs_h && obs_e && obs_b) {
		read_o_h(fp_obs, obs_h);

		tem2 = XYZ2BLH(tem2, obs_h->apX, obs_h->apY, obs_h->apZ);
		station.B = tem2.B; station.L = tem2.L; station.H = tem2.H;
		//Out put the header of solution file
		FILE* result_file_clear = fopen(res_path, "w");
		fclose(result_file_clear);
		FILE* result_file = fopen(res_path, "a+");
		fprintf(result_file, "@ GENERATE PROGRAM   : KNZ_GeoTrackLab ver1.5.1\n");
		fprintf(result_file, "@ GENERATE TYPE      : Satellite  Position\n");
		fprintf(result_file, "@ GENERATE TIME      : %s", ctime(&gen_time));
		fprintf(result_file, "@ OBS FILE PATH      : %s\n", obs_path);
		fprintf(result_file, "@ NAV FILE PATH      : %s\n", nav_path);
		fprintf(result_file, "@ TIME OF FIRST OBS  : %4d %02d %02d %02d %02d %07.4f\n"
			, obs_h->f_y, obs_h->f_m, obs_h->f_d, obs_h->f_h, obs_h->f_min, obs_h->f_sec);
		fprintf(result_file, "@ TIME OF LAST OBS   : %4d %02d %02d %02d %02d %07.4f\n"
			, obs_h->l_y, obs_h->l_m, obs_h->l_d, obs_h->l_h, obs_h->l_min, obs_h->l_sec);
		fprintf(result_file, "@ APPROX POSITION XYZ: %13.04f%13.04f%13.04f\n@ APPROX POSITION BLH:  %12.07f %12.07f %12.07f\n"
			, obs_h->apX, obs_h->apY, obs_h->apZ
			, station.B, station.L, station.H);
		fprintf(result_file, "END OF HEADER\n");
		//Begin to calculate
		for (int i = 0; i < epochunum; i++){
			read_o_eb(fp_obs, obs_h, obs_e, obs_b);
			result += sat_pos_cal(obs_h, obs_e, obs_b, nav_b,
								result_file, station,
								gnsscode, satnum);
			fprintf(result_file, "\n");
		}
		freeobs_e(obs_e, obs_b);
		fprintf(result_file, "\nEND"); 
		fclose(result_file);
		return epochunum - result;
	}
}
