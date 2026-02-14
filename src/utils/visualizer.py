import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体，解决乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_evolution_charts(csv_path, output_dir):
    """
    增强版演化规律可视化 (2x2 布局)
    分析维度：维护类型、活跃趋势、贡献者分布、工作习惯
    """
    if not os.path.exists(csv_path):
        print(f"错误: 未找到数据文件 {csv_path}")
        return

    # 1. 加载并预处理数据
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    # 提取周几 (0=周一, 6=周日)
    df['weekday'] = df['date'].dt.weekday 
    
    # 设置绘图风格
    plt.style.use('ggplot')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # --- 图 1：提交类别分布 (左上) ---
    plt.subplot(2, 2, 1)
    counts = df['category'].value_counts()
    counts.plot.pie(
        autopct='%1.1f%%', 
        startangle=140, 
        cmap='Pastel1',
        explode=[0.05] * len(counts) # 增加轻微裂开效果
    )
    plt.title("Flask 项目维护任务类型分布", fontsize=14, pad=15)
    plt.ylabel("")

    # --- 图 2：开发活跃度趋势 (右上) ---
    plt.subplot(2, 2, 2)
    df_resampled = df.resample('ME', on='date').size()
    df_resampled.plot(kind='line', marker='o', color='#3498db', linewidth=2)
    plt.fill_between(df_resampled.index, df_resampled.values, color='#3498db', alpha=0.2)
    plt.title("Flask 提交频率演化趋势 (按月)", fontsize=14, pad=15)
    plt.xlabel("年份")
    plt.ylabel("提交数量")

    # --- 图 3：核心开发者贡献排行 (左下) ---
    plt.subplot(2, 2, 3)
    # 统计前 10 名活跃开发者
    top_authors = df['author'].value_counts().head(10)
    top_authors.plot(kind='bar', color='#2ecc71')
    plt.title("核心开发者贡献 Top 10", fontsize=14, pad=15)
    plt.xlabel("开发者名称")
    plt.ylabel("提交次数")
    plt.xticks(rotation=45)

    # --- 图 4：开发者工作习惯分析 (右下) ---
    plt.subplot(2, 2, 4)
    weekday_counts = df['weekday'].value_counts().sort_index()
    weekday_labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    # 确保 0-6 都有数据，防止因采样少导致的索引缺失
    weekday_counts = weekday_counts.reindex(range(7), fill_value=0)
    
    weekday_counts.plot(kind='bar', color='#e67e22')
    plt.title("开发者工作习惯分布 (周内活跃度)", fontsize=14, pad=15)
    plt.xticks(range(7), weekday_labels, rotation=0)
    plt.xlabel("星期")
    plt.ylabel("提交总数")

    # 保存与展示
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plot_path = os.path.join(output_dir, "evolution_charts.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"增强版分析图表已保存至: {plot_path}")
    
    # 如果在非交互模式下运行，可以注释掉 plt.show()
    # plt.show()

if __name__ == "__main__":
    # 测试用代码
    plot_evolution_charts("../../data/processed/flask_history.csv", "../../data/output")