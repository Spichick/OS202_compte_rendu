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

scaleX = 3.0 / width
scaleY = 2.25 / height

if rank == 0:
    # Master Process: Task Distribution
    task_queue = list(range(height))
    results = {}
    start_time = time.time()
    active_workers = min(size - 1, height)  # 确保不会超出进程数

    # 分发任务给工作进程
    for i in range(1, active_workers + 1):
        row = task_queue.pop(0)
        comm.send(row, dest=i, tag=1)
    
    while active_workers > 0:
        source, (row, data) = comm.recv(source=MPI.ANY_SOURCE, tag=2)
        results[row] = data
        if task_queue:
            next_row = task_queue.pop(0)
            comm.send(next_row, dest=source, tag=1)
        else:
            comm.send(None, dest=source, tag=0)
            active_workers -= 1
    
    end_time = time.time()
    final_convergence = np.zeros((height, width), dtype=np.double)
    for row, data in results.items():
        final_convergence[row] = data
    
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(final_convergence) * 255))
    image.save("Q1_3.png")
else:
    # Slave Processes: Compute and return data
    local_start_time = time.time()
    while True:
        row = comm.recv(source=0, tag=MPI.ANY_TAG)
        if row is None:
            break
        
        data = np.empty(width, dtype=np.double)
        for x in range(width):
            c = complex(-2.0 + scaleX * x, -1.125 + scaleY * row)
            data[x] = mandelbrot_set.convergence(c, smooth=True)
        
        comm.send((rank, (row, data)), dest=0, tag=2)
    local_end_time = time.time()
    print(f"Process {rank} finished in {local_end_time - local_start_time:.4f} seconds.")
