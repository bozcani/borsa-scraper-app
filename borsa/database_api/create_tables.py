import sqlite3 
import pathlib
import os 
def create_db(path_to_db):

    if os.path.isfile(path_to_db):
        print("[*] create_db: Database already exist: {}".format(path_to_db))

    else:    
        connection = sqlite3.connect(path_to_db) 
        print("[*] create_db: Database crated{}".format(path_to_db))


def create_stocks_table(path_to_db):
    connection = sqlite3.connect(path_to_db) 

    # cursor  
    crsr = connection.cursor() 

    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE stocks (    
    symbol VARCHAR(5) PRIMARY KEY, 
    market VARCHAR(10), 
    name VARCHAR(50),  
    link VARCHAR(50));"""
    
    # execute the statement 
    crsr.execute(sql_command) 

    # Save changes
    connection.commit() 
    
    # close the connection 
    connection.close() 



create_stocks_table("./data/mydatabase.db")    