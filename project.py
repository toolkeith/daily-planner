import sys
import re
from tabulate import tabulate
from fpdf import FPDF
from datetime import datetime, date


class DailyPlannerPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(180, 10, "Daily Planner", align="C")
        self.ln(8)
        self.set_font("Helvetica", "I", 14)
        self.cell(180, 10, f"({date.today().strftime('%B %d, %Y')})", align="C")
        self.ln(10)


def save_to_pdf(activity_lists, filename):
    pdf = DailyPlannerPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    header_names = ["From", "To", "Activities/Tasks"]
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

    pdf.output(filename)


def print_activities_table(activity_lists):
    header_names = ["From", "To", "Acivities/Tasks"]
    print(
        tabulate(
            sort_list(activity_lists),
            headers=["ID"] + header_names,
            showindex="always",
            tablefmt="grid",
        )
    )


def validate_time(input_time):
    match = re.search(r"^(0\d|1\d|2[0-3]):([0-5]\d)$", input_time)
    if not match:
        raise ValueError("\n********** Invalid time format! **********\n")

    return input_time


def sort_list(activity_lists):
    sorted_list = sorted(activity_lists, key=lambda x: int(x[0].split(":")[0]))

    return sorted_list


def delete_task_by_id(activity_lists, task_id):
    if 0 <= task_id < len(activity_lists):
        activity_lists = activity_lists.pop(task_id)
        return activity_lists


def validate_date(date_input):
    date_format = "%Y-%m-%d"

    try:
        checked_date = datetime.strptime(date_input, date_format)
        date_today = date.today()

        if checked_date.date() < date_today:
            sys.exit(f"Date must be from today ({date_today}) onwards!")
        return date_input

    except ValueError:
        sys.exit("Invalid date format!")


def main():
    if len(sys.argv) != 2:
        sys.exit("Use this format: python project 2023-08-01")

    else:
        date_input = validate_date(sys.argv[1])

        activity_lists = []
        filename = f"{date_input}_daily-planner.pdf"

        while True:
            print_activities_table(activity_lists)

            keyboard_keys = [
                ["Ctrl+D", "Delete an entry"],
                ["Ctrl+C", "Save to PDF and exit"],
                ["Ctrl+Z", "Exit the program"],
            ]

            print(tabulate(keyboard_keys, tablefmt="plain"))

            try:
                start_time = validate_time(input("From (24-hr format): "))
                end_time = validate_time(input("To (24-hr format): "))

                if int(start_time.split(":")[0]) == int(end_time.split(":")[0]) and int(
                    start_time.split(":")[1]
                ) >= int(end_time.split(":")[1]):
                    raise ValueError("\n********** Invalid time range! **********\n")

                activity = input("Acivities/Tasks: ")

            except ValueError as e:
                print(str(e))

            except EOFError:
                while True:
                    if not activity_lists:
                        print("\n\n********** No tasks in the list! **********\n")
                        break

                    try:
                        task_id = int(
                            input("\nDelete Task (ID) or Ctrl+D to go back: ")
                        )
                        delete_task_by_id(activity_lists, task_id)
                        print(f"Task {task_id} deleted successfully!!!")
                        break

                    except ValueError:
                        print(
                            "********** Invalid Task ID! Please enter a valid index! **********",
                            end="",
                        )
                        continue

                    except KeyboardInterrupt:
                        pass

                    except EOFError:
                        break

            except KeyboardInterrupt:
                print(f"\nPDF file created: {filename}")
                save_to_pdf(activity_lists, filename)
                break

            else:
                activity_list = [start_time, end_time, activity]
                activity_lists.append(activity_list)


if __name__ == "__main__":
    main()
