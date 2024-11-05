#include "brdm2pos.h"
using namespace std;
/*Tropshere correction with saastamoinen model*/
static double trosaastamoinen(pobs_head obs_h, double elev)
{
    double P0, e0, T0, deltaSd, deltaSw, dtropd, dtropw, dtrop;
    double B = obs_h->apB, L = obs_h->apL, H = obs_h->apH;

    P0 = 1013.25 * pow((1 - 2.2557 * 10e-5 * H), 5.2568);
    e0 = 11.69;
    T0 = 15 - 6.5 * 10e-3 * H + 273.15;
    deltaSd = 2.2768e-3 * P0 / (1 - 2.66e-3 * cos(2 * B) - 2.8e-4 * H * 1e3);
    deltaSw = 2.2768e-3 * (1255 / T0 + 0.05) * e0;
    // Dry
    dtropd = deltaSd / sqrt(
                            sin(
                                deg2rad(
                                        rad2deg(
                                                pow(elev,2) 
                                               ) + 6.25
                                       )
                               )
                           );
    // Wet
    dtropw = deltaSw / sqrt(
                            sin(
                                deg2rad(
                                        rad2deg(
                                                pow(elev,2)
                                               ) + 6.25
                                       )
                               )
                           );
    dtrop = dtropw + dtropd;
    return dtrop;
}
/*Tropshere correction with hopfiled model*/
static double trohopfield(pobs_head obs_h, double elev)
{
    double P0, e0, T0, deltaSd, deltaSw, dtropd, dtropw, dtrop;
    double B = obs_h->apB, L = obs_h->apL, H = obs_h->apH;

    P0 = 1013.25 * pow((1 - 2.2557 * 10e-5 * H), 5.2568);
    e0 = 11.69;
    T0 = 15 - 6.5 * 10e-3 * H + 273.15;
    deltaSd = 1.552e-5 * P0 * (40136 + 148.72 * (T0 - 273.16) - H) / T0;
        deltaSw = 1.552e-5 * 4810 * e0 * (11000 - H) / pow(T0, 2);
    // Dry delay component
    dtropd = deltaSd / sqrt(
        sin(
            deg2rad(
                rad2deg(
                    pow(deg2rad(elev), 2)
                ) + 6.25
            )
        )
    );
    // Wet delay component
    dtropw = deltaSw / sqrt(
        sin(
            deg2rad(
                rad2deg(
                    pow(deg2rad(elev), 2)
                ) + 6.25
            )
        )
    );
    dtrop = dtropw + dtropd;
    return dtrop;
}
/*Iono correction by IF-IC*/
static double ionofree(acct_obs obs, pobs_head obs_h, int k, int GNSS)
{
    double P1 = obs.Per1[k], P2 = obs.Per2[k],
           freq1 = obs.freq1, freq2 = obs.freq2;
    //IF-IC
    if (P1 != 0.0 && P2 != 0.0) {
        P1 = (pow(freq1, 2) * P1) / (pow(freq1, 2) - pow(freq2, 2))
            - (pow(freq2, 2) * P2) / (pow(freq1, 2) - pow(freq2, 2));

        return P1;
    }
    if (P1 == 0.0 || P2 == 0.0) {
        if (P1 == 0.0 && P2 != 0.0) return P2;
        if (P1 != 0.0 && P2 == 0.0) return P1;
        return 0.0;
    }
}
/*Rest correction of observation*/
static double restcorr(pobs_head obs_h, acct_obs obs, int ionopt, int tropopt,
    int k, int GNSS, double elev) {

    double P = 0.0, diono = 0.0, dtrop = 0.0;

    switch (ionopt) {
    case 0:P = obs.Per1[k]; break;
    case 1:P = ionofree(obs, obs_h, k, GNSS); break;
    case 2:break;
    }
    switch (tropopt) {
    case 0:break;
    case 1:dtrop = trohopfield(obs_h, elev); break;
    case 2:dtrop = trosaastamoinen(obs_h, elev); break;
    }
    P = P - diono - dtrop;
    return P;
}
/*(Weighted)Least square estimate*/
int lsq(const double* BtP, const double* L, const double* B, int n, int m, double* x,
    double* Q)
{
    double* BtPL;
    int info;

    if (m < n) return -1;
    BtPL = mat(n, 1);

    matmul("NN", n, 1, m, 1.0, BtP, L, 0.0, BtPL); /* =B'*P*L */
    matmul("NN", n, n, m, 1.0, BtP, B, 0.0, Q);  /* =B'*P*B */
    if (!(info = matinv(Q, n)))
    matmul("NN", n, 1, n, 1.0, Q, BtPL, 0.0, x); /* x=Q^-1*(B'*P*L) */
    free(BtPL);
    return info;
}
/*Construct into desgin matrix and solve the lsq*/
stations designmat(pobs_head obs_h, acct_obs obs,
    double *l, double* m, double* n, double* o,
    double* B, double* P, double* L,
    double X, double Y, double Z,
    int satnum, int ionopt, int tropopt, int GNSS)
{
    stations sta;
    double Q[16], dx[4], *BP, *PL;
    BP = mat(satnum, 4);
    PL = mat(satnum, 1);

    double R;
    for (int i = 0; i < satnum; i++) {
        R = sqrt(
            pow(l[i] - X, 2) +
            pow(m[i] - Y, 2) +
            pow(n[i] - Z, 2)
        );
        B[i + satnum * 0] = -(l[i] - X) / R;
        B[i + satnum * 1] = -(m[i] - Y) / R;
        B[i + satnum * 2] = -(n[i] - Z) / R;
        B[i + satnum * 3] = 1;
        P[i * (satnum) + i] = pow(sin(o[i]),2);
        L[i] = restcorr(obs_h, obs, ionopt, tropopt, i, GNSS, o[i]) -
            R + obs.sclk[i] * C_V;
    }
    matmul("TN", 4, satnum, satnum, 1.0, B, P, 0.0, BP);//B'*P
    if (!lsq(BP, L, B, 4, satnum, dx, Q))
        sta.X = dx[0]; sta.Y = dx[1]; sta.Z = dx[2]; sta.delta_TR = dx[3];

    free(BP); free(PL);

    return sta;
}
/*Output the header data of satllite position solution*/
FILE* headerout(pobs_head obs_h, int mode,
    char obs_path[MAXPATH], char nav_path[MAXPATH], char res_path[MAXPATH])
{
    time_t gen_time;
    time(&gen_time);

    FILE* result_file_clear = fopen(res_path, "w");
    fclose(result_file_clear);
    FILE* result_file = fopen(res_path, "a+");
    fprintf(result_file, ">GENERATE PROGRAM   : KNZ_GeoTrackLab ver%s\n", KNZ_GTL_VER);
    fprintf(result_file, " GENERATE SOURCE    : %.10s\n", obs_h->marker);

    if (mode != 1); fprintf(result_file, " GENERATE TYPE      : Position Resolve\n");
    if (mode == 0); fprintf(result_file, " GENERATE TYPE      : Satellite  Position\n");
    fprintf(result_file, " GENERATE TIME      : %s", ctime(&gen_time));
    fprintf(result_file, " OBS FILE PATH      : %s\n", obs_path);
    fprintf(result_file, " NAV FILE PATH      : %s\n", nav_path);
    fprintf(result_file, " APPROX POSITION XYZ: %13.04f%13.04f%13.04f\n"\
                         " APPROX POSITION BLH:  %12.07f %12.07f %12.07f\n"
        , obs_h->apX, obs_h->apY, obs_h->apZ
        , obs_h->apB, obs_h->apL, obs_h->apH);
    fprintf(result_file, " TIME OF FIRST OBS  : %4d %02d %02d %02d %02d %07.4f\n"
        , obs_h->f_y, obs_h->f_m, obs_h->f_d, obs_h->f_h, obs_h->f_min, obs_h->f_sec);
    fprintf(result_file, " TIME OF LAST OBS   : %4d %02d %02d %02d %02d %07.4f\n"
        , obs_h->l_y, obs_h->l_m, obs_h->l_d, obs_h->l_h, obs_h->l_min, obs_h->l_sec);
    fprintf(result_file, " INTERVAL           : %5.02f\n",obs_h->interval);
    fprintf(result_file, "<END OF HEADER\n");

    return result_file;
}
/*Output the satellite solution data*/
void outdata(blh blh, FILE* res_file, int sPRN, int GNSS)
{
    switch (GNSS) {
    case GPS:
        fprintf(res_file, "\nG%02d %9.06f %9.06f %15.05f"
            , sPRN, blh.B, blh.L, blh.H);break;
    case BDS:
        fprintf(res_file, "\nC%02d %9.06f %9.06f %15.05f"
            , sPRN, blh.B, blh.L, blh.H);break;
    case GAL:
        fprintf(res_file, "\nE%02d %9.06f %9.06f %15.05f"
            , sPRN, blh.B, blh.L, blh.H);break;
    case GLO:
        fprintf(res_file, "\nR%02d %9.06f %9.06f %15.05f"
            , sPRN, blh.B, blh.L, blh.H);break;
    }
}
/*Output the satellite solution data*/
void solution(FILE* res_file,pobs_head obs_h, double X, double Y, double Z)
{
    double deltax, deltay, deltaz;
    deltax = X - obs_h->apX;
    deltay = Y - obs_h->apY;
    deltaz = Z - obs_h->apZ;
    fprintf(res_file, "\nRec:%9.4f %9.4f %9.4f",
    deltax, deltay, deltaz);
}