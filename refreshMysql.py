import os,mysql.connector as mysql

try:
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "sas"
    )

    cursor = db.cursor()

    cursor.execute("SHOW DATABASES")

    databases = [_[0] for _ in cursor.fetchall() if (_[0].startswith("db") and _[0].endswith("db"))]

    cursor.execute("DROP DATABASE jbossdbpvz;")
    cursor.execute("CREATE DATABASE jbossdbpvz;")
    for _ in databases:
        cursor.execute(f"DROP DATABASE {_}")
    print("Success")
except Exception as e:
    os.system("clear")
    print("Failure")
    print(e)