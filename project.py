import re
import csv
from tabulate import tabulate
from fpdf import FPDF


def main():
    header_names = ["From", "To", "Acivities/Tasks"]
    activity_lists = []
    filename = "pdf"

    while True:
        print(tabulate(sort_list(activity_lists), header_names, tablefmt="grid"))
        print("Ctrl+D to exit")

        try:
            start_time = validate_time(input("From: "))
            end_time = validate_time(input("To: "))

            if int(start_time.split(":")[0]) == int(end_time.split(":")[0]) and int(
                start_time.split(":")[1]
            ) >= int(end_time.split(":")[1]):
                raise ValueError

            activity = input("Acivities/Tasks: ")

        except ValueError:
            print("Invalid time range")

        except EOFError:
            print(f"\nPDF file created: {filename}")

            class PDF(FPDF):
                def header(self):
                    self.set_font("Helvetica", "B", 20)
                    self.cell(180, 10, "Daily Planner", align="C")
                    self.ln(20)

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=16)
            activity_lists.insert(0, header_names)

            with pdf.table(
                width=150,
                col_widths=(15, 15, 60),
                first_row_as_headings=True,
                text_align=("CENTER", "CENTER", "CENTER"),
            ) as table:
                for data_row in activity_lists:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)

            pdf.output("table.pdf")
            break

        else:
            activity_list = [start_time, end_time, activity]
            activity_lists.append(activity_list)

            # with open("daily-planner.csv", "w", newline="") as file:
            #     writer = csv.writer(file)

            #     for row in sort_list(activity_lists):
            #         writer.writerow(row)


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
