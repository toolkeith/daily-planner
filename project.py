import re
import csv
from tabulate import tabulate


def main():
    header_names = ["From", "To", "Acivities/Tasks"]
    activity_lists = []

    while True:
        print(tabulate(sort_list(activity_lists), header_names, tablefmt="grid"))

        try:
            start_time = validate_time(input("From: "))
            end_time = validate_time(input("To: "))

            if (
                start_time.split(":")[0] >= end_time.split(":")[0]
                and start_time.split(":")[1] >= end_time.split(":")[1]
            ):
                raise ValueError

            activity = input("Acivities/Tasks: ")

        except ValueError:
            print("Invalid time range")

        else:
            activity_list = [start_time, end_time, activity]
            activity_lists.append(activity_list)

            with open("daily-planner.csv", "w", newline="") as file:
                writer = csv.writer(file)

                for row in sort_list(activity_lists):
                    writer.writerow(row)


def validate_time(input_time):
    match = re.search(r"^(0?\d|1\d|2[0-3]):([0-5]\d)$", input_time)
    if not match:
        raise ValueError

    return input_time


def sort_list(activity_lists):
    sorted_list = sorted(activity_lists, key=lambda x: int(x[0].split(":")[0]))

    return sorted_list


if __name__ == "__main__":
    main()
