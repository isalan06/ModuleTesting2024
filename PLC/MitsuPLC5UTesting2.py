#!/usr/bin/python3
#MitsuPLC5UTesting.py

# 请先安装 pymodbus 和 pyserial
# pip install pymodbus
# pip install pyserial

from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException, ConnectionException
import logging

# 配置日志记录
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient(port='/dev/tty0', baudrate=19200, timeout=3,stopbits=1, bytesize=8, parity='O')

def readPLCData(client):
    try:
        result = client.read_holding_registers(address=1000, count=3, slave=1)  
 
        if result.isError():
            # 处理错误
            print("Read Error:", result)
            return None, None
 
        registers = result.registers
        d1000 = registers[0]
        d1001 = registers[1]
        d1002 = registers[2]

        print(f"d1000: {d1000}; d1001: {d1001}; d1002: {d1002}")

        return d1000, d1001, d1002
    except ModbusException as e:
        print("Modbus Error:", e)
        return None, None, None
    except Exception as e:
        # 捕获除ModbusException之外的所有异常
        print(f"An error occurred: {e}")
        return None, None, None

def main():
    try:
        if client.connect():  # 尝试连接到Modbus服务器/设备
            print("Connect to Modbus Device")

            d1000, d1001, d1002 = readPLCData(client)

            print("Disconnect from Modbus Device")
            client.close()  # 关闭连接
        else:
            print("Cannot connect to Modbus Device")
    except ConnectionException as e:
        print("Connection Error:", e)
 
 
if __name__ == "__main__":
    main()


