#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <time.h>

int main(int argc, char* argv[]) {
    int rank, size;
    long num_points = 1000000;  // 每个进程生成的点数
    long num_inside = 0;
    long total_points_inside = 0;
    double x, y, pi;
    double start_time, end_time;

    // 初始化MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // 获取进程的rank
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // 获取总进程数

    // 获取每个进程需要生成的点的数量
    long points_per_process = num_points / size;

    // 计时开始
    start_time = MPI_Wtime();

    // 每个进程计算其分配的点
    for (long i = 0; i < points_per_process; i++) {
        x = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
        y = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
        if (x * x + y * y <= 1.0) {
            num_inside++;
        }
    }

    // 使用MPI_Reduce汇总各进程的结果
    MPI_Reduce(&num_inside, &total_points_inside, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

    // 计时结束
    end_time = MPI_Wtime();

    // 只有rank为0的进程计算和输出结果
    if (rank == 0) {
        pi = (4.0 * total_points_inside) / num_points;
        printf("Approximated pi value: %f\n", pi);
        printf("Time taken: %f seconds\n", end_time - start_time);
    }

    // 结束MPI环境
    MPI_Finalize();

    return 0;
}
