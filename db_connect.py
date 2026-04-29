import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="neeha@2004",
    database="hospital_db"
)

cursor=conn.cursor()

cursor.execute("SELECT full_name, role From users  WHERE role='admin'")
for row in cursor.fetchall():
    print(row)

conn.close()