#include "brdm2pos.h"
using namespace std;
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
	if (gnsscode == BDS) {
		if (sPRN > 5 && sPRN < 59) //BDS IGSO & MEO Satellites
		{
			l = nav_b[best_epoch].OMEGA + (nav_b[best_epoch].deltaomega - Earth_e) * tk - Earth_e * nav_b[best_epoch].TOE;
			X = x * cos(l) - y * cos(i) * sin(l);
			Y = x * sin(l) + y * cos(i) * cos(l);
			Z = y * sin(i);
		}
		else //BDS GEO Satellites
		{
			l = nav_b[best_epoch].OMEGA + nav_b[best_epoch].deltaomega * tk - Earth_e * nav_b[best_epoch].TOE;
			X = x * cos(l) - y * cos(i) * sin(l);
			Y = x * sin(l) + y * cos(i) * cos(l);
			Z = y * sin(i);

			double f = deg2rad(-5);
			double p = Earth_e * tk;

			X = X * cos(p) + Y * sin(p) * cos(f) + Z * sin(p) * sin(f);
			Y = X * -sin(p) + Y * cos(p) * cos(f) + Z * cos(p) * sin(f);
			Z = Y * -sin(f) + Z * cos(f);
		}
	}
	else {
		l = nav_b[best_epoch].OMEGA + (nav_b[best_epoch].deltaomega - Earth_e) * tk - Earth_e * nav_b[best_epoch].TOE;
		X = x * cos(l) - y * cos(i) * sin(l);
		Y = x * sin(l) + y * cos(i) * cos(l);
		Z = y * sin(i);
	}
	pos_t.X = cos(Earth_e * pos_t.delta_t) * X + sin(Earth_e * pos_t.delta_t) * Y;
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

			while (fabs(pos_t.delta_t - pos_t.deltat) > 1.0e-9) {
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
double brdm2pos(char nav_path[260], char obs_path[260], char res_path[260], int gnsscode)
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
	if (fp_nav == NULL) return -1;
	satnum = getsatnum(fp_nav);

	switch (satnum) {
		case -1: return -3;//mismatch version or format
		case  0: return -4;//no data
		default:
			break;
	}

	rewind(fp_nav);
	nav_h = (pnav_head)malloc(sizeof(nav_head));
	nav_b = (pnav_body)malloc(sizeof(nav_body) * (satnum));
	if (nav_h && nav_b) {
		read_n_h(fp_nav, nav_h); read_n_b(fp_nav, nav_b);
	}
	fclose(fp_nav);

	FILE* fp_obs = fopen(obs_path, "r");
	if (fp_obs == NULL) return -2;
	epochunum = get_epochnum(fp_obs);

	switch (epochunum) {
		case -1: return -5;//mismatch version or format
		case  0: return -6;//no data
		default:
			break;
	}

	rewind(fp_obs);
	obs_h = (pobs_head)malloc(sizeof(obs_head));
	if (obs_h) {
		read_o_h(fp_obs, obs_h);

		tem2 = XYZ2BLH(tem2, obs_h->apX, obs_h->apY, obs_h->apZ);
		station.B = tem2.B; station.L = tem2.L; station.H = tem2.H;

		//Out put the header of solution file
		FILE* result_file_clear = fopen(res_path, "w");
		fclose(result_file_clear);
		FILE* result_file = fopen(res_path, "a+");
		fprintf(result_file, "@ GENERATE PROGRAM   : KNZ_GeoTrackLab ver1.5.3.1\n");
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
		for (int i = 0; i < epochunum; i++) {
			//Allocate memory for obs epoch and body data
			obs_e = (pobs_epoch)malloc(sizeof(obs_epoch));
			obs_b = (pobs_body)malloc(sizeof(obs_body));

			read_o_eb(fp_obs, obs_h, obs_e, obs_b);
			result += sat_pos_cal(obs_h, obs_e, obs_b, nav_b,
				result_file, station,
				gnsscode, satnum);

			fprintf(result_file, "\n");
			freeobs_e(obs_e, obs_b);
		}
		free(obs_h); free(nav_h); free(nav_b);
		fprintf(result_file, "\nEND"); fclose(result_file);
		if (epochunum == result) return 0;
	}
}