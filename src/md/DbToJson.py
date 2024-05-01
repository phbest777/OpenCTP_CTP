import sys
import cx_Oracle
import json
import time
import datetime

# curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('D:\PythonProject\OpenCTP_CTP')

if __name__ == "__main__":
    conn = cx_Oracle.connect('user_ph', 'ph', '127.0.1.1:1521/orclpdb')
    cursor = conn.cursor()
    DesFilePath="D:\\GitRepository\\ZJJGWebFront\\src\\views\\acc_debt\\acc_debt_oper_new \\data\\"
    DesFileName=DesFilePath+"test1.json"
    #print("timestamp is"+str(datetime.datetime.now().timestamp()))
    #print("timestamp is" + str(datetime.datetime.now().timestamp()))
    #sqlstr="select TRADINGDAY,INSTRUMENTID,LASTPRICE,VOLUME,OPENINTEREST,UPRATIO,INTERESTMINUS,INTERESTRATIO,UPDATEMINUTE from QUANT_FUTURE_MD_ONEMIN " \
    #       "where tradingday='20231218' and instrumentid='SA405' order by UPDATEMINUTE asc"
    sqlstr2 = "select * from QUANT_FUTURE_MD_ONEMIN " \
             "where tradingday='20231222' and instrumentid='SA405'  order by id asc"
    rows=cursor.execute(sqlstr2).fetchall()
    with open(DesFileName, 'w') as file:
        json.dump(rows, file)
