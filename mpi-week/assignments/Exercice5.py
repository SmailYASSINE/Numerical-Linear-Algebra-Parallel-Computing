import numpy as np
from scipy.sparse import lil_matrix
from numpy.random import rand, seed
from numba import njit
from mpi4py import MPI


''' This program compute parallel csc matrix vector multiplication using mpi '''

COMM = MPI.COMM_WORLD
nbOfproc = COMM.Get_size()
RANK = COMM.Get_rank()

seed(42)

def matrixVectorMult(A, b, x):
    
    row, col = A.shape
    for i in range(row):
        a = A[i]
        for j in range(col):
            x[i] += a[j] * b[j]

    return 0

########################initialize matrix A and vector b ######################
#matrix sizes
SIZE = 1000
Local_size = SIZE//nbOfproc

# counts = block of each proc
counts = []
displ =[]
for i in range(nbOfproc):
    counts[i] = Local_size 
    displ[i] = i*local_size 
# displacements = [i*Local_size for i in range(nbOfproc)]

if RANK == 0:
    A = lil_matrix((SIZE, SIZE))
    A[0, :100] = rand(100)
    A[1, 100:200] = A[0, :100]
    A.setdiag(rand(SIZE))
    A = A.toarray()
    b = rand(SIZE)
else :
    A = None
    b = None



b = COMM.bcast(b, root=0)
LocalMatrix = np.zeros((Local_size, SIZE))
# Scatter the matrix A
COMM.Scatterv([A, counts, displacements, MPI.DOUBLE], LocalMatrix, root=0)

#                                                   Compute A*b
LocalX = np.zeros(Local_size)

start = MPI.Wtime()
matrixVectorMult(LocalMatrix, b, LocalX)
stop = MPI.Wtime()
if RANK == 0:
    print("CPU time of parallel multiplication is ", (stop - start)*1000)

#                                                The use of GatherV into X

sendcounts = counts[RANK]
if RANK == 0:
    X = np.zeros(SIZE, dtype=np.float64)
else:
    X = None

COMM.Gatherv(LocalX, [X, sendcounts, np.arange(nbOfproc, dtype=np.int32) * local_size, MPI.DOUBLE], root=0)

if RANK == 0 :
    X_ = A.dot(b)
    print("The result of A*b using dot is :", np.max(X_ - X))


