#DB Connection helper

import mysql.connector

def get_connection(database=None):
    config = {
        "host": "localhost",
        "user": "root",
        "password": "ridima456",
    }
    if database:
        config["database"] = database

    return mysql.connector.connect(**config)

   