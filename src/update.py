import configparser
import json
import os
import mysql.connector

config = configparser.ConfigParser()
config.read('../config.conf')

file_path = os.path.join(os.path.dirname(__file__), './list/applist.json')

with open(file_path) as f:
    parsed = json.load(f)

conn = mysql.connector.connect(host=config.get("DB", "host"), user=config.get("DB", "user"),password=config.get("DB", "password"), database=config.get("DB", "database"))
cursor = conn.cursor()
cursor.execute("SET names 'utf8mb4'");

cursor.execute('select count(AppID) from apps')

count = int(cursor.fetchone()[0]) - 1

appscount = int(len(parsed))

result = [(item.get('appid', 'NA'), item.get('name', 'NA')) for item in parsed]

if count < appscount:

    print('Updating...')
    for app in result:
        insert_applist = "replace into apps(AppID, Name) VALUES (%s,%s)"
        cursor.execute(insert_applist, app)
        conn.commit()    
    cursor.close()
    print('Everything up to date')

