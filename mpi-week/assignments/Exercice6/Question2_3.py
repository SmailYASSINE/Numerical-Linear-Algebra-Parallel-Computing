from mpi4py import MPI
import math
import numpy as np

N = 840
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def calcul_pi(Ni, start, end):
    local_pi = 0.0
    for i in range(start, end):
        local_pi += 1.0 / (1.0 + ((i-0.5)/N)**2)
    return 4*local_pi/N

#                                                 Question 2 & 3:





numbers_per_rank = N/size

# in case N is not divisible by the number of rank, we then add the rest of the division(modulo) to the number per rank.
if N  % size > 0:
    numbers_per_rank += 1

 
# set the ranges for each processor
my_first = rank * numbers_per_rank
my_last = my_first + numbers_per_rank
# here we compare if our last value exceeds N we affect it value of N for example if we take N =841 and number of processrsor n=4 
# the first 3 processors calculate pi for N= 211(iterations) and the last processor calculate for N=208 and without this conditioning, we will be exceeding our expected number N.
if my_last>N:
    my_last=N


start_time = MPI.Wtime()
# apply the calcul_pi for the given start and end of each processor
my_pi = calcul_pi(N, my_first, my_last)

print(my_pi)

# apply the global reduction function and use the sum function to sum the values calculated by each processor
pi = comm.reduce(my_pi, op=MPI.SUM, root=0)
end_time = MPI.Wtime()

if rank ==0:
    print("Using reduce function we get", pi)
    print("elapsed time for pi calculation is:", end_time - start_time)

