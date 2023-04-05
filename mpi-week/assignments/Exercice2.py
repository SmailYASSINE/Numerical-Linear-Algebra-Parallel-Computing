from mpi4py import MPI

# Initialize MPI and get the rank and size of the current process
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

while True:
    if rank == 0:
        data = int(input(" choose data to broadcast :"))
    else:
        data = None

    data = comm.bcast(data, root=0)
    if data<0:
        break

    if rank == 0:
        print('Process {} broadcast data:'.format(rank), data)
    else:
        print('Process {} received data:'.format(rank), data)



