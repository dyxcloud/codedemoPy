import sqlite3
import os

db_path = '../../data/test.db'
print(os.path.abspath(db_path))
conn = sqlite3.connect(os.path.abspath(db_path))
# 创建一个Cursor:
cursor = conn.cursor()
cursor.execute("select id,name from user")
print(cursor.fetchall())
# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
conn.close()
