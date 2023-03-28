import pymysql
import os
from dotenv import load_dotenv


load_dotenv()

try:
    connection = pymysql.connect(user=os.getenv('MYSQL_USER'),
                            password=os.getenv('MYSQL_PASSWORD'),
                            db=os.getenv('MYSQL_DATABASE'),
                            host=os.getenv('MYSQL_HOST'),
                            port=int(os.getenv('MYSQL_PORT')))
    print("Conexión correcta")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Ocurrió un error al conectar: \n", e)


DB_NAME = 'users'

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `firts_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `email` varchar(120) NOT NULL,"
    "  `password` varchar(128) NOT NULL,"
    "  `role` varchar(10) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

cursor = connection.cursor()

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except pymysql.connect.Error as e:
        print("Error al crear la base de datos: {}".format(e))

def exist_database(cursor):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except pymysql.connect.Error as e:
        print("La base de datos {} no existe".format(e))
        if e.errno == e.errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Base de datos {} creada.".format(DB_NAME))
            connection.database = DB_NAME
        else:
            print(e)
            exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creando tabla {} ".format(table_name), end='')
        cursor.execute(table_description)
    except pymysql.connect.Error as e:
            print("")
    else:
        print("OK")

cursor.close()
connection.close()