import csv
import os


home = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
file_name = 'prueba.csv'
file_directory = os.path.join(home,file_name)

#file1 = open(direccion,"w")
#file1.close()


def write_csv(data):
    if os.path.isfile(file_directory):
        with open(file_directory, 'a', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(data)
    else:
        with open(file_directory, 'w', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["activity_id","activity_name", "activity_url","activty_dates","activity_times","activty_place","activity_district","activity_address","activity_description"])
            writer.writerow(data)

def read_csv():
    with open(file_directory, 'r', encoding='UTF8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            print(row[0])

