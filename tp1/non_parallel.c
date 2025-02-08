#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main() {
    long num_points = 1000000;
    long num_inside = 0;
    double x, y, pi;

    // 随机生成点并统计落在单位圆内的点数
    for (long i = 0; i < num_points; i++) {
        x = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
        y = (double)rand() / RAND_MAX * 2.0 - 1.0;  // [-1, 1] 范围内的随机数
        if (x * x + y * y <= 1.0) {
            num_inside++;
        }
    }

    // 计算 pi 值
    pi = (4.0 * num_inside) / num_points;
    printf("Approximated pi value: %f\n", pi);

    return 0;
}
