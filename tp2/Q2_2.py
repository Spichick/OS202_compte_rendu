from mpi4py import MPI
import numpy as np

# 初始化 MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 设定矩阵和向量的维度（必须能被任务数整除）
dim = 1200  

# 计算每个进程负责的行数
Nloc = dim // size

# 进程 0 生成完整矩阵和向量
if rank == 0:
    A = np.array([[(i + j) % dim + 1. for j in range(dim)] for i in range(dim)])  # 生成矩阵
    u = np.array([i + 1. for i in range(dim)])  # 生成向量
else:
    A = None
    u = np.zeros(dim)

# 广播向量 u（所有进程都需要整个 u）
comm.Bcast(u, root=0)

# 每个进程创建自己存储的局部矩阵
local_A = np.zeros((Nloc, dim))

# 进程 0 分发矩阵行数据
if rank == 0:
    for i in range(size):
        if i == 0:
            local_A[:, :] = A[i * Nloc:(i + 1) * Nloc, :]  # 直接赋值给 rank 0
        else:
            comm.Send(A[i * Nloc:(i + 1) * Nloc, :], dest=i, tag=i)
else:
    comm.Recv(local_A, source=0, tag=rank)

# 记录开始时间
start_time = MPI.Wtime()

# 计算局部矩阵-向量乘法
local_v = np.dot(local_A, u)  # (Nloc, dim) * (dim,) -> (Nloc,)

# 收集所有部分结果，形成完整的 v
v = np.zeros(dim)
comm.Allgather(local_v, v)

# 记录结束时间
end_time = MPI.Wtime()
elapsed_time = end_time - start_time

# 进程 0 输出结果
if rank == 0:
    print(f"并行计算的 v = {v}")
    print(f"运行时间: {elapsed_time:.6f} 秒")
