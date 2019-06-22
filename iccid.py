from datetime import datetime

import redis
from redis import ConnectionPool
import time
import xlwt


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
    host = '39.98.164.160'
    port = 6379
    # pool = ConnectionPool(host=host, port=port, password='bishisimo', decode_responses=True)
    pool = ConnectionPool(host=host, port=port,  decode_responses=True)
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
    target_timestamp = get_timestamp()
    app(target_timestamp)
