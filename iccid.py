import argparse
from datetime import datetime

import redis
from redis import ConnectionPool
import time
import xlwt

def get_args():
    result={"hour":0,"min":0} #使用一个字典以存储参数
    parser = argparse.ArgumentParser(description="your script description") #实例化一个参数对象,描述参数为help内容
    parser.add_argument('--year', type=int)  # 创建一个--hour参数,接收数据类型为int
    parser.add_argument('--month', type=int)  # 创建一个--min参数,接收数据类型为int
    parser.add_argument('--day', type=int)  # 创建一个--hour参数,接收数据类型为int
    parser.add_argument('--hour', type=int) #创建一个--hour参数,接收数据类型为int
    parser.add_argument('--min', type=int) #创建一个--min参数,接收数据类型为int
    args=parser.parse_args() #获得参数对象
    arg_dic={}
    if args.year is not None:
        arg_dic['year']=args.year
    if args.month is not None:
        arg_dic['month']=args.month
    if args.day is not None:
        arg_dic['day']=args.day
    if args.hour is not None:
        arg_dic['hour']=args.hour
    if args.min is not None:
        arg_dic['min']=args.min

    return arg_dic

def get_timestamp(year=2019, month=6, day=10, hour=0, min=0, sec=0):
    now = datetime(year, month, day, hour, min, sec)
    time_stamp_target = int(time.mktime(now.timetuple()))
    return time_stamp_target


def save2excel(data: dict):
    today = datetime.now()
    wb = xlwt.Workbook(encoding='gb2312')  # 创建实例，并且规定编码
    ws = wb.add_sheet('My Worksheet')  # 设置工作表名称
    ws.write(0, 0, 'ICCID')
    ws.write(0, 1, '时间')
    i = 0
    for k, v in data.items():
        i += 1
        ws.write(i, 0, k)
        ws.write(i, 1, v)
    file_name = 'data-{}年{}月{}日.xls'.format(today.year, today.month, today.day)
    wb.save(file_name)


def app(target_timestamp):
    # host = '118.89.106.236'
    host = '127.0.0.1'
    port = 6379
    pool = ConnectionPool(host=host, port=port, password='bishisimo', decode_responses=True)
    r = redis.StrictRedis(connection_pool=pool)
    t = r.dbsize()
    i = 0
    j = 0
    data = {}
    for k in r.keys():
        timestamp = int(r.get(k))

        if timestamp < target_timestamp:
            i += 1
        else:
            j += 1
            tl = time.localtime(timestamp)
            format_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
            data[k] = format_time
    print('总共{}条,6月10号之前的有{}条,之后的有{}条'.format(t, i, j))
    save2excel(data)

if __name__ == '__main__':
    arg_dic=get_args()
    target_timestamp = get_timestamp(**arg_dic)
    print(target_timestamp)
    app(target_timestamp)
