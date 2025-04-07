数据清洗逻辑说明（Data Cleaning Pipeline）
1. 原始数据问题诊断
python
复制
# 检查原始数据
print(f"原始数据量: {len(df)} 行")
print("前5行原始数据:")
print(df.head())
print("\n数据统计描述:")
print(df.describe())
典型问题：

试验机导出的无效表头行（如"Test Date: 2023-01-01"）

异常值（如负位移或超大载荷）

非数值型数据混入（如"ERROR"字符串）

2. 清洗步骤（代码实现）
python
复制
def clean_tensile_data(raw_df):
    """
    参数:
        raw_df: 直接从CSV读取的原始DataFrame
    
    返回:
        清洗后的DataFrame
    """
    # (1) 处理表头问题
    if '位移(mm)' not in raw_df.columns:
        # 自动检测真实表头行（试验机数据常见问题）
        header_row = raw_df[raw_df.iloc[:,0].str.contains('位移', na=False)].index[0]
        raw_df = pd.read_csv('tensile_test.csv', header=header_row, encoding='gbk')
    
    # (2) 列名标准化
    raw_df.columns = raw_df.columns.str.strip()  # 去除空格
    
    # (3) 移除无效行
    df_clean = raw_df.copy()
    df_clean = df_clean.dropna(subset=['位移(mm)', '载荷(N)'])  # 删除关键列缺失的行
    
    # (4) 类型转换
    df_clean = df_clean.apply(pd.to_numeric, errors='coerce')  # 非数值转为NaN
    
    # (5) 物理合理性过滤
    df_clean = df_clean[
        (df_clean['位移(mm)'] >= 0) &  # 位移不能为负
        (df_clean['载荷(N)'] >= 0) &   # 载荷不能为负
        (df_clean['位移(mm)'] < 100)   # 假设标距50mm，断裂伸长率<100%
    ]
    
    # (6) 噪声数据平滑（可选）
    df_clean['载荷(N)'] = df_clean['载荷(N)'].rolling(5, center=True).mean()
    
    return df_clean.dropna()
3. 清洗效果验证
python
复制
# 可视化对比
plt.figure(figsize=(12,6))
plt.subplot(121)
plt.plot(raw_df['位移(mm)'], raw_df['载荷(N)'], 'r-', alpha=0.5, label='原始数据')
plt.title('清洗前')
plt.subplot(122)
plt.plot(clean_df['位移(mm)'], clean_df['载荷(N)'], 'b-', label='清洗后')
plt.title('清洗后')
plt.tight_layout()
plt.show()
4. 关键清洗逻辑说明
步骤	处理内容	技术实现	目的
表头检测	跳过试验机生成的说明行	header=header_row	避免非数据行干扰
类型转换	强制转为数值型	pd.to_numeric()	处理混入的文本错误
物理过滤	移除负值/异常值	布尔索引	保证数据符合材料力学规律
数据平滑	滑动平均降噪	.rolling().mean()	消除传感器抖动
5. 异常处理建议
python
复制
try:
    df = clean_tensile_data(pd.read_csv('tensile_test.csv'))
except Exception as e:
    print(f"清洗失败: {str(e)}")
    # 保存原始数据供调试
    with open('raw_error_data.txt', 'w') as f:
        f.write(open('tensile_test.csv').read())
