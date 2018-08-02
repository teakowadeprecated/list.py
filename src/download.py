import json
import filecmp
import requests
import codecs

r = requests.get('https://steamapi.addones.org/ISteamApps/GetAppList/v2')

parsed = json.dumps(r.json()['applist']['apps'])

# New applist.cache we need check version

cacheObject = open('./list/applist.cache', 'w+')
cacheObject.write(parsed)
cacheObject.close()
checkDiff = filecmp.cmp('./list/applist.json', './list/applist.cache')

if checkDiff:
    print('Already up to date.')
else:
    # Update applist.json 
    print('Writing objects...')
    fileObject = open('./list/applist.json', 'w')
    fileObject.write(parsed)
    fileObject.close()
    
    # Update applist.sql
    with open('./list/applist.json', 'r') as applist:
        data = json.load(applist)

    # Find all keys
    keys = []
    for row in data:
        for key in row.keys():
            if key not in keys:
                keys.append(key)

    f = codecs.open('./list/applist.sql', 'w+', 'utf-8')
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


