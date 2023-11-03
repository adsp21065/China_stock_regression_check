import sys
import logging
import configparser
from src import check_f10

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

def Regression_Stock_Main():
    config=configparser.ConfigParser()
    config.read("config.ini",encoding='utf-8-sig')

    #use chek_f10 to get infromation every month
    check_f10.get_stock_f10_value()

    #get the price every data

if __name__ == "__main__":
    Regression_Stock_Main()