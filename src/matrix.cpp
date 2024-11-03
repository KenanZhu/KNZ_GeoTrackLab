#include "brdm2pos.h"
/* new matrix ------------------------------------------------------------------
* allocate memory of matrix
* args   : int    n,m       I   number of rows and columns of matrix
* return : matrix pointer (if n<=0 or m<=0, return NULL)
*-----------------------------------------------------------------------------*/
double* mat(int n, int m)
{
    double* p;

    if (n <= 0 || m <= 0) return NULL;
    if (!(p = (double*)malloc(sizeof(double) * n * m))) {
        return NULL;
    }
    return p;
}
/* new integer matrix ----------------------------------------------------------
* allocate memory of integer matrix
* args   : int    n,m       I   number of rows and columns of matrix
* return : matrix pointer (if n<=0 or m<=0, return NULL)
*-----------------------------------------------------------------------------*/
int* imat(int n, int m)
{
    int* p;

    if (n <= 0 || m <= 0) return NULL;
    if (!(p = (int*)malloc(sizeof(int) * n * m))) {
        return NULL;
    }
    return p;
}
/* zero matrix -----------------------------------------------------------------
* generate new zero matrix
* args   : int    n,m       I   number of rows and columns of matrix
* return : matrix pointer (if n<=0 or m<=0, return NULL)
*-----------------------------------------------------------------------------*/
double* zeros(int n, int m)
{
    double* p;

#if NOCALLOC
    if ((p = mat(n, m))) for (n = n * m - 1; n >= 0; n--) p[n] = 0.0;
#else
    if (n <= 0 || m <= 0) return NULL;
    if (!(p = (double*)calloc(sizeof(double), n * m))) {
        return NULL;
    }
#endif
    return p;
}
/* identity matrix -------------------------------------------------------------
* generate new identity matrix
* args   : int    n         I   number of rows and columns of matrix
* return : matrix pointer (if n<=0, return NULL)
*-----------------------------------------------------------------------------*/
double* eye(int n)
{
    double* p;
    int i;

    if ((p = zeros(n, n))) for (i = 0; i < n; i++) p[i + i * n] = 1.0;
    return p;
}
/* inner product ---------------------------------------------------------------
* inner product of vectors
* args   : double *a,*b     I   vector a,b (n x 1)
*          int    n         I   size of vector a,b
* return : a'*b
*-----------------------------------------------------------------------------*/
double dot(const double* va, const double* vb, int n)
{
    double c = 0.0;

    while (--n >= 0) c += va[n] * vb[n];
    return c;
}
/* euclid norm -----------------------------------------------------------------
* euclid norm of vector
* args   : double *a        I   vector a (n x 1)
*          int    n         I   size of vector a
* return : || a ||
*-----------------------------------------------------------------------------*/
double norm(const double* va, int n)
{
    return sqrt(dot(va, va, n));
}
/* outer product of 3d vectors -------------------------------------------------
* outer product of 3d vectors
* args   : double *a,*b     I   vector a,b (3 x 1)
*          double *c        O   outer product (a x b) (3 x 1)
* return : none
*-----------------------------------------------------------------------------*/
void cross3(const double* va, const double* vb, double* vc)
{
    vc[0] = va[1] * vb[2] - va[2] * vb[1];
    vc[1] = va[2] * vb[0] - va[0] * vb[2];
    vc[2] = va[0] * vb[1] - va[1] * vb[0];
}
/* normalize 3d vector ---------------------------------------------------------
* normalize 3d vector
* args   : double *a        I   vector a (3 x 1)
*          double *b        O   normlized vector (3 x 1) || b || = 1
* return : status (1:ok,0:error)
*-----------------------------------------------------------------------------*/
int normv3(const double* va, double* vb)
{
    double r;
    if ((r = norm(va, 3)) <= 0.0) return 0;
    vb[0] = va[0] / r;
    vb[1] = va[1] / r;
    vb[2] = va[2] / r;
    return 1;
}
/* copy matrix -----------------------------------------------------------------
* copy matrix
* args   : double *A        O   destination matrix A (n x m)
*          double *B        I   source matrix B (n x m)
*          int    n,m       I   number of rows and columns of matrix
* return : none
*-----------------------------------------------------------------------------*/
void matcpy(double* A, const double* B, int n, int m)
{
    memcpy(A, B, sizeof(double) * n * m);
}
/*multiply matrix*/
void matmul(const char* tr, int n, int k, int m, double alpha,
    const double* A, const double* B, double beta, double* C)
{
    double d;
    int i, j, x, f = tr[0] == 'N' ? (tr[1] == 'N' ? 1 : 2) : (tr[1] == 'N' ? 3 : 4);

    for (i = 0; i < n; i++) for (j = 0; j < k; j++) {
        d = 0.0;
        switch (f) {
        case 1: for (x = 0; x < m; x++) d += A[i + x * n] * B[x + j * m]; break;
        case 2: for (x = 0; x < m; x++) d += A[i + x * n] * B[j + x * k]; break;
        case 3: for (x = 0; x < m; x++) d += A[x + i * m] * B[x + j * m]; break;
        case 4: for (x = 0; x < m; x++) d += A[x + i * m] * B[j + x * k]; break;
        }
        if (beta == 0.0) C[i + j * n] = alpha * d; else C[i + j * n] = alpha * d + beta * C[i + j * n];
    }
}
/*LU decomposition*/
static int ludcmp(double* A, int n, int* indx, double* d)
{
    double big, s, tmp, * vv = mat(n, 1);
    int i, imax = 0, j, k;

    *d = 1.0;
    for (i = 0; i < n; i++) {
        big = 0.0; for (j = 0; j < n; j++) if ((tmp = fabs(A[i + j * n])) > big) big = tmp;
        if (big > 0.0) vv[i] = 1.0 / big; else { free(vv); return -1; }
    }
    for (j = 0; j < n; j++) {
        for (i = 0; i < j; i++) {
            s = A[i + j * n]; for (k = 0; k < i; k++) s -= A[i + k * n] * A[k + j * n]; A[i + j * n] = s;
        }
        big = 0.0;
        for (i = j; i < n; i++) {
            s = A[i + j * n]; for (k = 0; k < j; k++) s -= A[i + k * n] * A[k + j * n]; A[i + j * n] = s;
            if ((tmp = vv[i] * fabs(s)) >= big) { big = tmp; imax = i; }
        }
        if (j != imax) {
            for (k = 0; k < n; k++) {
                tmp = A[imax + k * n]; A[imax + k * n] = A[j + k * n]; A[j + k * n] = tmp;
            }
            *d = -(*d); vv[imax] = vv[j];
        }
        indx[j] = imax;
        if (A[j + j * n] == 0.0) { free(vv); return -1; }
        if (j != n - 1) {
            tmp = 1.0 / A[j + j * n]; for (i = j + 1; i < n; i++) A[i + j * n] *= tmp;
        }
    }
    free(vv);
    return 0;
}
/*LU back-substitution*/
static void lubksb(const double* A, int n, const int* indx, double* b)
{
    double s;
    int i, ii = -1, ip, j;

    for (i = 0; i < n; i++) {
        ip = indx[i]; s = b[ip]; b[ip] = b[i];
        if (ii >= 0) for (j = ii; j < i; j++) s -= A[i + j * n] * b[j]; else if (s) ii = i;
        b[i] = s;
    }
    for (i = n - 1; i >= 0; i--) {
        s = b[i]; for (j = i + 1; j < n; j++) s -= A[i + j * n] * b[j]; b[i] = s / A[i + i * n];
    }
}
/*inverse of matrix*/
int matinv(double* A, int n)
{
    double d, * B;
    int i, j, * indx;

    indx = imat(n, 1); B = mat(n, n); matcpy(B, A, n, n);
    if (ludcmp(B, n, indx, &d)) { free(indx); free(B); return -1; }
    for (j = 0; j < n; j++) {
        for (i = 0; i < n; i++) A[i + j * n] = 0.0;
        A[j + j * n] = 1.0;
        lubksb(B, n, indx, A + j * n);
    }
    free(indx); free(B);
    return 0;
}
/*solve linear equation*/
int solve(const char* tr, const double* A, const double* Y, int n,
    int m, double* X)
{
    double* B = mat(n, n);
    int info;

    matcpy(B, A, n, n);
    if (!(info = matinv(B, n))) matmul(tr[0] == 'N' ? "NN" : "TN", n, m, n, 1.0, B, Y, 0.0, X);
    free(B);
    return info;
}
void matprint(const double A[], int n, int m, int p, int q)
{
    int i, j;

    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) printf(" %*.*f", p, q, A[i + j * n]);
        printf("\n");
    }
}


