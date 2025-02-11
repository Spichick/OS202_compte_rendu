<<<<<<< HEAD
# include "Matrix.hpp"
# include <cassert>

Matrix::Matrix( int nRows, int nCols ) :
  nbRows{nRows}, nbCols{nCols}, m_arr_coefs(nRows*nCols)
{}
// ------------------------------------------------------------------------
Matrix::Matrix( int nRows, int nCols, double val ) :
  nbRows{nRows}, nbCols{nCols}, m_arr_coefs(nRows*nCols, val)
{}
// ========================================================================
=======
# include "Matrix.hpp"
# include <cassert>

Matrix::Matrix( int nRows, int nCols ) :
  nbRows{nRows}, nbCols{nCols}, m_arr_coefs(nRows*nCols)
{}
// ------------------------------------------------------------------------
Matrix::Matrix( int nRows, int nCols, double val ) :
  nbRows{nRows}, nbCols{nCols}, m_arr_coefs(nRows*nCols, val)
{}
// ========================================================================
>>>>>>> 48d0b7edac6490e9191898da2a8c61a848f9ff3e
