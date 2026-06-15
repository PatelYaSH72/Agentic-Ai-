import psycopg2

conn = psycopg2.connect(
  host="localhost",
  user="postgres",        # ← yahan postgres rakho
  password="YASHPOSTGREYDATABASE",
  database="postgres"  
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("CREATE DATABASE traninBologDb")
print("Database created!")

cursor.close()
conn.close()