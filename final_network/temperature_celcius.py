import csv


def calculate_temperature(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        new_lines = []
        for row in csv_reader:
            if line_count == 0:
                new_lines.append(row)
            else:
                new_lines.append([row[0]]+[str(float(temp)-273.15) for temp in row[1:]])
            line_count += 1
    return new_lines


def update_temperature_csv(path, rows):
    with open(path, mode='w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in rows:
            csv_writer.writerow(row)


def temp_to_celcius(path):
    rows = calculate_temperature(f"{path}.csv")
    update_temperature_csv(f"{path}_celcius.csv", rows)
