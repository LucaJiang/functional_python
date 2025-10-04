# ===== IMPERATIVE PROGRAMMING APPROACH =====
# Focus: HOW to perform operations step by step
# summarize student scores

## Input CSV format:
# Name,Class,Subject,Score
# Alice,A02,Science,90
# Bob,A01,English,SomeError

# 1. Calculate Grade based on Score
# 2. Summary statistics: average score per class, subject, overall. Be careful of error values.

import pandas as pd
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Summarize student scores")
parser.add_argument(
    "-n",
    "--num-records",
    type=int,
    default=100,
    help="Number of records in the dataset (default: 100)",
)
args = parser.parse_args()

# Load the data
num_records = args.num_records
target_dataset = f"student_scores_{num_records}.csv"
data_path = os.path.join(os.path.dirname(__file__), "data", target_dataset)
df = pd.read_csv(data_path)

# Initialize variables for tracking state
students_data = []
class_totals = {}
class_counts = {}
subject_totals = {}
subject_counts = {}
overall_total = 0
overall_count = 0

# Process each row in the dataframe
for index, row in df.iterrows():
    # Extract data from current row
    name = row["Name"]
    student_class = row["Class"]
    subject = row["Subject"]
    score_str = row["Score"]

    # Handle score conversion with error checking
    try:
        score = float(score_str)
        is_valid_score = True
    except ValueError:
        is_valid_score = False

    # Calculate grade based on score
    if is_valid_score:
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
    else:
        grade = "Error"

    # Create student record
    student_record = {
        "Name": name,
        "Class": student_class,
        "Subject": subject,
        "Score": score,
        "Grade": grade,
    }
    students_data.append(student_record)

    # Update statistics for valid scores
    if is_valid_score:
        # Update overall statistics
        overall_total += score
        overall_count += 1

        # Update class statistics
        if student_class not in class_totals:
            class_totals[student_class] = 0
            class_counts[student_class] = 0
        class_totals[student_class] += score
        class_counts[student_class] += 1

        # Update subject statistics
        if subject not in subject_totals:
            subject_totals[subject] = 0
            subject_counts[subject] = 0
        subject_totals[subject] += score
        subject_counts[subject] += 1

# Calculate averages
overall_average = overall_total / overall_count if overall_count > 0 else 0

class_averages = {}
for cls in class_totals:
    class_averages[cls] = class_totals[cls] / class_counts[cls]

subject_averages = {}
for subj in subject_totals:
    subject_averages[subj] = subject_totals[subj] / subject_counts[subj]

# Display results
print("IMPERATIVE PROGRAMMING RESULTS")
print("=" * 50)
print(f"Overall Average Score: {overall_average:.2f}")
print(f"Valid Scores Processed: {overall_count}")
print(f"Invalid Scores: {len(df) - overall_count}")

print("\nClass Averages:")
for cls, avg in class_averages.items():
    print(f"  {cls}: {avg:.2f}")

print("\nSubject Averages:")
for subj, avg in subject_averages.items():
    print(f"  {subj}: {avg:.2f}")
