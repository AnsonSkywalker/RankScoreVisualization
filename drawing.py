import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
from datetime import datetime
from matplotlib.dates import DateFormatter, HourLocator, date2num
from scipy.interpolate import make_interp_spline

def get_desktop_path():
    """获取Windows桌面路径"""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def select_csv_file():
    """选择现有的记录文件"""
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    if not csv_files:
        print("没有找到CSV文件。")
        sys.exit(1)
        
    print("可用的CSV文件：")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
        
    while True:
        try:
            choice = input("请输入要打开的文件编号（或输入q退出）：").strip()
            if choice.lower() == 'q':
                sys.exit(0)
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(csv_files):
                return csv_files[choice_idx]
            else:
                print("错误：请输入有效的文件编号！")
        except ValueError:
            print("错误：请输入一个数字！")

def load_csv(filename=None):
    if filename is None:
        filename = select_csv_file()
    
    times = []
    scores = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                time_str, score = row
                time_obj = datetime.strptime(time_str, "%Y-%m-%d-%H-%M")
                times.append(time_obj)
                scores.append(int(score))
        return filename, times, scores
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到。")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时出错：{e}")
        sys.exit(1)

def set_chinese_font():
    try:
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        try:
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
        except:
            try:
                font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
                font_prop = FontProperties(fname=font_path)
                plt.rcParams['font.family'] = font_prop.get_name()
                plt.rcParams['axes.unicode_minus'] = False
            except:
                print("警告: 无法找到合适的中文字体，中文显示可能不正常")

def plot_by_session(filename, times, scores, smooth_curve=True):
    set_chinese_font()
    x = np.arange(len(times))
    labels = []
    prev_date = None
    for time in times:
        current_date = time.date()
        if current_date != prev_date:
            labels.append(time.strftime("%Y年%m月%d日\n%H:%M"))
            prev_date = current_date
        else:
            labels.append(time.strftime("%H:%M"))
    
    plt.figure(figsize=(12, 6))
    
    # 绘制平滑曲线或普通折线
    if smooth_curve and len(times) > 3:
        x_smooth = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, scores, k=3)
        scores_smooth = spl(x_smooth)
        plt.plot(x_smooth, scores_smooth, '-', color='blue', linewidth=2)
    else:
        plt.plot(x, scores, '-', color='blue', linewidth=2)
    
    # 绘制原始数据点
    plt.plot(x, scores, 'o', color='blue', markersize=6)
    
    # 添加分数标签
    for i, score in enumerate(scores):
        plt.text(x[i], score + 0.5, str(score), 
                ha='center', va='bottom', fontsize=9, color='black')
    
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.xlabel('场次 ')
    plt.ylabel('分数')
    plt.title(f'上分趋势 (按场次) - {"平滑" if smooth_curve else "折线"}模式')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 保存图像到桌面
    desktop_path = get_desktop_path()
    base_name = os.path.splitext(os.path.basename(filename))[0]
    save_name = f"{base_name}_场次_{'平滑' if smooth_curve else '折线'}.png"
    save_path = os.path.join(desktop_path, save_name)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"图像已保存到桌面: {save_path}")
    
    plt.show()

def plot_by_time(filename, times, scores, smooth_curve=True):
    set_chinese_font()
    plt.figure(figsize=(12, 6))
    
    dates_num = date2num(times)
    
    # 绘制平滑曲线或普通折线
    if smooth_curve and len(times) > 3:
        dates_num_smooth = np.linspace(dates_num.min(), dates_num.max(), 300)
        spl = make_interp_spline(dates_num, scores, k=3)
        scores_smooth = spl(dates_num_smooth)
        plt.plot(dates_num_smooth, scores_smooth, '-', color='blue', linewidth=2)
    else:
        plt.plot(dates_num, scores, '-', color='blue', linewidth=2)
    
    # 绘制原始数据点
    plt.plot(dates_num, scores, 'o', color='blue', markersize=6)
    
    # 添加分数标签
    for date, score in zip(times, scores):
        plt.text(date2num([date])[0], score + 0.5, str(score),
                ha='center', va='bottom', fontsize=9, color='black')
    
    ax = plt.gca()
    
    # 生成需要显示的整点时间标记
    hour_ticks = []
    prev_hour = None
    prev_date = None
    
    # 找到数据时间范围内的所有整点
    for time in times:
        current_date = time.date()
        current_hour = time.replace(minute=0, second=0, microsecond=0)
        
        if prev_date != current_date or (prev_hour is None or current_hour != prev_hour):
            hour_ticks.append(current_hour)
            prev_hour = current_hour
            prev_date = current_date
    
    # 生成标签（每天第一个整点显示日期）
    hour_labels = []
    prev_date = None
    for h in hour_ticks:
        current_date = h.date()
        if current_date != prev_date:
            hour_labels.append(h.strftime("%Y年%m月%d日\n%H:%M"))
            prev_date = current_date
        else:
            hour_labels.append(h.strftime("%H:%M"))
    
    # 设置x轴刻度
    ax.set_xticks(date2num(hour_ticks))
    ax.set_xticklabels(hour_labels, rotation=45, ha='right')
    
    plt.xlabel('时间')
    plt.ylabel('分数')
    plt.title(f'上分趋势 (按时间) - {"平滑" if smooth_curve else "折线"}模式')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 保存图像到桌面
    desktop_path = get_desktop_path()
    base_name = os.path.splitext(os.path.basename(filename))[0]
    save_name = f"{base_name}_时间_{'平滑' if smooth_curve else '折线'}.png"
    save_path = os.path.join(desktop_path, save_name)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"图像已保存到桌面: {save_path}")
    
    plt.show()

def main():
    print("图像绘制程序")
    # 自动列出并选择CSV文件
    filename, times, scores = load_csv()
    
    mode = input("请选择横轴模式（输入1或2）：\n1. 场次\n2. 时间\n")
    
    # 平滑曲线/折线模式选择
    smooth_mode = input("请选择曲线类型（输入1或2）：\n1. 平滑曲线\n2. 折线\n")
    smooth_curve = (smooth_mode == '1')
    
    if mode == '1':
        plot_by_session(filename, times, scores, smooth_curve)
    elif mode == '2':
        plot_by_time(filename, times, scores, smooth_curve)
    else:
        print("无效的选择，请输入1或2。")

if __name__ == "__main__":
    main()