from mpi4py import MPI
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
import matplotlib.cm
import time

@dataclass
class MandelbrotSet:
    max_iterations:int
    escape_radius:float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z: complex
        iter: int

        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


max_iterations = 50
width, height = 1024, 1024
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Process rank
size = comm.Get_size() 

mandelbrot_set = MandelbrotSet(max_iterations=max_iterations, escape_radius=10)

rows_per_process = height // size
remainder = height % size  # For case non divisible

if rank < remainder:
    start_row = rank * (rows_per_process + 1)
    end_row = start_row + rows_per_process + 1
else:
    start_row = rank * rows_per_process + remainder
    end_row = start_row + rows_per_process

# Mandelbrot calculation
scaleX = 3.0 / width
scaleY = 2.25 / height
local_convergence = np.empty((end_row - start_row, width), dtype=np.double)

start_time = time.time()

for j, y in enumerate(range(start_row, end_row)):
    for x in range(width):
        c = complex(-2.0 + scaleX * x, -1.125 + scaleY * y)
        local_convergence[j, x] = mandelbrot_set.convergence(c, smooth=True)

end_time = time.time()
local_time = end_time - start_time
print(f"Process {rank} finished in {local_time:.4f} seconds.")

# Process 0 gathers all data
if rank == 0:
    final_convergence = np.empty((height, width), dtype=np.double)
else:
    final_convergence = None

# Calculate the data size of each process
sendcounts = np.array(comm.gather(local_convergence.shape[0] * width, root=0))

# Process 0 gathers all data
comm.Gatherv(sendbuf=local_convergence, recvbuf=(final_convergence, sendcounts), root=0)

# Process 0 saves the image
if rank == 0:
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(final_convergence) * 255))
    image.save("Q1_1.png")
