from calendar import c
import sqlite3

# Connect to sqlite
connection = sqlite3.connect("student.db")

# Create a cursor
cursor = connection.cursor()

# Create a table
table_info = """
    CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), 
    SECTION VARCHAR(10), MARKS INT)
    """

cursor.execute(table_info)

# Insert data
cursor.execute("INSERT INTO STUDENT VALUES('John', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT VALUES('Mark', 'DevOps', 'B', 100)")
cursor.execute("INSERT INTO STUDENT VALUES('Jane', 'DevOps', 'A', 85)")
cursor.execute("INSERT INTO STUDENT VALUES('Lily', 'Data Science', 'A', 40)")
cursor.execute("INSERT INTO STUDENT VALUES('Harry', 'Data Science', 'B', 75)")
cursor.execute("INSERT INTO STUDENT VALUES('Tom', 'Data Science', 'A', 56)")

# Display all records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for record in data:
    print(record)

# Commit the changes
connection.commit()
connection.close()
