import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体（Windows系统自带）
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.style.use('ggplot')  # 用Matplotlib内置样式（无需安装）

# 加载数据
df = pd.read_csv('tensile_test.csv', encoding='gbk')  # 适用于中文Windows生成的CSV
# 试样参数
original_length = 50  # 标距长度 (mm)
cross_area = 78.5     # 截面积 (mm²)

# 计算工程应力应变
df['工程应变'] = df['位移(mm)'] / original_length
df['工程应力(MPa)'] = df['载荷(N)'] / cross_area

# 绘制曲线
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df['工程应变'], df['工程应力(MPa)'], 
        linewidth=1.5, 
        color='#2E86C1',
        label='工程应力-应变曲线')

# 标注抗拉强度
max_stress = df['工程应力(MPa)'].max()
max_strain = df.loc[df['工程应力(MPa)'].idxmax(), '工程应变']
ax.scatter(max_strain, max_stress, c='red', zorder=5)
ax.annotate(f'抗拉强度: {max_stress:.1f}MPa', 
           xy=(max_strain, max_stress),
           xytext=(max_strain+0.02, max_stress*0.9),
           arrowprops=dict(arrowstyle='->'))

# 图表设置
ax.set_xlabel('工程应变', fontsize=12)
ax.set_ylabel('工程应力 (MPa)', fontsize=12)
ax.set_title('材料拉伸试验曲线', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

plt.show()
