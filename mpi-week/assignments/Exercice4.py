from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()


n, m = map(int, input().split())
if RANK == 0:
    A = np.random.rand(n, m)
else:
    A = None
A = COMM.bcast(A, root=0)


counts = [n // SIZE] * SIZE


displs = [sum(counts[:i]) for i in range(SIZE)]
recv_buf = np.empty((counts[RANK], m), dtype=np.float64)
COMM.Scatterv([A, counts, displs, MPI.DOUBLE], recv_buf, root=0)


print("I am the rank", rank, "I got", reecv_buf)
