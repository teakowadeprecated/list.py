import json
import os

import requests

from src import hashfile

r = requests.get('https://steamapi.addones.org/ISteamApps/GetAppList/v2')

parsed = json.dumps(r.json()['applist']['apps'])

fileObject = open('./list/applist.json', 'w')
fileObject.write(parsed)

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './list/applist.json')

fileObject = open('./list/applist.lock', 'wb')
fileObject.write(hashfile.SHA1(file_path))
fileObject.close()
