import sys
import re
from tabulate import tabulate
from fpdf import FPDF
from datetime import datetime, date


def main():
    date_format = "%Y-%m-%d"
    if len(sys.argv) != 2:
        sys.exit(
            f"\n********** Usage sample: python project {date.today()} **********\n"
        )

    else:
        # Using sys.argv to get the date to be used in naming the file and in PDF output
        date_input = validate_date(date_format, sys.argv[1])

        activity_lists = []
        filename = f"{date_input.strftime(date_format)}_daily-planner.pdf"

        while True:
            # Printing of activity table and keyboard actions
            print_activities_table(activity_lists)
            print_keyboard_action()

            try:
                # Validate time input
                start_time = validate_time(input("From (Use 24-hr format): "))
                end_time = validate_time(input("To (Use 24-hr format): "))

                # If same hour, end_time minutes must be greater than start_time minutes
                if int(start_time.split(":")[0]) == int(end_time.split(":")[0]) and int(
                    start_time.split(":")[1]
                ) >= int(end_time.split(":")[1]):
                    raise ValueError("\n********** Invalid time range! **********\n")

                activity = input("Acivities/Tasks: ")

            except ValueError as e:
                print(str(e))

            except EOFError:
                while True:
                    # No entries yet
                    if not activity_lists:
                        print("\n\n********** No tasks in the list! **********\n")
                        break

                    try:
                        task_id = int(
                            input("\nDelete Task (ID) or (Ctrl+D) to go back: ")
                        )
                        #  Task ID not in the list
                        if task_id < 0 or task_id >= len(activity_lists):
                            raise ValueError
                        else:
                            delete_task_by_id(activity_lists, task_id)
                            print(
                                f"\n********** Task {task_id} deleted successfully! **********\n"
                            )
                            break

                    except ValueError:
                        print(
                            "\n********** Invalid Task ID! Please enter a valid index! **********"
                        )
                        continue

                    except KeyboardInterrupt:
                        pass

                    except EOFError:
                        print()
                        break

            except KeyboardInterrupt:
                print(f"\nPDF file created: {filename}")
                save_to_pdf(activity_lists, filename, date_input)
                break

            else:
                activity_list = [start_time, end_time, activity]
                activity_lists.append(activity_list)


class DailyPlannerPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(180, 10, "Daily Planner", align="C")
        self.ln(8)
        self.set_font("Helvetica", "I", 14)
        self.cell(180, 10, f"({self.date_input.strftime('%B %d, %Y')})", align="C")
        self.ln(10)


def save_to_pdf(activity_lists, filename, date_input):
    pdf = DailyPlannerPDF()
    pdf.date_input = date_input
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    header_names = ["From", "To", "Activities/Tasks"]
    sorted_pdf_list = sort_list(activity_lists)
    sorted_pdf_list.insert(0, header_names)

    with pdf.table(
        width=150,
        col_widths=(15, 15, 60),
        first_row_as_headings=True,
        text_align=("CENTER", "CENTER", "CENTER"),
    ) as table:
        for data_row in sorted_pdf_list:
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


def print_keyboard_action():
    keyboard_keys = [
        ("Ctrl+D", "Delete an entry"),  # EOFError
        ("Ctrl+C", "Save to PDF and exit"),  # KeyboardInterrupt
        ("Ctrl+Z", "Exit the program"),
    ]
    print(
        tabulate(
            keyboard_keys,
            headers=["Keyboard Shortcut", "Action"],
            tablefmt="simple_outline",
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


# Validation for sys.argv[1] date input
def validate_date(date_format, date_input):
    try:
        checked_date = datetime.strptime(date_input, date_format)
        date_today = date.today()
        # Date checking - must be today or future date
        if checked_date.date() < date_today:
            sys.exit(
                f"\n********** Date must be from today({date_today}) onwards! **********\n"
            )
        return checked_date

    except ValueError:
        sys.exit("Invalid date format!")


if __name__ == "__main__":
    main()
