from mpi4py import MPI
import numpy as np

# If you use imbalanced data, you'll see that process 0 spends a lot more time sorting than the other processes.
imb_data = True

def bucket_sort(arr):
    if len(arr) == 0:
        return arr
    return sorted(arr)  

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# dataset
if rank == 0:
    num_elements = 5000
    data = [np.random.uniform(0, 1) for _ in range(num_elements)]
    
    if (imb_data==True):
        # imb_data
        for i in range(size - 1):
            data = np.array(data) ** 4 
            data = data.tolist()
else:
    data = None
 

# 计算全局最小值和最大值
min_val = comm.reduce(min(data) if rank == 0 else float('inf'), op=MPI.MIN, root=0)
max_val = comm.reduce(max(data) if rank == 0 else float('-inf'), op=MPI.MAX, root=0)

# 广播最小值和最大值给所有进程
min_val = comm.bcast(min_val, root=0)
max_val = comm.bcast(max_val, root=0)

# 划分等间距的桶
buckets = np.linspace(min_val, max_val, size + 1)
bucket_data = [[] for _ in range(size)]

if rank == 0:
    for num in data:
        # 计算该数据应该放入哪个桶
        index = np.digitize(num, buckets) - 1
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

if rank == 0:
    final_data = [num for sublist in gathered_data for num in sublist]
    
    print("Sorted Data (First 100 elements for verification):")
    print(final_data[:100])
    
    print("\nExecution Time for Each Process:")
    for i in range(size):
        print(f"Process {i}: {all_times[i]:.6f} seconds")
