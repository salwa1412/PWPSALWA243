from flask_mysqldb import MySQL
from flask import Flask

def init_db(app: Flask):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'  # Ganti dengan username MySQL kamu
    app.config['MYSQL_PASSWORD'] = '1234'  # Ganti dengan password MySQL kamu
    app.config['MYSQL_DB'] = ''

    # Inisialisasi MySQL
    mysql = MySQL(app)
    return mysql