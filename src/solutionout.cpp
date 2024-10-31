#include "brdm2pos.h"
using namespace std;

/*Output the header data of satllite position solution*/
FILE* outputheader(pobs_head obs_h,
      char obs_path[MAXPATH], char nav_path[MAXPATH], char res_path[MAXPATH])
{
    time_t gen_time;
    time(&gen_time);

    FILE* result_file_clear = fopen(res_path, "w");
    fclose(result_file_clear);
    FILE* result_file = fopen(res_path, "a+");
    fprintf(result_file, "@ GENERATE PROGRAM   : KNZ_GeoTrackLab ver1.5.4.1\n");
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
        , obs_h->apB, obs_h->apL, obs_h->apH);
    fprintf(result_file, "END OF HEADER\n");

    return result_file;
}
/*Ion correction by IF-IC*/
static double ionofree(pobs_body obs_b, pobs_head obs_h, int j, int GNSS)
{
    double P1=0.0, P2=0.0, freq1=0.0, freq2=0.0;
    //Match the code with system
    switch (GNSS) {
    case GPS:
        P1 = obs_b->obs_gps[j][code2type(C1, obs_h->obstypenum_gps, obs_h->obscode_gps)];
        P2 = obs_b->obs_gps[j][code2type(C2, obs_h->obstypenum_gps, obs_h->obscode_gps)];
        freq1 = FREQ1; freq2 = FREQ2;
        break;
    case BDS:
        P1 = obs_b->obs_bds[j][code2type(C2, obs_h->obstypenum_bds, obs_h->obscode_bds)];
        P2 = obs_b->obs_bds[j][code2type(C7, obs_h->obstypenum_bds, obs_h->obscode_bds)];
        freq1 = FREQ1_BDS; freq2 = FREQ2_BDS;
        break;
    case GAL:
        P1 = obs_b->obs_gal[j][code2type(C1, obs_h->obstypenum_gal, obs_h->obscode_gal)];
        P2 = obs_b->obs_gal[j][code2type(C5, obs_h->obstypenum_gal, obs_h->obscode_gal)];
        freq1 = FREQ1; freq2 = FREQ6;
        break;
    case GLO:
        P1 = obs_b->obs_glo[j][code2type(C1, obs_h->obstypenum_glo, obs_h->obscode_glo)];
        P2 = obs_b->obs_glo[j][code2type(C2, obs_h->obstypenum_glo, obs_h->obscode_glo)];
        freq1 = FREQ1_GLO; freq2 = FREQ2_GLO;
        break;
    }
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
/*Output the satellite solution data*/
void outputbodydata(pobs_head obs_h, pobs_body obs_b,
     pos_ts pos_t, rah in_rah, FILE* res_file,
     int sPRN, int j, int GNSS)
{
    double P = ionofree(obs_b, obs_h, j, GNSS);

    if (P == 0) return;

    switch (GNSS) {
    case GPS:
        fprintf(res_file, "\nG %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
            , sPRN, pos_t.X, pos_t.Y, pos_t.Z
            , P, in_rah.H, pos_t.delta_clk);
        break;
    case BDS:
        if (sPRN <= 5 || sPRN >= 59) break;
        else;
        fprintf(res_file, "\nC %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
            , sPRN, pos_t.X, pos_t.Y, pos_t.Z
            , P, in_rah.H, pos_t.delta_clk);
        break;
    case GAL:
        fprintf(res_file, "\nE %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
            , sPRN, pos_t.X, pos_t.Y, pos_t.Z
            , P, in_rah.H, pos_t.delta_clk);
        break;
    case GLO:
        fprintf(res_file, "\nR %02d| %15.05f %15.05f %15.05f %15.05f %15.05f %16.13f"
            , sPRN, pos_t.X, pos_t.Y, pos_t.Z
            , P, in_rah.H, pos_t.delta_clk);
        break;
    }
}