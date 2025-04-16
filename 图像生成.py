import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from matplotlib.dates import DateFormatter, HourLocator
from matplotlib.font_manager import FontProperties

def load_csv(filename):
    times = []
    scores = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            time_str, score = row
            time_obj = datetime.strptime(time_str, "%Y-%m-%d-%H-%M")
            times.append(time_obj)
            scores.append(int(score))
    return times, scores

def set_chinese_font():
    # 尝试使用系统支持的中文字体
    try:
        # Windows系统常见的字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except:
        try:
            # Mac系统常见的字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
        except:
            # 如果以上字体都没有，使用FontProperties指定字体路径
            try:
                font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # 常见Linux字体路径
                font_prop = FontProperties(fname=font_path)
                plt.rcParams['font.family'] = font_prop.get_name()
                plt.rcParams['axes.unicode_minus'] = False
            except:
                print("警告: 无法找到合适的中文字体，中文显示可能不正常")

def plot_by_session(times, scores):
    set_chinese_font()
    
    # 准备x轴数据（均匀分布的场次）
    x = np.arange(len(times))
    
    # 准备x轴标签
    labels = []
    prev_date = None
    for time in times:
        current_date = time.date()
        # 如果是新的一天，显示日期+时间
        if current_date != prev_date:
            labels.append(time.strftime("%Y年%m月%d日\n%H:%M"))
            prev_date = current_date
        else:
            labels.append(time.strftime("%H:%M"))
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, scores, marker='o', linestyle='-')
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.xlabel('场次 (带时间信息)', fontproperties='simhei')
    plt.ylabel('分数', fontproperties='simhei')
    plt.title('分数变化趋势 (按场次)', fontproperties='simhei')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_by_time(times, scores):
    set_chinese_font()
    
    plt.figure(figsize=(12, 6))
    plt.plot(times, scores, marker='o', linestyle='-')
    
    # 设置x轴格式
    ax = plt.gca()
    ax.xaxis.set_major_locator(HourLocator(interval=1))  # 每小时一个主刻度
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    
    # 添加日期标签
    prev_date = None
    for time in times:
        current_date = time.date()
        if current_date != prev_date:
            plt.text(time, min(scores)-5, time.strftime("%Y年%m月%d日"), 
                    rotation=45, ha='right', va='top', fontproperties='simhei')
            prev_date = current_date
    
    plt.xlabel('时间', fontproperties='simhei')
    plt.ylabel('分数', fontproperties='simhei')
    plt.title('分数变化趋势 (按时间)', fontproperties='simhei')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    filename = input("请输入要打开的CSV文件名（例如：data.csv）：")
    
    try:
        times, scores = load_csv(filename)
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到。")
        return
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return
    
    mode = input("请选择横轴模式（输入1或2）：\n1. 场次\n2. 时间\n")
    
    if mode == '1':
        plot_by_session(times, scores)
    elif mode == '2':
        plot_by_time(times, scores)
    else:
        print("无效的选择，请输入1或2。")

if __name__ == "__main__":
    main()