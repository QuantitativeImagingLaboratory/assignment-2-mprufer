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
                        asum += matrix[i][j]*((cm.cos(((2*cm.pi)/w)*(a*i+b*j)))-(cm.sqrt(-1)*cm.sin(((2*cm.pi)/w)*(a*i+b*j))))
                real = float('%.3f'%(asum.real))
                comp = float('%.3f'%(asum.imag))
                beta[a][b] = real+comp*1j

        return beta

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        matrix: a 2d matrix (DFT) usually complex
        takes as input:
        returns a complex matrix representing the inverse fourier transform"""

        beta = [[0 for x in range(15)] for y in range(15)]

        for i in range(15):
            for j in range (15):
                asum = 0
                for u in range(15):
                    for v in range(15):
                        asum+=matrix[u][v]*((cm.cos((2*cm.pi/15)*(u*i+v*j)))+(cm.sqrt(-1)*cm.sin((2*cm.pi/15)*(u*i+v*j))))
                real = float('%.3f' % (asum.real))
                comp = float('%.3f' % (asum.imag))
                beta[i][j] = real+comp*1j

        return beta


    def discrete_cosine_tranform(self, matrix):
        """Computes the discrete cosine transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing discrete cosine transform"""
        w, h = matrix.shape

        beta = [[0 for x in range(w)] for y in range(h)]

        for a in range(h):
            for b in range(w):
                asum = 0
                for i in range(h):
                    for j in range(w):
                        asum += matrix[i][j] * (cm.cos(((2 * cm.pi) / w) * (a * i + b * j)))
                beta[a][b] = float('%.3f' % (asum.real))

        return beta


    def magnitude(self, matrix):
        """Computes the magnitude of the DFT
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the dft"""
        beta = [[0 for x in range(15)] for y in range(15)]

        for a in range(15):
            for b in range(15):
                asum = matrix[a][b]
                beta[a][b] = abs(matrix[a][b])
        return beta