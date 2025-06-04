import os
import csv
from datetime import datetime
import sys

def validate_initial_score(score_str):
    """验证初始分数是否为大于零的整数"""
    try:
        score = int(score_str)
        if score > 0:
            return score
        else:
            print("错误：分数必须大于零！")
            return None
    except ValueError:
        print("错误：请输入一个有效的整数！")
        return None

def validate_score_change(change_str):
    """验证分数变化是否为允许的值"""
    allowed_changes = {-20, -10, -5, 0, 20}
    try:
        change = int(change_str)
        if change in allowed_changes:
            return change
        else:
            print("错误：分数变化必须是-20、-10、-5、0或20中的一个！")
            return None
    except ValueError:
        print("错误：请输入一个有效的整数！")
        return None

def check_format(filename):
    """检查并修复文件格式，确保以换行符结尾且无多余空行"""
    try:
        with open(filename, 'r+', newline='') as file:
            lines = file.readlines()
            if not lines:
                return  # 空文件，无需处理
            
            # 移除多余的空行
            cleaned_lines = [line for line in lines if line.strip() != '']
            
            # 确保最后一行以换行符结尾
            if cleaned_lines and not cleaned_lines[-1].endswith('\n'):
                cleaned_lines[-1] = cleaned_lines[-1] + '\n'
            
            # 重新写入文件
            file.seek(0)
            file.writelines(cleaned_lines)
            file.truncate()
    except IOError as e:
        print(f"检查文件格式时出错: {e}")
        sys.exit(1)

def create_new_record():
    """创建新的记录文件"""
    while True:
        filename = input("请输入新记录的文件名（不带.csv扩展名）：").strip()
        if not filename:
            print("错误：文件名不能为空！")
            continue
        
        filename += ".csv"
        if os.path.exists(filename):
            print("错误：文件已存在，请选择其他名称！")
            continue
            
        # 验证初始分数
        while True:
            initial_score = input("请输入起始分数（必须大于零的整数）：").strip()
            validated_score = validate_initial_score(initial_score)
            if validated_score is not None:
                break
                
        # 创建文件并写入初始记录
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                # 写入表头
                writer.writerow(['time', 'score'])
                # 写入初始记录
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
                writer.writerow([timestamp, validated_score])
            print(f"已创建新记录文件: {filename}")
            return filename, validated_score
        except IOError as e:
            print(f"创建文件时出错: {e}")
            sys.exit(1)

def select_existing_record():
    """选择现有的记录文件"""
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    if not csv_files:
        print("没有找到现有的记录文件。")
        return None
        
    print("现有的记录文件：")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
        
    while True:
        try:
            choice = input("请输入要打开的文件编号（或输入q退出）：").strip()
            if choice.lower() == 'q':
                return None
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(csv_files):
                filename = csv_files[choice_idx]
                # 检查并修复文件格式
                check_format(filename)
                # 获取最后一行数据以确定当前分数（跳过表头）
                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    headers = next(reader)  # 跳过表头
                    last_row = None
                    for last_row in reader:
                        pass
                    if last_row:
                        current_score = int(last_row[1])
                        return filename, current_score
            else:
                print("错误：请输入有效的文件编号！")
        except ValueError:
            print("错误：请输入一个数字！")

def work_mode(filename, current_score):
    """工作模式，处理用户输入并记录数据"""
    print("\n进入工作模式。输入分数变化（-20、-10、-5、0或20），或输入'q'退出。")
    print(f"当前分数:{current_score}")
    
    while True:
        change_input = input("请输入分数变化：").strip()
        if change_input.lower() == 'q':
            print("退出工作模式。")
            break
            
        validated_change = validate_score_change(change_input)
        if validated_change is not None:
            # 计算新分数
            new_score = current_score + validated_change
                
            # 记录数据前再次检查文件格式
            check_format(filename)
            
            # 记录数据
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
            try:
                with open(filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, new_score])
                current_score = new_score
                print(f"已记录：时间 {timestamp}, 新分数 {new_score}")
            except IOError as e:
                print(f"写入文件时出错: {e}")
                sys.exit(1)

def main():
    print("//////////数据收集程序//////////")
    print("1. 创建新的记录")
    print("2. 继续先前的记录")
    
    while True:
        choice = input("请键盘输入以选择（1或2）：").strip()
        if choice == '1':
            filename, current_score = create_new_record()
            break
        elif choice == '2':
            result = select_existing_record()
            if result:
                filename, current_score = result
                break
            else:
                print("返回主菜单...")
        else:
            print("错误：请输入1或2！")
    
    if 'filename' in locals():
        work_mode(filename, current_score)

if __name__ == "__main__":
    main()