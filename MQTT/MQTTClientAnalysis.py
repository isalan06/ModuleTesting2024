#!/usr/bin/python3
#MQTTClientAnalysis.py

# import mysql
import pymysql

from operator import itemgetter

data_assembly = []

class MyData:

    def __init__(self):
        print('To initialize MyData')        

    def CreateData(self):
        global data_assembly

        # Create a MySQL connection
        connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', charset='utf8', db='anko_iot')

        with connect_db.cursor() as cursor:
            sql = 'SELECT * FROM anko_iot.table_dio_record order by id desc limit 1;'
            # 執行指令
            cursor.execute(sql)
            result_set = cursor.fetchone()#cursor.fetchall()
            value_string = result_set[3]
            #print(result_set[3])
            value_string = value_string.replace(' ', '').replace('\n', '')
            #print(value_string)
            value_string_array = value_string.split('|')
            #print(value_string_array)

            showmessage = 'hz_in: ' + value_string_array[0] + "; "
            showmessage += 'hz_out: ' + value_string_array[1] + "; "
            showmessage += 'a_out: ' + value_string_array[2] + "; "
            showmessage += 'rpm_out: ' + value_string_array[3] + "; "
            showmessage += 'temp: ' + value_string_array[4] + "; "
            showmessage += 'error: ' + value_string_array[5] + "; "
            showmessage += 'day: ' + value_string_array[6] + "; "
            showmessage += 'hour: ' + value_string_array[7] + "; "
            #print(showmessage)

            sql = """
                SET sql_mode = (SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''));
                """
            cursor.execute(sql)

            sql = 'SELECT * FROM (SELECT id, record_time, topic, value FROM anko_iot.table_dio_record order by id desc LIMIT 10) AS RAW_DATA GROUP BY topic;'
            cursor.execute(sql)
            result_set = cursor.fetchall()
            #print(result_set)

            data_assembly = []
            for row in result_set:
                data = {}
                topic = row[2].replace(' ', '').replace('\n', '').split('/')[2]
                data["topic"] = topic
                data_array = row[3].replace(' ', '').replace('\n', '').split('|')
                data["hz_in"] = int(data_array[0])
                data["hz_out"] = int(data_array[1])
                data["a_out"] = int(data_array[2])
                data["rpm_out"] = int(data_array[3])
                data["temp"] = int(data_array[4])
                data["error"] = int(data_array[5])
                data["day"] = int(data_array[6])
                data["hour"] = int(data_array[7])

                data_assembly.append(data)

            self.ShowMessage()
    
            

    def ShowMessage(self):
        newlist = sorted(data_assembly, key=itemgetter('topic'))

        showmessage2 = '\r'

        for da in newlist:
            showmessage2 += 'Topic: ' + da['topic'] + '; '
            showmessage2 += 'hz_in: ' + '{:<4}'.format(da['hz_in']) + '; '
            showmessage2 += 'hz_out: ' + '{:<4}'.format(da['hz_out']) + '; '
            showmessage2 += 'a_out: ' + '{:<4}'.format(da['a_out']) + '; '
            showmessage2 += 'rpm_out: ' + '{:<6}'.format(da['rpm_out']) + '; '
            showmessage2 += 'temp: ' + '{:<4}'.format(da['temp']) + '; '
            showmessage2 += 'error: ' + '{:<6}'.format(da['error']) + '; '
            showmessage2 += 'day: ' + '{:<3}'.format(da['day']) + '; '
            showmessage2 += 'hour: ' + '{:<3}'.format(da['hour']) + '; '
            showmessage2 += '\n'

        print(showmessage2)

if __name__ == '__main__':
    myData = MyData()
    myData.CreateData()
