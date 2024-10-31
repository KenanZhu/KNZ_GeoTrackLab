#include "brdm2pos.h"

#define	MAXTOE_GPS		7200.0
#define	MAXTOE_BDS		21600.0
#define	MAXTOE_GAL		14400.0
#define	MAXTOE_GLO		1800.0
#define	MAXTOE_SBS		360.0
using namespace std;
/**
 * Find the nearest obs epoch with boardcast.
 * 
 * \param SecofWeek: SecofWeek second of week of obs epoch time
 * \param sPRN: sPRN the satellite PRN which need to match
 * \param nav_b: Nav data file structure
 * \param satnum: Total number of boardcast satellite 
 * \param syscode: GNSS code
 * \return the absolute epoch number of the best epoch
 *		   -1 ,no match satellite
 */
int select_epoch(double SecofWeek, int sPRN, pnav_body nav_b, int satnum, int syscode)
{
    int best_epoch = -1;
    double min;//Initialize the minimum value
    double Min;

    if (syscode == GPS){//GPS
        min = MAXTOE_GPS;
        for (int i = 0; i < satnum; i++){
            if (sPRN == nav_b[i].sPRN_GPS && nav_b[i].sHEA == 0) {
                Min = fabs(SecofWeek - nav_b[i].TOE);
                if (Min <= min){
                    best_epoch = i;
                    min = Min;
                }
            }
        }return best_epoch;
    }
    else if (syscode == BDS){//BeiDou
        min = MAXTOE_BDS;
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
    else if (syscode == GAL){//Galileo
        min = MAXTOE_GAL;
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
    else if (syscode == GLO){//GLONASS
        min = MAXTOE_GLO;
        for (int i = 0; i < satnum; i++){
            if (sPRN == nav_b[i].sPRN_GLO){
                Min = fabs(SecofWeek - nav_b[i].TOE);
                if (Min <= min)
                {
                    best_epoch = i;
                    min = Min;
                }
            }
        }return best_epoch;
    }return best_epoch;
}
/**
 * Match the observation type(char*) with the code type(int).
 * 
 * \param Lxcodeindex: Frequency X observation type(char*)
 * \param code_original: The observation will matched
 * \param freq: Observation frequency
 * \return code type
 */
static int findtype(const char Lxcodeindex[60], char code_original[4], int freq)
{
    int code_return = 0;
    char code_contrast[4] = "/0";

    for (int j = 0; j < (strlen(Lxcodeindex) / 3); j++) {
        strncpy(code_contrast, Lxcodeindex + 0 + j * 3, 3);
        if (strcmp(code_contrast, code_original) == 0) {
            code_return = j + freq;
        }
    }return code_return;
}
/**
 * Converts the observation type to the numeric code defined.
 * 
 * \param i: Reads the number of incoming loops in the loop
 * \param buff: Type of incoming observation
 * \return 
 */
int type2code(int i, char buff[MAXRINEX])
{
    int  code_return = 0;
    char code_original[4] = "/0";

    const char L1codeindex[] = "C1AC1BC1CC1DC1LC1MC1PC1SC1XC1YC1Z";//obs type of different frequency 
    const char L2codeindex[] = "C2CC2DC2IC2LC2MC2PC2QC2SC2XC2YC2Z";
    const char L3codeindex[] = "C3IC3QC3X";
    const char L4codeindex[] = "C5IC5QC5X";
    const char L5codeindex[] = "C5IC5QC5X";
    const char L6codeindex[] = "C6AC6BC6CC6XC6Z";
    const char L7codeindex[] = "C7IC7QC7XC7DC7PC7Z";
    const char L8codeindex[] = "C8IC8QC8X";

    strncpy(code_original, buff + 7 + 4 * i, 3);

    if (strstr(code_original, "1")) return findtype(L1codeindex, code_original, C1);
    else if (strstr(code_original, "2")) return findtype(L2codeindex, code_original, C2);
    else if (strstr(code_original, "3")) return findtype(L3codeindex, code_original, C3);
    else if (strstr(code_original, "4")) return findtype(L4codeindex, code_original, C4);
    else if (strstr(code_original, "5")) return findtype(L5codeindex, code_original, C5);
    else if (strstr(code_original, "6")) return findtype(L6codeindex, code_original, C6);
    else if (strstr(code_original, "7")) return findtype(L7codeindex, code_original, C7);
    else if (strstr(code_original, "8")) return findtype(L8codeindex, code_original, C8);
    else return 0;
}
/**
 * Match the obs code and convert into type.
 * 
 * \param type: Obs type that you want to match
 * \param typenum: The total number of obs types
 * \param typearr: Type codes store arrays
 * \return the array position of the corresponding obs type code
 */
int code2type(int type, int typenum, int typearr[36])
{
    int pos;
    for (pos = 0; pos < typenum; pos++) {
        if ((typearr[pos] - typearr[pos] % 100) == type) {
            return pos;
        }
    }return pos;
}
/**
 * Broad form of function code2type.
 * 
 * \param exclude: The excluded type
 * \param typenum: The total number of obs types
 * \param typearr: Type codes store arrays
 * \return the array position of the corresponding obs type code
 */
int code2type_broad(int exclude, int freq, int typenum, int typearr[36]) 
{
    int pos;
    for (pos = 0; pos < typenum; pos++) {
        if (typearr[pos] == 0 ? (0) : ((typearr[pos] - typearr[pos] % 100) == exclude ? 0 : 1)) {
            
            return pos;
        }
    }return pos;
}
/*Read the file of rnx*/
/**
 * Convert the string to number.
 * 
 * \param buff
 * \param i: Position of begin to read
 * \param n: The number of character will to capture
 * \return number of string you captured
 * 
 * @Author: T. TAKASU
 * 
 * Function will return 0.0 as error code when three occasion are below:
 * 1.Begining position < 0
 * 2.The number of Byte of read < i
 * 3.The Byte size of string < n
 */
static double strtonum(const char* buff, int i, int n)
{
    double value = 0.0;char str[256] = { 0 };char* p = str;
    if (i < 0 || (int)strlen(buff) < i || (int)sizeof(str) - 1 < n) {
        return 0.0;
    }
    for (buff += i; *buff && --n >= 0; buff++) {
        *p++ = ((*buff == 'D' || *buff == 'd') ? 'e' : *buff);
    }
    *p = '\0';
    return sscanf(str, "%lf", &value) == 1 ? value : 0.0;
}
/*Free the memory of observation structure*/
void freeobs_e(pobs_epoch obs_e, pobs_body obs_b)
{
    free(obs_e); free(obs_b);
}
/*Read the file of nav*/
/**
 * Get the total amount of satellite boardcast data of nav file .
 * 
 * \param fp_nav: The file pointer of nav file
 * \return amount of satellite
 */
int getsatnum(FILE* fp_nav)
{
    int satnum = 0;
    char buff[MAXRINEX];
    char satvar;
    char* lable = buff + 60;
    while (fgets(buff, MAXRINEX, fp_nav)) {	
        if (strstr(lable, "RINEX VERSION / TYPE")) {
            if (strtonum(buff, 0, 9) < 3 || strtonum(buff, 0, 9) >= 4) return -1;
        }
        if (strstr(lable, "END OF HEADER")) {
            while (fgets(buff, MAXRINEX, fp_nav)) {
                strncpy(&satvar, buff + 0, 1);
                if (satvar == 'G' || satvar == 'E' || satvar == 'R' || satvar == 'S' || satvar == 'C' || satvar == 'I' || satvar == 'J') {
                    satnum++;
                }
                else {
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
    while (fgets(buff, MAXRINEX, fp_nav)) {
        if (strstr(lable, "RINEX VERSION / TYPE")) {
            nav_h->ver = strtonum(buff, 0, 9);
            strncpy((nav_h->type), buff + 20, 15);
            continue;
        }
        else if (strstr(lable, "GPSA")) {
            nav_h->ION_GPSA[0] = strtonum(buff, 6, 12);
            nav_h->ION_GPSA[1] = strtonum(buff, 6 + 12, 12);
            nav_h->ION_GPSA[2] = strtonum(buff, 6 + 12 + 12, 12);
            nav_h->ION_GPSA[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
            continue;
        }
        else if (strstr(lable, "GPSB")) {
            nav_h->ION_GPSB[0] = strtonum(buff, 6, 12);
            nav_h->ION_GPSB[1] = strtonum(buff, 6 + 12, 12);
            nav_h->ION_GPSB[2] = strtonum(buff, 6 + 12 + 12, 12);
            nav_h->ION_GPSB[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
            continue;
        }
        else if (strstr(lable, "BDSA")) {
            nav_h->ION_BDSA[0] = strtonum(buff, 6, 12);
            nav_h->ION_BDSA[1] = strtonum(buff, 6 + 12, 12);
            nav_h->ION_BDSA[2] = strtonum(buff, 6 + 12 + 12, 12);
            nav_h->ION_BDSA[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
            continue;
        }
        else if (strstr(lable, "BDSB")) {
            nav_h->ION_BDSB[0] = strtonum(buff, 6, 12);
            nav_h->ION_BDSB[1] = strtonum(buff, 6 + 12, 12);
            nav_h->ION_BDSB[2] = strtonum(buff, 6 + 12 + 12, 12);
            nav_h->ION_BDSB[3] = strtonum(buff, 6 + 12 + 12 + 12, 12);
            continue;
        }
        else if (strstr(lable, "BDUT")) {
            nav_h->BDUT[0] = strtonum(buff, 5, 17);
            nav_h->BDUT[1] = strtonum(buff, 5 + 17, 16);
            nav_h->BDUT[2] = strtonum(buff, 5 + 17 + 16, 7);
            nav_h->BDUT[3] = strtonum(buff, 5 + 17 + 16 + 7, 5);
            continue;
        }
        else if (strstr(lable, "GPUT")) {
            nav_h->GPUT[0] = strtonum(buff, 5, 17);
            nav_h->GPUT[1] = strtonum(buff, 5 + 17, 16);
            nav_h->GPUT[2] = strtonum(buff, 5 + 17 + 16, 7);
            nav_h->GPUT[3] = strtonum(buff, 5 + 17 + 16 + 7, 5);
            continue;
        }
        else if (strstr(lable, "LEAP SECONDS")) {
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
    while (fgets(buff, MAXRINEX, fp_nav)) {
        int j_g = 0;
        int j_c = 0;
        int j_ga = 0;
        int j_gl = 0;
        strncpy(&flag, buff + 0, 1);
        //GPS SATELLITE
        if (flag == 'G') {
            for (j_g = 0; j_g < 8; j_g++) {
                switch (j_g) {
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
        if (flag == 'C') {
            for (j_c = 0; j_c < 8; j_c++) {
                switch (j_c) {
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
        if (flag == 'E') {
            for (j_ga = 0; j_ga < 8; j_ga++) {
                switch (j_ga) {
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
        if (flag == 'R') {
            for (j_gl = 0; j_gl < 4; j_gl++) {
                switch (j_gl) {
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
/*Read the file of obs*/
/**
 * Get the total amount of epoch of obs.
 * 
 * \param fp_obs: The file pointer of obs
 * \return amount of epoch
 */
int get_epochnum(FILE* fp_obs)
{
    int n = 0;
    char flag;
    char buff[MAXRINEX];
    char* lable = buff + 60;
    while (fgets(buff, MAXRINEX, fp_obs)) {
        if (strstr(lable, "RINEX VERSION / TYPE")) {
            if (strtonum(buff, 0, 9) < 3) return -1;
        }
        if (strstr(lable, "END OF HEADER")) {
            while (fgets(buff, MAXRINEX, fp_obs)) {
                strncpy(&flag, buff + 0, 1);
                if (flag == '>') {
                    n++;
                }
            }
        }
    }return n;
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

    while (fgets(buff, MAXRINEX, fp_obs)) {
        if (strstr(lable, "RINEX VERSION / TYPE")) {
            obs_h->ver = strtonum(buff, 0, 9);
            strncpy(obs_h->type, buff + 20, 30);
            continue;
        }
        else if (strstr(lable, "APPROX POSITION XYZ")) {
            obs_h->apX = strtonum(buff, 0, 14);
            obs_h->apY = strtonum(buff, 0 + 14, 14);
            obs_h->apZ = strtonum(buff, 0 + 14 + 14, 14);
            continue;
        }
        else if (strstr(lable, "ANTENNA: DELTA H/E/N")) {
            obs_h->ANTH = strtonum(buff, 0, 14);
            obs_h->ANTdeltaE = strtonum(buff, 14, 14);
            obs_h->ANTdeltaN = strtonum(buff, 14 + 14, 14);
            continue;
        }
        else if (strstr(lable, "SYS / # / OBS TYPES")) {
            char flag = { 0 };
            strncpy(&flag, buff + 0, 1);
            if (flag == 'G') {
                obs_h->obstypenum_gps = (int)strtonum(buff, 4, 2);
                for (i = 0; i < obs_h->obstypenum_gps;) {
                    for (int j = 0; j < 13; i++, j++) {
                        if (i == obs_h->obstypenum_gps) break;
                        else obs_h->obscode_gps[i] = type2code(i, buff);
                    }i == obs_h->obstypenum_gps? 0 : fgets(buff, MAXRINEX, fp_obs);
                }continue;
            }
            else if (flag == 'C') {
                obs_h->obstypenum_bds = (int)strtonum(buff, 4, 2);
                for (i = 0; i < obs_h->obstypenum_bds;) {
                    for (int j = 0; j < 13; i++, j++) {
                        if (i == obs_h->obstypenum_bds) break;
                        else obs_h->obscode_bds[i] = type2code(i, buff);
                    }i == obs_h->obstypenum_bds ? 0 : fgets(buff, MAXRINEX, fp_obs);
                }continue;
            }
            else if (flag == 'E') {
                obs_h->obstypenum_gal = (int)strtonum(buff, 4, 2);
                for (i = 0; i < obs_h->obstypenum_gal;) {
                    for (int j = 0; j < 13; i++, j++) {
                        if (i == obs_h->obstypenum_gal) break;
                        else obs_h->obscode_gal[i] = type2code(i, buff);
                    }i == obs_h->obstypenum_gal ? 0 : fgets(buff, MAXRINEX, fp_obs);
                }continue;
            }
            else if (flag == 'R') {
                obs_h->obstypenum_glo = (int)strtonum(buff, 4, 2);
                for (i = 0; i < obs_h->obstypenum_glo;) {
                    for (int j = 0; j < 13; i++, j++) {
                        if (i == obs_h->obstypenum_glo) break;
                        else obs_h->obscode_glo[i] = type2code(i, buff);
                    }i == obs_h->obstypenum_glo ? 0 : fgets(buff, MAXRINEX, fp_obs);
                }continue;
            }continue;
        }
        else if (strstr(lable, "INTERVAL")) {
            obs_h->interval = strtonum(buff, 0, 10);
            continue;
        }
        else if (strstr(lable, "TIME OF FIRST OBS")) {
            obs_h->f_y = (int)strtonum(buff, 2, 4);
            obs_h->f_m = (int)strtonum(buff, 2 + 6, 4);
            obs_h->f_d = (int)strtonum(buff, 2 + 6 + 6, 4);
            obs_h->f_h = (int)strtonum(buff, 2 + 6 + 6 + 6, 4);
            obs_h->f_min = (int)strtonum(buff, 2 + 6 + 6 + 6 + 6, 4);
            obs_h->f_sec = strtonum(buff, 2 + 6 + 6 + 6 + 6 + 6, 9);
            strncpy(obs_h->tsys, buff + 6 + 6 + 6 + 6 + 6 + 18, 3);
            continue;
        }
        else if (strstr(lable, "TIME OF LAST OBS")) {
            obs_h->l_y = (int)strtonum(buff, 2, 4);
            obs_h->l_m = (int)strtonum(buff, 2 + 6, 4);
            obs_h->l_d = (int)strtonum(buff, 2 + 6 + 6, 4);
            obs_h->l_h = (int)strtonum(buff, 2 + 6 + 6 + 6, 4);
            obs_h->l_min = (int)strtonum(buff, 2 + 6 + 6 + 6 + 6, 4);
            obs_h->l_sec = strtonum(buff, 2 + 6 + 6 + 6 + 6 + 6, 9);
            continue;
        }
        else if (strstr(lable, "END OF HEADER")) {
            break;
        }
    }
}
/*Read the body data of file of obs*/
void read_o_eb(FILE* fp_obs, pobs_head obs_h, pobs_epoch obs_e, pobs_body obs_b)
{
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