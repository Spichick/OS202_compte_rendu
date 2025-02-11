<<<<<<< HEAD
#include <stdio.h>
#include <mpi.h>

int main(int argc, char* argv[]) {
    int rank, size, token = 1;

    // 初始化MPI环境
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // 获取进程的rank
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // 获取总进程数

    if (rank == 0) {
        // 进程0初始化令牌并发送到进程1
        MPI_Send(&token, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    } else {
        // 其它进程接收令牌，增加令牌值并发送到下一个进程
        if (rank < size - 1) {
            MPI_Recv(&token, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            token++;
            MPI_Send(&token, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
        }
        // 处理最后一个进程
        else {
            MPI_Recv(&token, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            token++;
            MPI_Send(&token, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }

    // 进程0接收最后的令牌并打印
    if (rank == 0) {
        MPI_Recv(&token, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Final token value: %d\n", token);
    }

    // 结束MPI环境
    MPI_Finalize();
    return 0;
}
=======
#include <stdio.h>
#include <mpi.h>

int main(int argc, char* argv[]) {
    int rank, size, token = 1;

    // 初始化MPI环境
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // 获取进程的rank
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // 获取总进程数

    if (rank == 0) {
        // 进程0初始化令牌并发送到进程1
        MPI_Send(&token, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    } else {
        // 其它进程接收令牌，增加令牌值并发送到下一个进程
        if (rank < size - 1) {
            MPI_Recv(&token, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            token++;
            MPI_Send(&token, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
        }
        // 处理最后一个进程
        else {
            MPI_Recv(&token, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            token++;
            MPI_Send(&token, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }

    // 进程0接收最后的令牌并打印
    if (rank == 0) {
        MPI_Recv(&token, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Final token value: %d\n", token);
    }

    // 结束MPI环境
    MPI_Finalize();
    return 0;
}
>>>>>>> 48d0b7edac6490e9191898da2a8c61a848f9ff3e
