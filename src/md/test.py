import inspect
import os
import sys
from pprint import pprint

import cx_Oracle
import asyncio
import datetime
import random
import websockets
import websocket
from websocket import create_connection
# curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# sys.path.append('D:\PythonProject\OpenCTP_CTP')
from openctp_ctp import mdapi

#from src import config
from TickDataStruct import OneMinuteTick

'''
def test1(instruments):
    for instrument_id in instruments:
        # 初始化Bar字段
        print("instrumentid is:"+instrument_id)

if __name__ == "__main__":

    # 注意选择有效合约, 没有行情可能是过期合约或者不再交易时间内导致
    instruments = ("SA401", "FG401", "UR401", "SH405", "eg2401", "p2401")
    test1(instruments)
'''

print(' ========= websocket is going to run =========')


async def time(websocket, path):
    while True:
        now = str(random.randint(0, 100))
        print(now)
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


start_server = websockets.serve(time, "127.0.0.1", 5678)
print(' ========= websocket running =========')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

'''
ws = create_connection("ws://127.0.0.1:5678")
msg = str(random.randint(0, 100))
print("发送消息：%s" % msg)
ws.send(msg)
# print("发送中...")
result = ws.recv()
print("返回结果：%s" % result)
ws.close()
'''