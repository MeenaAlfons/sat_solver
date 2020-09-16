import csv

def save_csv(filename, header, data):
    with open(filename,'w') as out:
        csvWriter = csv.writer(out)
        csvWriter.writerow(header)
        for row in data:
            csvWriter.writerow(row)