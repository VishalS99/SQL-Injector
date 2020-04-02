import mysql.connector as connector
import json
from extractor import *

try:
    with open('config.json') as config_file:
        data = json.load(config_file)
except:
    print("Config doesnt exist")
    exit(0)


def determine_mysql_datatype(type):
    if type == 0:
        return "INT"
    if type == 1:
        return "VARCHAR(255)"
    if type == 2:
        return "DATE"
    else:
        print("Wrong option!!")
        determine_mysql_datatype(type)


def connect_database(db_name):
    try:
        db = connector.connect(
            host=data["host"],
            user=data["user"],
            passwd=data["password"]
        )
        cursor = db.cursor()
        print("Craeted conne")
        cursor.execute("CREATE DATABASE " + db_name)
        cursor.execute("USE " + db_name)
        print("## Created database connection to mysql")
        return (cursor, db)
    except:
        print("xx Failed to create connection to Mysql")
        exit(0)


def create_table(db, cursor, headings, table_name):
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    entries = ""
    type_list = []
    for head in headings:

        entry_type = int(input(
            "Enter type of data (int: 0, varchar: 1, date: 2) for " + head + ": "))
        datatype = determine_mysql_datatype(entry_type)
        type_list.append(datatype)
        is_primary = int(input("Is it primary (No: 0, Yes: 1)? "))
        if is_primary == 1:
            entries += head + " " + datatype + " PRIMARY KEY,"
        else:
            entries = entries + head + " " + datatype + ","
    query = "CREATE TABLE " + table_name + " (" + entries[:-1] + ")"
    print(query)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Failed to execute the query!!")
    return type_list


def populator(db, cursor, table_name, headings, row_entries):
    type_list = create_table(db, cursor, headings, table_name)

    # sql_queries = "INSERT INTO " + table_name + " VALUES("
    # for j in range(len(row_entries[0])):
    #     if type_list[j] == "INT":
    #         sql_queries += "%d,"
    #     elif type_list[j] == "VARCHAR(255)":
    #         sql_queries += "%s,"
    #     elif type_list[j] == "DATE":
    #         sql_queries += "%d,"
    # sql_queries = sql_queries[:-1] + ")"


def main():
    path = './images/tt.jpg'
    # path = input("Enter image path: ")
    # database_name = input("Enter the name of database: ")
    database_name = "sqlhelper"
    # table_name = input("Enter the name of table: ")
    table_name = "test1"
    (headings, row_entries) = extractor(path)
    print("## Extraction of table completed.\n")
    print("## Adding entries to database")
    (cursor, db) = connect_database(database_name)
    populator(db, cursor, table_name, headings, row_entries)
    print("## Added table into database " + database_name)
    db.close()


if __name__ == "__main__":
    print("### Sequel Injector ###\n")
    main()
    print("\n### Done ###")
