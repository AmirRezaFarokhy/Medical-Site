import psycopg2 as pg 

try:
    conn = pg.connect(
        host='localhost',
        port=5432,
        dbname='postgres',
        password='postgres',
        user='postgres'
    )
    print("Connected succesfully...")

except Exception as e:
    print(f"Can't Connect for {e}")

conn.autocommit = True
cur = conn.cursor()
sql_command_1 = "SELECT * FROM main_doctor"
sql_command_2 = "SELECT * FROM main_doctor_patient" 
sql_command_3 = "SELECT * FROM main_patientprofile" 

def GetDataBases():
    database = []
    for sql in [sql_command_1, sql_command_2, sql_command_3]:
        lst = []
        cur.execute(sql)
        for row in cur.fetchall():
            print(row)
            lst.append(row)
        database.append(lst)
        print("\n Done Go Next...")
    return database

def ShowManyToManyRelationship(databases):
    for doctor in databases[0]:
        for relation, patient in zip(databases[1], databases[2]):
            if relation[1]==doctor[0]:
                print(f"This '{patient[1]+patient[2]}' Patiant belongs to this '{doctor[1]}' Doctor.")


database = GetDataBases()
ShowManyToManyRelationship(database)
