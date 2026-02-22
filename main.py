import os
import numpy
from pathlib import Path

def clear_console():
    """Clears the console screen."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

STUDENT_AXIS = 1
SUBJECT_AXIS = 0


#! Load data
base_path = Path(__file__).parent
file_path = base_path / "student_data.csv"

raw_data = numpy.genfromtxt(
    file_path,
    delimiter=",",
    skip_header=1,
)



roll_numbers = raw_data[:, 0]
marks = raw_data[:, 1:]


#! Validation
def validate_data(roll_numbers, marks, min_mark=0, max_mark=100):

    if marks.size == 0:
        raise ValueError("Marks data is empty.")

    if roll_numbers.size != marks.shape[0]:
        raise ValueError("Mismatch between roll numbers and marks rows.")

    if len(numpy.unique(roll_numbers)) != roll_numbers.shape[0]:
        raise ValueError("Duplicate roll numbers detected.")

    if numpy.isnan(marks).any():
        raise ValueError("Missing values detected in marks.")

    if ((marks < min_mark) | (marks > max_mark)).any():
        raise ValueError("Marks must be between 0 and 100.")

    return marks


marks = validate_data(roll_numbers, marks)


#! Analytics
def analyze_data(data, axis=None):
    return {
        "mean": numpy.mean(data, axis=axis),
        "median": numpy.median(data, axis=axis),
        "min": numpy.min(data, axis=axis),
        "max": numpy.max(data, axis=axis),
        "std": numpy.std(data, axis=axis)
    }


row_stats = analyze_data(marks, axis=STUDENT_AXIS)
col_stats = analyze_data(marks, axis=SUBJECT_AXIS)


#! Evaluation
def find_topper(roll_numbers, marks):
    averages = numpy.mean(marks, axis=STUDENT_AXIS)
    index = numpy.argmax(averages)
    return roll_numbers[index], averages[index]


def pass_fail_mask(marks, pass_mark=50):
    return numpy.any(marks < pass_mark, axis=STUDENT_AXIS)


failed_count = int(numpy.sum(pass_fail_mask(marks)))
passed_count = int(numpy.sum(~pass_fail_mask(marks)))
topper_roll, topper_avg = find_topper(roll_numbers, marks)


#! Report
def print_report():
    clear_console()
    print("\n" + "=" * 50)
    print("STUDENT PERFORMANCE")
    print("=" * 50)

    for i, roll in enumerate(roll_numbers):
        print(
            f"Roll {int(roll)} | "
            f"Mean: {row_stats['mean'][i]:.2f} | "
            f"Min: {row_stats['min'][i]:.0f} | "
            f"Max: {row_stats['max'][i]:.0f}"
        )

    print("\n" + "=" * 50)
    print("SUBJECT PERFORMANCE")
    print("=" * 50)

    for i in range(len(col_stats["mean"])):
        print(
            f"Subject {i+1} | "
            f"Mean: {col_stats['mean'][i]:.2f} | "
            f"Std: {col_stats['std'][i]:.2f}"
        )

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    print("Passed:", passed_count)
    print("Failed:", failed_count)
    print(f"Topper: Roll {int(topper_roll)} (Avg: {topper_avg:.2f})")


def text_report():
    report_path = base_path / "report.txt"
    with open(report_path, "w") as f:
        f.write("STUDENT PERFORMANCE\n")
        f.write("=" * 50 + "\n")

        for i, roll in enumerate(roll_numbers):
            f.write(
                f"Roll {int(roll)} | "
                f"Mean: {row_stats['mean'][i]:.2f} | "
                f"Min: {row_stats['min'][i]:.0f} | "
                f"Max: {row_stats['max'][i]:.0f}\n"
            )

        f.write("\n" + "=" * 50 + "\n")
        f.write("SUBJECT PERFORMANCE\n")
        f.write("=" * 50 + "\n")

        for i in range(len(col_stats["mean"])):
            f.write(
                f"Subject {i+1} | "
                f"Mean: {col_stats['mean'][i]:.2f} | "
                f"Std: {col_stats['std'][i]:.2f}\n"
            )

        f.write("\n" + "=" * 50 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 50 + "\n")

        f.write("Passed: " + str(passed_count) + "\n")
        f.write("Failed: " + str(failed_count) + "\n")
        f.write(f"Topper: Roll {int(topper_roll)} (Avg: {topper_avg:.2f})\n")


#! Menu
def report_menu():
    while True:
        try:
            clear_console()

            print("\n" + "=" * 50)
            print("REPORT MENU")
            print("=" * 50)
            print("1. View Report in terminal")
            print("2. Report in text file")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":   
                print_report()
            elif choice == "2":
                text_report()
            elif choice == "3":
                    exit()
            else:
             print("Invalid choice. Please try again.")
        except Exception as e:
            print("Error:", e)
            break


if __name__ == "__main__":
    report_menu()