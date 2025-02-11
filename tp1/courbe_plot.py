import matplotlib.pyplot as plt
import numpy as np

# OMP_NUM 和 MFlops 数据
OMP_NUM = [1, 2, 3, 4, 5, 6, 7, 8]
MFlops_2048 = [606.798, 864.573, 613.113, 592.328, 616.738, 542.057, 562.063, 565.705]
MFlops_512 = [2853.74, 2326.51, 2761.13, 2303.73, 2784.53, 2458.84, 2932.34, 2225.78]
MFlops_4096 = [426.883, 425.539, 394.406, 371.406, 345.51, 146.577, 132.925, 132.347]
MFlops_1024 = [942.677, 929.505,908.884,878.446,927.929,940.5,965.041, 955.735]
# 计算加速比
speedup_512 = [1/MFlops_512[0] * mflop for mflop in MFlops_512]
speedup_1024 = [1/MFlops_1024[0] * mflop for mflop in MFlops_1024]
speedup_2048 = [1/MFlops_2048[0] * mflop for mflop in MFlops_2048]
speedup_4096 = [1/MFlops_4096[0] * mflop for mflop in MFlops_4096]
# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(OMP_NUM, speedup_512, label='n=512', marker='o', linestyle='-', color='g')
plt.plot(OMP_NUM, speedup_1024, label='n=1024', marker='o', linestyle='-', color='y')   
plt.plot(OMP_NUM, speedup_2048, label='n=2048', marker='o', linestyle='-', color='b')
plt.plot(OMP_NUM, speedup_4096, label='n=4096', marker='o', linestyle='-', color='r')

# 设置图表标题和标签
plt.title("Speedup vs. Number of Threads (OMP_NUM)", fontsize=14)
plt.xlabel("Number of Threads (OMP_NUM)", fontsize=12)
plt.ylabel("Speedup", fontsize=12)
# 设置图例
plt.legend()

# 显示图表
plt.grid(True)

plt.savefig("speedup.png")
plt.show()

