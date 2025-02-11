#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"

namespace {
void prodSubBlocks(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                  const Matrix& A, const Matrix& B, Matrix& C) {                
    for (int i = iRowBlkA; i < std::min(A.nbRows, iRowBlkA + szBlock); ++i) 
      for (int j = iColBlkB; j < std::min(B.nbCols, iColBlkB + szBlock); j++)
        for (int k = iColBlkA; k < std::min(A.nbCols, iColBlkA + szBlock); k++) 
        C(i, j) += A(i, k) * B(k, j);
}
// const int szBlock = 512;
}  // namespace

Matrix operator*(const Matrix& A, const Matrix& B) {
    Matrix C(A.nbRows, B.nbCols, 0.0);
    int szBlock = 512;
    // prodSubBlocks(0, 0, 0, std::max({A.nbRows, B.nbCols, A.nbCols}), A, B, C);
    for (int i = 0; i < A.nbRows; i += szBlock) {   
      for (int j = 0; j < B.nbCols; j += szBlock) { 
        for (int k = 0; k < A.nbCols; k += szBlock) {
          prodSubBlocks(i, j, k, szBlock, A, B, C);
        }
      }
    }
    return C;
  }
// set OMP_NUM_THREADS=12
// .\TestProductMatrix.exe 1024