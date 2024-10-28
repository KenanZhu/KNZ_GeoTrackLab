#include "brdm2pos.h"
using namespace std;
/* -------------------------------------------------------------------------- */
/// @brief degree to radian
/// @param deg 
/// @return return radian
/* -------------------------------------------------------------------------- */
double deg2rad(double deg)
{
	double rad = (PI / 180) * deg;
	return rad;
}
/* -------------------------------------------------------------------------- */
/// @brief radian to degree                      
/// @param rad 
/// @return return degree
/* -------------------------------------------------------------------------- */
double rad2deg(double rad)
{
	double deg = (180 / PI) * rad;
	return deg;
}
/* -------------------------------------------------------------------------- */
/// @brief satellite azimuth angle calculation
/// @param rahcal parameter transfer structure
/// @param E east
/// @param N north
/// @param U up
/// @return return structure contain R, A, H members                      
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
/// @brief convert BLH coordinates to ENU coordinates
/// @param blh2enu parameter transfer structure
/// @param stationB latitude of receiver station
/// @param stationL longitude of receiver station
/// @param deltax X-coordinate difference of satellite arrival center
/// @param deltay Y-coordinate difference of satellite arrival center
/// @param deltaz Z-coordinate difference of satellite arrival center
/// @return return type of structure contain E, N, U members
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
/// @param a major semiaxis of WGS-84 ellipsoid
/// @param e2 the square of the first eccentricity of WGS-84 ellipsoid
/// @return return type of structure contain B, L, H members
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