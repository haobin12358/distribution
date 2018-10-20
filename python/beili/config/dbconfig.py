import os
database = os.environ.get('DB_NAME', "beili")
host = os.environ.get('DB_HOST', "localhost")
port = "3306"
username = os.environ.get('DB_USER', 'root')
password = os.environ.get('DB_PWD', 'root')
charset = "utf8"
sqlenginename = 'mysql+pymysql'
