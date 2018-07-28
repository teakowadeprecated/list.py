# -*- coding: utf-8 -*-  
import json
import codecs

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
