#!/usr/bin/python3
#ReadFile.py

import csv
from datetime import datetime
import pymysql

def PrintCSVFile(filename):
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile)

        #for row in rows:
        #    print(row)

        """datas = list(rows)
        print(datas)

        length = len(datas)
        print(length)

        testtime = datetime.strptime(datas[1][8],'%m/%d/%Y %I:%M:%S %p')
        print(testtime)

        floatvalue = float(datas[1][9])
        print(floatvalue) """

        datas = list(rows)
        length = len(datas)

        connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', charset='utf8', db='anko_iot')

        sql = 'INSERT INTO table_vibration_message(topic, status, naber, record_time, message) VALUES'
        sql2 = 'insert into anko_iot.table_vibration_message(topic, status, naber, record_time, message) values(%s, %s, %s, %s, %s)'#, %f)'

        list1 = []

        for _index in range(1, length):
            testtime = datetime.strptime(datas[_index][8],'%m/%d/%Y %I:%M:%S %p')
            floatvalue = float(datas[_index][9])
            str_now = testtime.strftime('%Y-%m-%d %H:%M:%S')
            sql += '(\'' + datas[_index][5] + '\',\'' + datas[_index][6] + '\',\'' + datas[_index][7] + '\',\'' + str(testtime) + '\',' + str(floatvalue) + ')'
            if _index < (length-1):
                sql += ','
            else:
                sql += ';'
            list2 = []
            list2.append(datas[_index][5])
            list2.append(datas[_index][6])
            list2.append(datas[_index][7])
            list2.append(str_now)
            list3 = (datas[_index][5], datas[_index][6], datas[_index][7], str_now, floatvalue)
            #list2.append(floatvalue)
            list1.append(list3)

        print(list1)
        print(sql2)
        
        with connect_db.cursor() as cursor:
            print(cursor.rowcount)
            cursor.executemany(sql2, list1)
            result_set = cursor.fetchone()
            #print(result_set)
            #print(cursor.rowcount)
            #cursor.executemany(sql2, [('A','B','C', '20240312081223', 0.22),('A','B','C', '20240312081223', 0.22)])
        connect_db.commit()

if __name__ == '__main__':
    PrintCSVFile('data.csv')