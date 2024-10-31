#include "brdm2pos.h"
using namespace std;
/**
 * Degree to radian.
 * 
 * \param deg: Degree
 * \return Radian
 */
double deg2rad(double deg)
{
	double rad = (PI / 180) * deg;
	return rad;
}
/**
 * Radian to degree .
 * 
 * \param rad: Radian
 * \return Degree
 */
double rad2deg(double rad)
{
	double deg = (180 / PI) * rad;
	return deg;
}
/**
 * Azimuth/Calculate.
 * 
 * \param rah: Parameter transfer structure
 * \param E: East
 * \param N: North
 * \param U: Up
 * \return structure contain R, A, H members
 */
rah rahcal(rah rah,
	double E, double N, double U)
{
	rah.H = atan2(U, sqrt(E * E + N * N));
	rah.A = atan2(E, U);
	if (rah.A < 0)
		rah.A += 2 * PI;
	if (rah.A > 2 * PI)
		rah.A -= 2 * PI;
	rah.R = sqrt(E * E + N * N + U * U);

	return rah;
}
/**
 * Convert BLH coordinates to ENU coordinates.
 * 
 * \param enu: Parameter transfer structure
 * \param stationB: Latitude of receiver station
 * \param stationL: Longitude of receiver station
 * \param deltax: Deltax X-coordinate difference of satellite arrival center
 * \param deltay: Deltax Y-coordinate difference of satellite arrival center
 * \param deltaz: Deltax Z-coordinate difference of satellite arrival center
 * \return 
 */
enu blh2enu(enu enu,
	double stationB, double stationL,
	double deltax, double deltay, double deltaz)
{
	double sinB = sin(stationB);
	double cosB = cos(stationB);
	double sinL = sin(stationL);
	double cosL = cos(stationL);
	enu.E = -sinL * (deltax)       +cosL * (deltay);
	enu.N = -sinB * cosL * (deltax)-sinB * sinL * (deltay)+cosB * (deltaz);
	enu.U =  cosB * cosL * (deltax)+cosB * sinL * (deltay)+sinB * (deltaz);

	return enu;
}
/**
 * Convert ECEF geostationary coordinates to BLH coordinates.
 * 
 * \param blh: Parameter transfer structure
 * \param X: X coordinates of ECEF
 * \param Y; Y coordinates of ECEF
 * \param Z: Z coordinates of ECEF
 * \return type of structure contain B, L, H members
 */
blh xyz2blh(blh blh,
	double X, double Y, double Z)
{
	double B = 0.0, N = 0.0, H = 0.0, R0, R1, deltaH, deltaB;
	R0 = sqrt(pow(X, 2) + pow(Y, 2));
	R1 = sqrt(pow(X, 2) + pow(Y, 2) + pow(Z, 2));
	blh.L = atan2(Y, X);
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
	blh.B = B;
	blh.H = H;

	return blh;
}