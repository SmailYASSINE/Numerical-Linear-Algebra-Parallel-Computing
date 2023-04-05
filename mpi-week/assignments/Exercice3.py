from mpi4py import MPI

# Initialize MPI and get the rank and size of the current process
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


while(1):
    if rank==0:
        x=int(input())
        comm.send(x, rank+1)

    else:
        x = comm.recv(source = rank-1)
        if rank< size - 1:
            if x < 0:
                x -= rank
            comm.send(x + rank, rank+1)
    if x < 0:
        break
    print("rank", rank, "data", x)
