import numpy as np
import time

def calculate_mflops(matrix_size):
    # 生成随机矩阵
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)

    # 记录开始时间
    start_time = time.time()

    # 进行矩阵乘法
    C = np.dot(A, B)

    # 记录结束时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time

    # 计算 MFlops (百万浮点运算每秒)
    mflops = (2.0 * matrix_size ** 3) / elapsed_time / 1000000

    return elapsed_time, mflops

# 设置矩阵的维度
matrix_size = 20480  # 可以更改为 512、1024、4096 等其他值

# 计算时间和 MFlops
elapsed_time, mflops = calculate_mflops(matrix_size)

# 输出结果
print(f"矩阵尺寸: {matrix_size}x{matrix_size}")
print(f"运算时间: {elapsed_time:.6f} 秒")
print(f"MFlops: {mflops:.2f} MFlops")
