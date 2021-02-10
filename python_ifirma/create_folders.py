from datetime import datetime as dt
import os
from config import FILE_PATH
import dateutil.relativedelta

def create_folders(folder, month):
    date = dt.now()
    if month == 'last':
        date = date - dateutil.relativedelta.relativedelta(months=1)
    year = date.strftime('%Y')
    month_folder = date.strftime('%m-%B')

    pathyear = FILE_PATH + year
    if not os.path.exists(pathyear):
        os.makedirs(pathyear)

    pathmonth = pathyear + '/' + month_folder
    if not os.path.exists(pathmonth):
        os.makedirs(pathmonth)

    lastpath = pathmonth + folder
    if not os.path.exists(lastpath):
        os.makedirs(lastpath)

    return lastpath

