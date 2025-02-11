#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <time.h>

int main() {
    long num_points = 1000000;
    long num_inside = 0;
    double x, y, pi;

    // 获取线程数
    int num_threads = omp_get_max_threads();
    printf("Running with %d threads\n", num_threads);

    // 计时开始
    double start_time = omp_get_wtime();

    // 使用 OpenMP 并行化循环
    #pragma omp parallel private(x, y) reduction(+:num_inside)
    {
        // 每个线程处理部分循环
        #pragma omp for
        for (long i = 0; i < num_points; i++) {
            x = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
            y = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
            if (x * x + y * y <= 1.0) {
                num_inside++;
            }
        }
    }

    // 计时结束
    double end_time = omp_get_wtime();
    printf("Time taken: %f seconds\n", end_time - start_time);

    // 计算 pi 值
    pi = (4.0 * num_inside) / num_points;
    printf("Approximated pi value: %f\n", pi);

    return 0;
}
