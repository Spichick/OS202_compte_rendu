from mpi4py import MPI
import random
import time

def calculate_pi(num_points):
    num_inside = 0
    for _ in range(num_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            num_inside += 1
    return num_inside

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    num_points = 1000000  # 总点数
    points_per_process = num_points // size  # 每个进程处理的点数

    # 计时开始
    start_time = time.time()

    # 每个进程计算它自己的部分
    num_inside = calculate_pi(points_per_process)

    # 汇总所有进程的结果
    total_inside = comm.reduce(num_inside, op=MPI.SUM, root=0)

    # 计时结束
    end_time = time.time()

    # 只有进程0输出结果
    if rank == 0:
        pi = 4 * total_inside / num_points
        print(f"Approximated pi value: {pi}")
        print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
