from mpi4py import MPI
import numpy as np

def bucket_sort(arr):
    if len(arr) == 0:
        return arr
    min_val, max_val = min(arr), max(arr)
    bucket_size = (max_val - min_val) / len(arr) + 1
    buckets = [[] for _ in range(len(arr))]

    for num in arr:
        index = int((num - min_val) / bucket_size)
        buckets[index].append(num)

    for bucket in buckets:
        bucket.sort()

    return [num for bucket in buckets for num in bucket]

def distribute_data(data, size):
    # 均匀分配
    chunk_size = len(data) // size
    chunks = [data[i * chunk_size:(i + 1) * chunk_size] for i in range(size - 1)]
    chunks.append(data[(size - 1) * chunk_size:])  
    return chunks

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0: # 进程0
    num_elements = 40  
    data = np.random.uniform(0, 100, num_elements).tolist()
    print(f"Data: {data}")

    chunks = distribute_data(data, size)
else:
    chunks = None

# 进程 0 分发数据给其他进程
local_data = comm.scatter(chunks, root=0)

# 各进程执行桶排序
sorted_local_data = bucket_sort(local_data)

# 进程 0 收集排序后的数据
gathered_data = comm.gather(sorted_local_data, root=0)

if rank == 0:
    # 将所有部分合并并最终排序
    final_data = [num for sublist in gathered_data for num in sublist]
    final_sorted_data = bucket_sort(final_data)

    print(f"排序后的数据: {final_sorted_data}")
