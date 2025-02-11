<<<<<<< HEAD
from mpi4py import MPI
import numpy as np

# 初始化 MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 设定矩阵和向量的维度（必须能被任务数整除）
dim = 1200

# 计算每个任务负责的列数
Nloc = dim // size

# 初始化局部矩阵和向量
local_A = np.zeros((dim, Nloc))
if rank == 0:
    # 生成完整矩阵
    A = np.array([[(i + j) % dim + 1. for i in range(dim)] for j in range(dim)])
    u = np.array([i + 1. for i in range(dim)])
else:
    A = None
    u = np.zeros(dim)

# 广播向量 u 给所有进程
comm.Bcast(u, root=0)

# 进程 0 按列块分发矩阵
if rank == 0:
    for i in range(size):
        if i == 0:
            local_A[:, :] = A[:, i * Nloc:(i + 1) * Nloc]  # 直接赋值给 rank 0
        else:
            comm.Send(np.ascontiguousarray(A[:, i * Nloc:(i + 1) * Nloc]), dest=i, tag=i)
else:
    comm.Recv(local_A, source=0, tag=rank)

# 记录开始时间
start_time = MPI.Wtime()

# 计算局部矩阵-向量乘积
local_u = u[rank * Nloc:(rank + 1) * Nloc]  # 取出该进程需要的向量部分
local_v = np.dot(local_A, local_u)  # 矩阵(120,30) * 向量(30,) -> 结果 (120,)

# 计算全局结果
v = np.zeros(dim)
comm.Allreduce(local_v, v, op=MPI.SUM)

# 记录结束时间
end_time = MPI.Wtime()
elapsed_time = end_time - start_time

if rank == 0:
    print(f"并行计算的 v = {v}")
    print(f"运行时间: {elapsed_time:.6f} 秒")
=======
from mpi4py import MPI
import numpy as np

# 初始化 MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 设定矩阵和向量的维度（必须能被任务数整除）
dim = 1200

# 计算每个任务负责的列数
Nloc = dim // size

# 初始化局部矩阵和向量
local_A = np.zeros((dim, Nloc))
if rank == 0:
    # 生成完整矩阵
    A = np.array([[(i + j) % dim + 1. for i in range(dim)] for j in range(dim)])
    u = np.array([i + 1. for i in range(dim)])
else:
    A = None
    u = np.zeros(dim)

# 广播向量 u 给所有进程
comm.Bcast(u, root=0)

# 进程 0 按列块分发矩阵
if rank == 0:
    for i in range(size):
        if i == 0:
            local_A[:, :] = A[:, i * Nloc:(i + 1) * Nloc]  # 直接赋值给 rank 0
        else:
            comm.Send(np.ascontiguousarray(A[:, i * Nloc:(i + 1) * Nloc]), dest=i, tag=i)
else:
    comm.Recv(local_A, source=0, tag=rank)

# 记录开始时间
start_time = MPI.Wtime()

# 计算局部矩阵-向量乘积
local_u = u[rank * Nloc:(rank + 1) * Nloc]  # 取出该进程需要的向量部分
local_v = np.dot(local_A, local_u)  # 矩阵(120,30) * 向量(30,) -> 结果 (120,)

# 计算全局结果
v = np.zeros(dim)
comm.Allreduce(local_v, v, op=MPI.SUM)

# 记录结束时间
end_time = MPI.Wtime()
elapsed_time = end_time - start_time

if rank == 0:
    print(f"并行计算的 v = {v}")
    print(f"运行时间: {elapsed_time:.6f} 秒")
>>>>>>> 48d0b7edac6490e9191898da2a8c61a848f9ff3e
