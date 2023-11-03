import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
import pandas as pd
import time
import xlrd
import efinance as ef
import configparser
import os

def read_excel_column_format_string(file_path, column_name):
    try:
        if file_path.lower().endswith('.xls'):
            xls = xlrd.open_workbook(file_path)
            df = pd.read_excel(xls, engine='xlrd')  # 通过指定文件路径来读取Excel文件
        else:
            df = pd.read_excel(file_path)  # 使用默认引擎读取xlsx文件

        if column_name in df.columns:
            selected_column = df[column_name].astype(str)  # 将列数据转换为字符串
            selected_column = selected_column.apply(lambda x: x.zfill(6)[:6])  # 前面补零并保持总长度不超过6
            return selected_column
        else:
            return f"列 '{column_name}' 不存在"
    except Exception as e:
        return str(e)  # 如果出现错误，返回错误信息

def read_excel_column(file_path, column_name):
    try:
        df = pd.read_excel(file_path)  # 通过指定文件路径来读取Excel文件
        if column_name in df.columns:
            selected_column = df[column_name].astype(str)  # 将列数据转换为字符串
            selected_column = selected_column.apply(lambda x: x.zfill(6)[:6])  # 前面补零并保持总长度不超过6
            return selected_column
        else:
            return f"列 '{column_name}' 不存在"
    except Exception as e:
        return str(e)  # 如果出现错误，返回错误信息
    
def find_text_in_table_2(url, target_texts):
    found_data = []  # 用于存储找到的数据

    try:
        # 发送GET请求以获取页面内容
        response = requests.get(url)

        # 检查是否成功获取页面内容
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到所有<tr>元素
            rows = soup.find_all('tr')

            for row in rows:
                # 查找<td>元素中的文本内容
                cells = row.find_all('td')
                cell_texts = [cell.get_text(strip=True) for cell in cells]

                # 检查是否有包含任何目标文本的单元格
                for target_text in target_texts:
                    if any(target_text in cell_text for cell_text in cell_texts):
                        print(cell_texts)
                        data = [cell_texts[0]]  # 第一列是名字
                        data.extend(cell_texts[1:])  # 从第二列开始是数字
                        found_data.append(data)
                        

        else:
            print(f'无法获取页面内容，状态码: {response.status_code}')
    
    except Exception as e:
        print(f'发生错误: {e}')

    return found_data  # 返回找到的数据



def find_text_in_table(url, target_texts):
    found_rows = []  # 用于存储找到的行

    try:
        # 发送GET请求以获取页面内容
        response = requests.get(url)

        # 检查是否成功获取页面内容
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)
            # 找到所有<tr>元素
            rows = soup.find_all('tr')

            # 遍历每一行并查找包含目标文本的行
            for row in rows:
                # 查找<td>元素中的文本内容
                cells = row.find_all('td')
                cell_texts = [cell.get_text(strip=True) for cell in cells]

                # 检查是否有包含任何目标文本的单元格
                if any(target in cell_text for target in target_texts for cell_text in cell_texts):
                    print(cell_texts)
                    found_rows.append(cell_texts)
                else:
                    print('cannot find the data')

        else:
            print(f'无法获取页面内容，状态码: {response.status_code}')
    
    except Exception as e:
        print(f'发生错误: {e}')

    return found_rows  # 返回找到的行

# 函数用于将数据写入Excel文件
def write_to_excel(data, output_file):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for row in data:
        sheet.append(row)

    workbook.save(output_file)
    print(f'数据已写入到 {output_file}')

