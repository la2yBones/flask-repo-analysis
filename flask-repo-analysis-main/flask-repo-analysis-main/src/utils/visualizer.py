import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
def plot_evolution_charts(csv_path, output_dir):
    """生成演化规律图表"""
    if not os.path.exists(csv_path):
        print("未找到数据文件，请先运行 run_all.py")
        return

    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    
    # 设置绘图风格
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 6))

    # 1. 提交类别分布饼图
    plt.subplot(1, 2, 1)
    df['category'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, cmap='Pastel1')
    plt.title("Flask 演化维护类型分布", fontsize=14)
    plt.ylabel("")

    # 2. 随时间变化的提交频率 (按月)
    plt.subplot(1, 2, 2)
    df.resample('ME', on='date').size().plot(kind='line', marker='o', color='skyblue')
    plt.title("Flask 开发活跃度趋势", fontsize=14)
    plt.xlabel("年份")
    plt.ylabel("提交数量")

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "evolution_charts.png")
    plt.savefig(plot_path)
    print(f"图表已保存至: {plot_path}")
    plt.show()