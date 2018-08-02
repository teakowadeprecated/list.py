import json
import filecmp
import requests
import codecs
import os

r = requests.get('https://steamapi.addones.org/ISteamApps/GetAppList/v2')

parsed = json.dumps(r.json()['applist']['apps'])

file = os.path.dirname(__file__)
listCache = file + '/list/applist.cache'
listJson = file + '/list/applist.json'
listSQL = file + '/list/applist.sql'

# New applist.cache we need check version

with open(listCache, 'w+') as cacheObject:
    cacheObject.write(parsed)

checkDiff = filecmp.cmp(listJson, listCache)

if checkDiff:
    print('Already up to date.')
else:
    # Update applist.json 
    print('Writing objects...')
    with open(listJson, 'w') as fileObject:
        fileObject.write(parsed)

    # Update applist.sql
    with open(listJson, 'r') as applist:
        data = json.load(applist)

    # Find all keys
    keys = []
    for row in data:
        for key in row.keys():
            if key not in keys:
                keys.append(key)

    f = codecs.open(listSQL, 'w+', 'utf-8')
    insert = """INSERT INTO `applist` (`{0}`) VALUES""".format("`, `".join(map(lambda key: "{0}".format(key), keys)))

    f.write(insert)
    f.write('\n')

    for row in data:
        writeData = """    ({0}),""".format(
            ",".join(
                map(
                    lambda key: "`{0}`".format(row[key]) if key in row else "NULL", keys
                )
            )
        )
        f.writelines(writeData)
        f.write('\n')
    print('Everything up to date')


