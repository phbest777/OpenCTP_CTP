import sys
import cx_Oracle
import json

# curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('D:\PythonProject\OpenCTP_CTP')

if __name__ == "__main__":
    conn = cx_Oracle.connect('user_ph', 'ph', '127.0.1.1:1521/orclpdb')
    cursor = conn.cursor()
    DesFilePath="D:\\GitRepository\\ZJJGWebFront\\src\\views\\acc_debt\\acc_debt_oper\\data\\"
    DesFileName=DesFilePath+"test1.json"
    sqlstr="select TRADINGDAY,INSTRUMENTID,LASTPRICE,VOLUME,OPENINTEREST,UPRATIO,INTERESTMINUS,INTERESTRATIO,UPDATEMINUTE from QUANT_FUTURE_MD_ONEMIN " \
           "where tradingday='20231205' and instrumentid='SA401' order by UPDATEMINUTE asc"
    rows=cursor.execute(sqlstr).fetchall()
    with open(DesFileName, 'w') as file:
        json.dump(rows, file)
