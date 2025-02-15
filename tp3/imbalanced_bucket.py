from mpi4py import MPI
import numpy as np

def bucket_sort(arr):
    if len(arr) == 0:
        return arr
    return sorted(arr)  

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
def dataset_imb():
    # dataset
    if rank == 0:
        num_elements = 5000
        data = [np.random.uniform(0, 1) for _ in range(num_elements)]

        # imb_data
        for i in range(size - 1):
            data = np.array(data) ** 4 
            data = data.tolist()

    else:
        data = None
    return data

data = dataset_imb()
# 确保每个进程都有数据
data = comm.bcast(data, root=0)  # 广播数据到所有进程

# 计算局部最小值和最大值
local_min = np.min(data)  
local_max = np.max(data)

# 使用reduce操作，确保所有进程都可以知道全局的min和max值
min_val = comm.reduce(local_min, op=MPI.MIN, root=0)
max_val = comm.reduce(local_max, op=MPI.MAX, root=0)

# 广播全局的最小值和最大值给所有进程
min_val = comm.bcast(min_val, root=0)
max_val = comm.bcast(max_val, root=0)

# 计算分位数（即每个桶的边界），这里直接使用全局的min和max值
# 进程0会负责计算分位数的值，其他进程接收到这些值
if rank == 0:
    quantiles = np.percentile(data, np.linspace(0, 100, size + 1))  # size+1 个分位数
else:
    quantiles = None

quantiles = comm.bcast(quantiles, root=0)  # 广播分位数到所有进程

# 将数据分配到各个桶
bucket_data = [[] for _ in range(size)]

for num in data:
    # 计算该数据应该放入哪个桶
    index = np.digitize(num, quantiles) - 1
    if index == size:  # 确保最大值不会超出桶的范围
        index -= 1
    bucket_data[index].append(num)

# 使用scatter将每个进程的桶数据发送出去
local_data = comm.scatter(bucket_data, root=0)

# timer
start_time = MPI.Wtime()
sorted_local_data = bucket_sort(local_data)
end_time = MPI.Wtime()
execution_time = end_time - start_time

# gather
gathered_data = comm.gather(sorted_local_data, root=0)
all_times = comm.gather(execution_time, root=0)

bins = [0, 1e-1, 2e-1, 3e-1, 4e-1, 5e-1, 6e-1, 7e-1, 8e-1, 9e-1, 1]

if rank == 0:
    final_data = [num for sublist in gathered_data for num in sublist]

    hist, bin_edges = np.histogram(final_data, bins=bins)
    for i in range(len(hist)):
        print(f"Interval [{i}]: {hist[i]} datas")
        
    print("\nExecution Time for Each Process:")
    for i in range(size):
        print(f"Process {i}: {all_times[i]:.6f} seconds")