def write_to_csv(data, output_file,first_flag,search_name):
    with open(output_file, 'a', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # 写入第一行，所有列表的第一个元素
        if(first_flag==0):
            first_row =[item for row in data for item in [row[0], '同比%', '当季环比%']]
            csv_writer.writerow(['name']+ first_row)

        
        # 写入第二行及以后的数据
        second_row =[item for row in data for item in row[1:]]
        csv_writer.writerow([search_name]+second_row)
    
    print(f'数据已写入到 {output_file}')

def write_price_to_csv(data, output_file,first_flag,search_name):
    with open(output_file, 'a', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # 写入第一行，所有列表的第一个元素
        if(first_flag==0):
            csv_writer.writerow(['name']+ ['price'])

        
        # 写入第二行及以后的数据
        
        csv_writer.writerow([search_name]+data)
    
    #print(f'数据已写入到 {output_file}')



def get_stock_f10_value():
    config=configparser.ConfigParser()
    config.read("../config.ini",encoding='utf-8-sig')
    if config.has_section('stock_list_configure'):
       file_path_list = config.get("stock_list_configure","STOCK_LIST_NAME")
    else:
        file_path_list = ['Shenzhen_stock_list.xlsx','Shanghai_stock_list.xls'] # READ STOCK LIST
    for file_path in file_path_list:
        column_name = 'A股代码'
        checklist=[]
        selected_data = read_excel_column_format_string(file_path, column_name)
        #selected_data = read_excel_column(file_path, column_name)
        if isinstance(selected_data, pd.Series):
            print(f"成功读取列 '{column_name}' 的数据:")
            checklist=selected_data.tolist()
            print(checklist)
        else:
            print("读取列失败，错误信息：", selected_data)


        # 定义要爬取的网页URL
        last_element = 0
        number_List = 0
        for list_param in checklist:
            new_file_path=f'found_data_{file_path.split(".")[0]}.csv'
            if os.path.exists(new_file_path):
                with open(new_file_path, 'r', newline='',encoding='utf-8-sig') as csvfile:
                    reader = csv.reader(csvfile)
    
                    # 读取第一列的数据
                    first_column_data = [row[0] for row in reader]
    
                    if first_column_data:
                        last_element = first_column_data[-1]
                        print("第一列的最后一个元素是:", last_element)
                    else:
                        print("第一列没有数据")
                if int(last_element) > int(list_param):
                    continue

            if config.has_section('web_url_configure'):
                first_url=config.get("web_url_configure","WEBS_URL")
                web_name=config.get("web_url_configure","WEB_NAME")
                url=f'{first_url}/{list_param}/{web_name}'
            else:
                url = f'https://q.stock.sohu.com/cn/{list_param}/index.shtml'  
            
            # 调用函数并传入URL和要查找的文字
            if config.has_section('web_url_configure'):
                key_word=config.get("web_url_configure","KEY_WORD")
                target_text = key_word.split(',')
            else:
                target_text = ["每股收益",'每股净资产','主营收入','净利润','销售毛利率','总股本','流通股本','每股资本公积金','每股未分配利润','净资产收益率']  # 将此替换为你要查找的文字

            
            for i in range(10):
                found_rows = find_text_in_table(url, target_text)
                if found_rows:
                    break

            # 调用函数，将找到的数据写入Excel文件
            output_file = f'found_data_{file_path.split(".")[0]}.csv'  # 设置输出的Excel文件名

            write_to_csv(found_rows, output_file,number_List,list_param)
            number_List=number_List+1


def get_stock_today_value():
    config=configparser.ConfigParser()
    config.read("../config.ini",encoding='utf-8-sig')
    if config.has_section('stock_list_configure'):
       file_path_list = config.get("stock_list_configure","STOCK_LIST_NAME")
    else:
        file_path_list = ['Shenzhen_stock_list.xlsx','Shanghai_stock_list.xls'] # READ STOCK LIST
    for file_path in file_path_list:
        
        column_name = 'A股代码'
        checklist=[]
        #selected_data = read_excel_column_format_string(file_path, column_name)
        selected_data = read_excel_column(file_path, column_name)
        if isinstance(selected_data, pd.Series):
            print(f"成功读取列 '{column_name}' 的数据:")
            checklist=selected_data.tolist()
            print(checklist)
        else:
            print("读取列失败，错误信息：", selected_data)


        # 定义要爬取的网页URL
        number_List = 0
        for list in checklist:
            stock_code=list
            quote = ef.stock.get_latest_quote(stock_code)
            output_file = f'price_{file_path.split(".")[0]}.csv'
            value_now=quote['最新价'].tolist()
            #print(value_now)
            write_price_to_csv(value_now, output_file,number_List,list)
            number_List=number_List+1
        print('finished........!!!!!!!')
if __name__ == '__main__':

    get_stock_today_value()