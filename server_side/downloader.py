"""
It need to folder in drive C :
###Upload
#xTempDownload
"""
import mysql.connector
import shutil
import random
import string
import threading
from time import sleep
from pySmartDL import SmartDL

links = []
conn = mysql.connector.connect(
    host='webservermrm.ddns.net',
    user='root',
    passwd='',
    database='links')


# just add links to global link variable
def get_links():
    global links
    while True:
        sleep(5)
        try:
            sqldbcursor = conn.cursor()
            # fetch data from database
            sqldbcursor.execute('SELECT * FROM usermainlinksgap WHERE status="0"')
            for x in sqldbcursor.fetchall():
                links.append(x[3])
                # update database after links was got
                sqldbcursor.execute('UPDATE usermainlinksgap SET status ="1" WHERE id = "{id}"'.format(id=x[0]))
                conn.commit()
        except:
            pass


# return like : ['something_QejPo.rar', 'rar']
def file_name_for_download(name):
    random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    extension = name.rsplit('.', 1)[1]
    name = name.rsplit('.', 1)[0] + "_" + random_name
    return [name + '.' + extension, extension]


def download(link):
    if len(link) > 0:
        try:
            d = SmartDL(link, 'C:\\#xTempDownload\\')
            mainfilename = d.get_dest().rsplit('\\', 1)[1]
            # get download file name(with random_key) for move it
            filename = file_name_for_download(mainfilename)[0]
            print(filename + "  ===>   ", end="")
            d.start(blocking=False)
            d.wait()
            shutil.move('C:\\#xTempDownload\\{MFN}'.format(MFN=mainfilename), 'C:\\###Upload\\{FN}'.format(FN=filename))
        except ValueError:
            links.remove(link)
        except:
            pass


if __name__ == '__main__':
    get = threading.Thread(target=get_links)
    get.start()
    sleep(6)
    while True:
        jobs = []
        for each_link in links:
            t = threading.Thread(target=download, args=(each_link,))
            jobs.append(t)
            sleep(random.choice([1, 2, 3, 4]))
            t.start()
            links.remove(each_link)
        for job in jobs:
            job.join()





