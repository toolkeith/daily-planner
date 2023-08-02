# Daily Planner - CS50P Final Project
#### Video Demo:  https://www.youtube.com

## Description:
The Daily Planner is a command-line tool designed to help users plan their daily activities and create a printable PDF output. The program allows users to timeblock their day by entering the start time, end time, and a description of each activity or task they want to accomplish. The user must ensure that the input times are in the correct format (24-hour format). The tasks/activities are stored in a list and then displayed in a tabular format for easy viewing and management.

## Files and Functionality
- `project.py`: This is the main Python script that runs the daily planner. It takes the date input from the command-line arguments, validates it, and proceeds to ask users to input their daily activities. It includes functions for time validation, sorting the activities, and deleting tasks by their index. It also utilizes the `tabulate` library to display the activities in a formatted table.

- `FPDF` Library: The program uses the `FPDF` library to generate a PDF report of the daily planner. The `DailyPlannerPDF` class is a custom class that inherits from `FPDF`, and it includes a header method to add a title and date to the pdf output. The `save_to_pdf` function utilizes this custom class to generate the PDF file.

- `validate_date`: This function validates the date input from the command-line arguments to ensure that it is in the correct format and is today or a future date.

- `validate_time`: This function validates the time input to ensure that it is in the correct 24-hour format, using **regular expressions** to match the pattern.

- `sort_list`: This function sorts the list of activities based on their start times, ensuring they are displayed in chronological order.

- `delete_task_by_id`: This function allows users to delete a task from the activity list based on its index.

## Running the Project
To run the Daily Planner, execute the `project.py` script with the desired date in the format "YYYY-MM-DD" as a command-line argument. Make sure that the date is today or at some future dates. For example:
```
python project.py 2023-08-01
```
## Keyboard Shortcuts
Follow the on-screen instructions to input your start times, end times and activities. Additionally, you may use the following keyboard shortcuts:

| Keyboard Input | Action               |
| -------------- | -------------------- |
| Ctrl+D         | Delete an entry      |
| Ctrl+C         | Save to PDF and exit |
| Ctrl+Z         | Exit the program     |

- `Ctrl+D`: Pressing `Ctrl+D` (EOFError) exits the activity input loop and allows you to delete a task using its index. 
- `Ctrl+C`: Pressing `Ctrl+C` (KeyboardInterrupt) allows you to exit the program and be able to save your activities in a pdf file. 
- `Ctrl+Z`: Pressing `Ctrl+Z` exits the program without saving to a pdf file.

## Test Cases
The project includes test cases for some of the custom functions. To run the tests, make sure you have pytest installed, and then execute the following command in the terminal, in the project directory:
```
pytest test_project.py
```
The test cases ensure that the time and date validations work correctly and that the sorting and deletion functions behave as expected.

## Requirements
The project requires the following libraries, which can be installed using the following command in the terminal:

```
pip install -r requirements.txt
```
- tabulate
- fpdf2
- pytest

## Conclusion
This project was a great learning experience, allowing me to practice Python programming, date and time handling, regular expressions, working with external libraries (tabulate, fpdf) for data visualization and PDF generation, time validation using regular expressions, and command-line interface design using sys.argv. Through the development of this Daily Planner, I gained valuable insights into structuring a Python project with multiple functions and modules. The project includes test cases using pytest to ensure the reliability and correctness of the functions, covering time and date validation, list sorting, and list deletion functionalities. I hope this Daily Planner can be a helpful tool for others in organizing their daily activities by providing a clear view of the day's tasks and generating a printable PDF report, enabling users to plan and manage their time more efficiently.

