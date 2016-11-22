from json import *
import os

def get_var(data_var):

    jsonfile = "data.json"
    with open(jsonfile,'r') as file:
        file_data = file.read()
    file.close()
    try:
        json_data = loads(file_data)
    except:
        return
    data = {}
    if type(data_var) is tuple:
        for x in data_var:
            try:
                data[x] = json_data[x]
            except KeyError:
                print("No variable %s found in data"%x)
    else:
        try:
            data[data_var]= json_data[data_var]
        except KeyError:
            print("No variable %s found in data" % data_var)

    return data

def write_var(data_var,data):
    with open("data.json",'r+') as file:
        file_data = file.read()
    file.close()
    json_data = loads(file_data)

    fixup(json_data,data_var,data)

    file_data = dumps(json_data, sort_keys=True, indent=2, separators=(',',': '))
    with open("data.json",'r+') as file:
        file.seek(0)
        file.truncate()
        file.write(file_data)
        file.flush()
        os.fsync(file.fileno())

    file.close()

def fixup(adict, k ,v):
    for key in adict.keys():
        if key ==k:
            adict[key] = v
        elif type(adict[key]) is dict:
            fixup(adict, k, v)