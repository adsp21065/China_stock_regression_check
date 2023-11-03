import pandas as pd
import csv
import heapq
import configparser
def find_top_20_max_values_and_first_elements(csv_file, column_index):
    # 打开CSV文件
    with open(csv_file, "r",encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行，如果有的话

        # 初始化一个最小堆，用于保持前20个最大值及其对应行的第一个元素
        top_20_max_values = []
        heapq.heapify(top_20_max_values)

        # 迭代每一行
        for row in reader:
            try:
                current_value = float(row[column_index])  # 将列的值转换为浮点数
                if len(top_20_max_values) < 20 or current_value > top_20_max_values[0][0]:
                    if len(top_20_max_values) == 20:
                        heapq.heappop(top_20_max_values)
                    heapq.heappush(top_20_max_values, (current_value, row[0]))  # 保存最大值及其对应行的第一个元素
                    #print(current_value,row[0])
            except (ValueError, IndexError):
                # 忽略无法转换为浮点数的行或索引错误
                pass

    # 将堆中的元素按降序排列
    top_20_max_values.sort(reverse=True, key=lambda x: x[0])

    return top_20_max_values


def compare_csv_files(file1_path, file2_path):
    try:
        df1 = pd.read_csv(file1_path)
        #print(df1.shape,file2_path)
        df2 = pd.read_csv(file2_path)
        line1,row1=(df2.shape)
        line2,row2=(df2.shape)
        if line1==line2:
            return True
        else:
            return False
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return False

def merge_large_csv_files_with_selected_columns(input_file1, input_file2, output_file, columns_to_select1,columns_to_select2):
    chunk_size = 10000  # 每次读取的行数

    # 打开输出文件以准备写入
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)

        # 写入文件头
        with open(input_file1, 'r', newline='') as file1:
            reader = csv.reader(file1)
            header = next(reader)
            writer.writerow(header)

        # 逐块读取并写入数据
        for chunk_start in range(0, max(sum(1 for _ in open(input_file1,encoding='utf-8')), sum(1 for _ in open(input_file2,encoding='utf-8'))), chunk_size):
            with open(input_file1, 'r', newline='',encoding='utf-8') as file1, open(input_file2, 'r', newline='',encoding='utf-8') as file2:
                reader1 = csv.reader(file1)
                reader2 = csv.reader(file2)

                # 跳过文件头
                next(reader1)
                next(reader2)

                # 跳过文件1的数据
                for _ in range(chunk_start):
                    next(reader1)

                # 读取数据块
                for i in range(chunk_size):
                    try:
                        row1 = next(reader1)
                        row2 = next(reader2)
                        selected_data1 = [row1[i] for i in columns_to_select1]
                        selected_data2 = [row2[i] for i in columns_to_select2]
                        result = float(selected_data2[0])/float(selected_data1[1]) 
                        print(selected_data1,selected_data2,result)
                        combined_data = selected_data1 + selected_data2+[result]
                        writer.writerow(combined_data)
                    except StopIteration:
                        break

def combin_name_today_price_and_history_value():
    config=configparser.ConfigParser()
    config.read("../config.ini",encoding='utf-8-sig')
    if config.has_section('stock_list_configure'):
       file_path_list = config.get("stock_list_configure","STOCK_LIST_NAME")
    else:
        file_path_list = ['Shenzhen_stock_list.xlsx','Shanghai_stock_list.xls'] # READ STOCK LIST
    for file_path in file_path_list:
        # 指定要选择的列的位置
        columns_to_select1 = [0, 1]  # 从文件1选择的列的位置
        columns_to_select2 = [ 4]  # 从文件2选择的列的位置

        # 调用函数来合并CSV文件并选择指定列
        price_path=f'price_{file_path.split(".")[0]}.csv'
        sum_file_path=f'found_data_{file_path.split(".")[0]}.csv'
        merger_file=f'merged_{file_path.split(".")[0]}.csv'
        
        if(compare_csv_files(price_path,sum_file_path)):
            merge_large_csv_files_with_selected_columns(price_path, sum_file_path, merger_file,columns_to_select1, columns_to_select2)
        

def find_top_20_better_value(csv_file,column_index):
    better_list=[]
    # 调用函数并传递CSV文件路径和列索引
    
    
    top_20_max_values = find_top_20_max_values_and_first_elements(csv_file, column_index)

    # 输出前20个最大值及其对应行的第一个元素
    for i, (max_value, first_element) in enumerate(top_20_max_values):
        print(f"第 {i+1} 个最大值：{max_value}, 对应行的第一个元素：{first_element}")
        better_list.append(first_element.zfill(6)[:6])
    return better_list


if __name__ == '__main__':
    #combin_name_today_price_and_history_value()
    
    csv_file = "found_data_for_shanghai.csv"  # 请替换为你的CSV文件路径
    column_index = 4  # 替换为你要查找最大值的列的索引
    better_list_sh=find_top_20_better_value(csv_file,column_index)
    
    column_index = 22  # 替换为你要查找最大值的列的索引
    better_list_sh_cmp=find_top_20_better_value(csv_file,column_index)
    
    csv_file = "found_data_for_shenzheng.csv"  # 请替换为你的CSV文件路径
    column_index = 4  # 替换为你要查找最大值的列的索引
    better_list_sz=find_top_20_better_value(csv_file,column_index)

    csv_file = "found_data_for_shenzheng.csv"  # 请替换为你的CSV文件路径
    column_index = 22 # 替换为你要查找最大值的列的索引
    better_list_sz_cmp=find_top_20_better_value(csv_file,column_index)


    print(better_list_sh)
    print(better_list_sh_cmp)
    print(better_list_sz)
    print(better_list_sz_cmp)
    # 将列表转换为集合
    set1 = set(better_list_sh)
    set2 = set(better_list_sh_cmp)

    # 检查两个集合是否有交集
    if set1 & set2:
        common_elements = set1 & set2
        print("这两个列表有共同的元素:")
        print(common_elements)
    else:
        print("这两个列表没有共同的元素")
    # 将列表转换为集合
    set1 = set(better_list_sz)
    set2 = set(better_list_sh_cmp)

    # 检查两个集合是否有交集
    if set1 & set2:
        common_elements = set1 & set2
        print("这两个列表有共同的元素:")
        print(common_elements)
    else:
        print("这两个列表没有共同的元素")


    
