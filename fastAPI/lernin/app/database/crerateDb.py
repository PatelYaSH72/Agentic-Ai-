import psycopg2

# pehle postgres default db se connect karo
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="YASHPOSTGREYDATABASE",
    database="postgres"  # default db
)
conn.autocommit = True
cursor = conn.cursor()

# naya database banao
cursor.execute("CREATE DATABASE naya_database_naam")
print("Database created!")

cursor.close()
conn.close()