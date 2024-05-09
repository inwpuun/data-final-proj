import csv
def read_start_pointer() :
    result = []
    with open("test.csv", newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
            result.append({(row[0], row[1]): row[2]})
    return result

read_start_pointer()