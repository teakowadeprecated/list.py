import json
import filecmp
import requests

r = requests.get('https://steamapi.addones.org/ISteamApps/GetAppList/v2')

parsed = json.dumps(r.json()['applist']['apps'])

# New applist.cache we need check version

cacheObject = open('./list/applist.cache', 'w')
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
    print('Everything up to date')

