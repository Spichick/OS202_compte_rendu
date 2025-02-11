from mpi4py import MPI
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
import matplotlib.cm
import time

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex, smooth=False) -> int | float:
        if c.real * c.real + c.imag * c.imag < 0.0625:
            return self.max_iterations
        if (c.real + 1) * (c.real + 1) + c.imag * c.imag < 0.0625:
            return self.max_iterations
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real - 0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5 * (1 - ct.real / max(ctnrm2, 1.E-14)):
                return self.max_iterations

        z = 0
        for iter in range(self.max_iterations):
            z = z * z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z))) / log(2)
                return iter
        return self.max_iterations

# MPI Initialization
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Figure parameters
width, height = 1024, 1024
max_iterations = 50

mandelbrot_set = MandelbrotSet(max_iterations=max_iterations, escape_radius=10)

# Parallel computation using correct interleaved row distribution
scaleX = 3.0 / width
scaleY = 2.25 / height
local_rows = [(i, np.empty(width, dtype=np.double)) for i in range(rank, height, size)]

start_time = time.time()

for i, row in local_rows:
    for x in range(width):
        c = complex(-2.0 + scaleX * x, -1.125 + scaleY * i)
        row[x] = mandelbrot_set.convergence(c, smooth=True)

end_time = time.time()
local_time = end_time - start_time
print(f"Process {rank} finished in {local_time:.4f} seconds.")

# Gather results
all_data = comm.gather(local_rows, root=0)

# Process 0 reconstructs the full image
if rank == 0:
    final_convergence = np.empty((height, width), dtype=np.double)
    for process_rows in all_data:
        for i, row in process_rows:
            final_convergence[i] = row
    
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(final_convergence) * 255))
    image.save("Q1_2.png")
    print("Q1_2.png")
