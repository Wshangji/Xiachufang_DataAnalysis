import csv
import random

def get_random_proxy():
    '''随机从文件中读取proxy'''
    while 1:
        with open('D:\PROJECT\Xiachufang_DataAnalysis\DataGet\proxy.csv', 'r') as f:
            proxies = f.readlines()
        if proxies:
            break
        else:
            time.sleep(1)
    proxy = random.choice(proxies).strip()
    print(proxy)

if __name__ == '__main__':
    get_random_proxy()