from urllib.parse import unquote
import json
import threading
from time import sleep
import mysql.connector
import os

conn = mysql.connector.connect(
    host='webservermrm.ddns.net',
    user='root',
    passwd='765161448',
    database='links')
# after calling 'get_filename_on_server()' this list will be updated
# server list format: [NAME, NAME, NAME, ...]
server_files = []

# after calling 'get_filename_from_gap()' this dic will be updated
# gap dic format:  {id: {'filename': 'SOMETHINGS', 'path': 'SOMETHING', 'filesize': 'SOMETHING', ...}}
gap_files = {}

# after calling 'get_main_links()' this dic will be updated
# gap dic format:  {id: link, ...}
main_files = {}


def get_filename_on_server():
    global server_files
    server_files.extend(os.listdir('C:\###Upload\\'))


def get_filename_from_gap():
    global gap_files
    conncursorgap = conn.cursor()
    sql_commend = 'SELECT * FROM gaplinks WHERE status = "0" AND type="file"'
    conncursorgap.execute(sql_commend)
    for x in conncursorgap.fetchall():
        gap_files.update({x[0]: json.loads(x[5])})


def get_main_links():
    global main_files
    conncursormanilink = conn.cursor()
    sql_commend = 'SELECT * FROM usermainlinksgap WHERE status = "1"'
    conncursormanilink.execute(sql_commend)
    for x in conncursormanilink.fetchall():
        main_files.update({x[0]: unquote(x[3])})










































'''
url = 'http://gapbot.devmrm.ir/getlinks.php'
params = {'ACCESS_KEY': '2C785B1D294D852C7C88B542977A21A230527173'}
json_links = []
main_links = []


def gap_file_name(gap_name):
    extension = gap_name.rsplit('.', 1)[1]
    name = gap_name.rsplit('_', 1)[0]
    return [name + "." + extension, extension]


def file_name(link):
    if link.find('/'):
        name = link.rsplit('/', 1)[1]
        extension = name.rsplit('.', 1)[1]
        return [name, extension]


def get_main_links():
    global main_links
    params['COMPERE'] = 'true'
    while True:
        sleep(5)
        try:
            result = requests.get(url, params=params).content.decode("UTF-8")
            main_links = result.split('~~~')
            main_links = main_links[:(len(main_links) - 1)]
            for index, link in enumerate(main_links):
                id_link = link.split('#')
                main_links[index] = id_link
        except:
            pass


def get_gap_links():
    global json_links
    params['GAP_LINKS'] = 'true'
    while True:
        sleep(5)
        try:
            result = requests.get(url, params=params).content.decode("UTF-8")
            data = result.split('~~~')
            data = data[:(len(data) - 1)]
            for j in data:
                try:
                    json_links.append(json.loads(j))

                except json.decoder.JSONDecodeError:
                    pass
        except:
            pass


# essential params ===>  ACCESS_KEY  ,  SET_LINKS   ,  GAP_LINK  ,  ID
def compere():
    global main_links
    global json_links
    params['SET_LINKS'] = 'true'
    while True:
        sleep(5)
        try:
            for j_index, j in enumerate(json_links):
                if j['type'] == "file":
                    for main_index, main_link in enumerate(main_links):
                        gatfilename = gap_file_name(j['filename'])[0]
                        mainfilename = unquote(file_name(main_link[1])[0])

                        if gatfilename == mainfilename:
                            params['GAP_LINK'] = j['path']
                            params['ID'] = main_link[0]
                            requests.get(url, params=params)
                            print(gatfilename + "  ====>  was matched successfully!")
                            del json_links[j_index]
                            del main_links[main_index]
        except:
            pass


if __name__ == '__main__':
        t1 = threading.Thread(target=get_main_links)
        t2 = threading.Thread(target=get_gap_links)
        t3 = threading.Thread(target=compere)
        t1.start()
        t2.start()
        t3.start()


'''
