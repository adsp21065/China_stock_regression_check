import sys
import logging
import configparser
from src import check_f10
from src import find_out_better_value as fob
import shutil
from datetime import date
import os
import schedule
import time

def setup_logging_2():
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                        format='%(asctime)s [%(levelname)s] %(message)s')
    
class Logger(object):
    def __init__(self, filename='app.log'):
            self.terminal = sys.stdout
            
            self.log = open(filename,'a')
    def write(self, message):
        self.log.write(message)
        self.terminal.write(message)
        self.log.flush()
    def flush(self):
        pass

class Logger_error(object):
    def __init__(self, filename='app_err.log'):
            self.terminal_err = sys.stderr
            
            self.log = open(filename,'a')
    def write(self, message):
        self.log.write(message)
        self.terminal_err.write(message)
        self.log.flush()
    def flush(self):
        pass


def copy_to_date_folder(source_file, destination_root_folder):
    # 获取今天的日期
    today = date.today()

    # 根据日期创建文件夹名称（格式：YYYY-MM-DD）
    folder_name = today.strftime("%Y-%m-%d")

    # 构建目标文件夹的路径
    destination_folder = os.path.join(destination_root_folder, folder_name)

    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    # 构建目标文件的完整路径
    destination_path = os.path.join(destination_folder, os.path.basename(source_file))

    # 复制文件到目标文件夹
    shutil.move(source_file, destination_path)


def Regression_Stock_Main():
    config=configparser.ConfigParser()
    config.read("config.ini",encoding='utf-8-sig')
    if config.has_section('stock_list_configure'):
        file_path_list = config.get("stock_list_configure","STOCK_LIST_NAME")
    else:
        file_path_list = ['Shenzhen_stock_list.xlsx','Shanghai_stock_list.xls'] # READ STOCK LIST
    
    #use chek_f10 to get infromation every month
    #check_f10.get_stock_f10_value()

    #get the price every day
    check_f10.get_stock_today_value()

    #merger price and data
    fob.combin_name_today_price_and_history_value()
    for file_path in file_path_list:
        copy_path=f'merged_{file_path.split(".")[0]}.csv'
        copy_to_date_folder(copy_path,'Summary_Data')
        price_path=f'price_{file_path.split(".")[0]}.csv'
        shutil.remove(price_path)

# 定义定时执行的函数
def scheduled_task():
    Regression_Stock_Main()

if __name__ == "__main__":
    # 每天的执行时间（以24小时制的时:分表示）
    execution_time = "16:30"  # 这里以下午2点30分为例

    # 使用schedule库来安排任务的执行时间
    schedule.every().day.at(execution_time).do(scheduled_task)

    # 无限循环以等待任务的执行
    while True:
        schedule.run_pending()
        time.sleep(100)