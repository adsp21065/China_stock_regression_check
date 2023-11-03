import pandas as pd
import matplotlib.pyplot as plt

def plot_histogram_from_csv(file_path, column_name, bins=10, x_label="X轴标签", y_label="Y轴标签", title="直方图标题"):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 选择要绘制直方图的列
    data = df[column_name]

    # 绘制直方图
    plt.hist(data, bins=bins)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

# 使用示例
file_path = "data.csv"
column_name = "your_column_name"
plot_histogram_from_csv(file_path, column_name)
