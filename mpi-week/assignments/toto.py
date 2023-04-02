from mpi4py import MPI
COMM = COMM.COMMWORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

print(RANK)
