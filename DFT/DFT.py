import numpy as np
import cmath as cm

# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries


class DFT:

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""
        w,h=matrix.shape


        beta = [[0 for x in range(w)] for y in range(h)]

        for a in range(h):
            for b in range(w):
                asum = 0
                for i in range(h):
                    for j in range(w):
                        asum += matrix[i][j]*((cm.cos(((2*cm.pi)/w)*(a*i+b*j)))-cm.sqrt(-1)*cm.sin(((2*cm.pi)/w)*(a*i+b*j)))
                gyu = float('%.3f'%(asum.real))
                nam = float('%.3f'%(asum.imag))
                beta[a][b] = gyu+nam*1j

        return beta

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        matrix: a 2d matrix (DFT) usually complex
        takes as input:
        returns a complex matrix representing the inverse fourier transform"""



        return matrix


    def discrete_cosine_tranform(self, matrix):
        """Computes the discrete cosine transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing discrete cosine transform"""



        return matrix


    def magnitude(self, matrix):
        """Computes the magnitude of the DFT
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the dft"""

        return matrix