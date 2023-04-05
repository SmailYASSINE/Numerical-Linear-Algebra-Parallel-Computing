from mpi4py import MPI
import math
import numpy as np

N = 840
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#                                                  Question 1 :


def calcul_pi(Ni, start, end):
    local_pi = 0.0
    for i in range(start, end):
        local_pi += 1.0 / (1.0 + ((i-0.5)/N)**2)
    return 4*local_pi/N


if rank ==0:
    print("value of pi got by rank", rank, calcul_pi(N, 1, N+1))

else:
    print("value of pi got by rank", rank, calcul_pi(N, 1, N+1))


