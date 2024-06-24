#!/usr/bin/python3
#Analyze700U.py

import csv
import pymysql

sql_z05_x_02 = 'SELECT *, IF(AvgValue>AlarmValue, 2, IF(AvgValue>WarningValue, 1, 0)) AS Alert FROM view_vibration_info WHERE Status LIKE \'z05-%-02\' AND WarningValue>0 AND AlarmValue>0 ORDER BY Naber, Status;'
sql_z05_x_03 = 'SELECT *, IF(AvgValue>AlarmValue, 2, IF(AvgValue>WarningValue, 1, 0)) AS Alert FROM view_vibration_info WHERE Status LIKE \'z05-%-03\' AND WarningValue>0 AND AlarmValue>0 ORDER BY Naber, Status;'
sql_z05_x_04 = 'SELECT *, IF(AvgValue>AlarmValue, 2, IF(AvgValue>WarningValue, 1, 0)) AS Alert FROM view_vibration_info WHERE Status LIKE \'z05-%-04\' AND WarningValue>0 AND AlarmValue>0 ORDER BY Naber, Status;'

filename_02 = 'Vibration_700U_02.csv'
filename_03 = 'Vibration_700U_03.csv'
filename_04 = 'Vibration_700U_04.csv'

sql_command = [sql_z05_x_02, sql_z05_x_03, sql_z05_x_04]
filenames = [filename_02, filename_03, filename_04]
fields = ['Naber', 'Status', 'WarningValue', 'AlarmValue', 'AvgValue', 'StdValue', 'Count', 'Alert']

for i in range(0, 3):
    writedata = []
    

    connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', charset='utf8', db='anko_iot')

    with connect_db.cursor() as cursor:
        sql = sql_command[i]

        cursor.execute(sql)
        result_set = cursor.fetchall()

        for row in result_set:
            data = {}
            data['Naber'] = row[0]
            data['Status'] = row[1]
            data['WarningValue'] = row[2]
            data['AlarmValue'] = row[3]
            data['AvgValue'] = row[4]
            data['StdValue'] = row[5]
            data['Count'] = row[6]
            data['Alert'] = row[7]
            writedata.append(data)

        #print(writedata)

        print(filenames[i])
        with open(filenames[i], 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)
 
            # writing headers (field names)
            writer.writeheader()
 
            # writing data rows
            writer.writerows(writedata)


def ReadDBAndWriteCSV():
    pass

if __name__ == '__main__':
    ReadDBAndWriteCSV()