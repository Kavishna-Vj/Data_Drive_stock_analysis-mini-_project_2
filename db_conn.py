
import mysql.connector 

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "vjskp@9767offmysql",
    database = "stock_analysis")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS stock_data(
               ticker VARCHAR(10),
               date VARCHAR(20),
               open FLOAT,
               close FLOAT,
               high FLOAT,
               low FLOAT,
               volume INT)""")

cursor.execute("""INSERT INTO stock_data(ticker,date,open,close,high,low,volume)
               VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE 
               open=VALUES(open),close=VALUEs(close),high=VALUES(high),low=VALUES(low),volume=VALUES(volumegit)
               """,('CTS','2023-11','3193.85','3187.4','3212.8','3358.35',75689))
conn.commit()
cursor.close()
conn.close()
