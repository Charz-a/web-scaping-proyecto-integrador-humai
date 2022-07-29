import csv
import os
from datetime import datetime
import subprocess

#home = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
#file_name = 'prueba.csv'
#file_directory = os.path.join(home,file_name)

#file1 = open(direccion,"w")
#file1.close()

def get_last_csv():
    q = "ls " + get_project_path() + " -Art | tail -n 1"
    result = subprocess.getoutput(q)
    last_csv_path = get_file_directory(result)
    return last_csv_path


def get_project_path():
    q = "find /home -type d -name 'proyecto_integrador_humai' -print"
    result = subprocess.getoutput(q).split("\n")
    for path in result:
        if "proyecto_integrador_humai" in path:
            final_path = path
    
    return final_path + "/data"

def get_file_directory(file_name):
    file_directory = os.path.join(get_project_path(), file_name)
    return file_directory

def write_csv(data):
    file_name = 'actividades_' + datetime.today().strftime('%d-%m-%Y') + '.csv'
    file_directory = get_file_directory(file_name)

    if os.path.isfile(file_directory):
        with open(file_directory, 'a', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(data)
    else:
        with open(file_directory, 'w', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["activity_id","activity_name", "activity_url","activty_dates","activity_times","activty_place","activity_district","activity_address","activity_description"])
            writer.writerow(data)

    return file_directory

def read_csv(file_name): #no toque nada, cuando haya que hacer dashboard modificar acorde a necesidades
    file_directory = get_file_directory(file_name)
    with open(file_directory, 'r', encoding='UTF8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            print(row[0])
