# ===== FUNCTIONAL PROGRAMMING APPROACH =====
# Focus: WHAT transformations to apply to data

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


def clean_score(score_value):
    """
    Convert score to numeric, handling errors gracefully.

    Args:
        score_value: Score value as string or number

    Returns:
        Clean numeric score or None if invalid
    """
    try:
        return float(score_value)
    except (ValueError, TypeError):
        return None


def calculate_grade(score):
    """
    Calculate letter grade based on numerical score.

    Args:
        score: Numerical score value

    Returns:
        Letter grade (A-F) or 'Error' for invalid scores
    """
    if score is None:
        return "Error"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def add_grade_column(student_df):
    """
    Add grade column to student dataframe.

    Args:
        student_df: DataFrame with student data

    Returns:
        DataFrame with added Grade column
    """
    return student_df.assign(
        Score=student_df["Score"].apply(clean_score),
        Grade=student_df["Score"].apply(clean_score).apply(calculate_grade),
    )


def filter_valid_scores(student_df):
    """
    Filter dataframe to include only valid scores.

    Args:
        student_df: DataFrame with student data

    Returns:
        Filtered DataFrame with valid scores only
    """
    return student_df[student_df["Score"].notna()]


def calculate_group_average(student_df, group_column):
    """
    Calculate average scores for a given grouping column.

    Args:
        student_df: DataFrame with student data
        group_column: Column name to group by

    Returns:
        Dictionary of group averages
    """
    return student_df.groupby(group_column)["Score"].mean().to_dict()


def pipeline_processing(file_path):
    """
    Main processing pipeline using functional composition.

    Args:
        file_path: Path to CSV file

    Returns:
        Dictionary with processed results
    """
    # Read and process data through pipeline
    processed_df = pd.read_csv(file_path).pipe(add_grade_column)

    valid_scores_df = processed_df.pipe(filter_valid_scores)

    # Calculate statistics using functional approach
    overall_avg = valid_scores_df["Score"].mean()
    class_avgs = calculate_group_average(valid_scores_df, "Class")
    subject_avgs = calculate_group_average(valid_scores_df, "Subject")

    return {
        "processed_data": processed_df,
        "overall_average": overall_avg,
        "class_averages": class_avgs,
        "subject_averages": subject_avgs,
        "valid_count": len(valid_scores_df),
        "total_count": len(processed_df),
    }


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

# Execute functional pipeline
results = pipeline_processing(data_path)

print("FUNCTIONAL PROGRAMMING RESULTS")
print("=" * 50)
print(f"Overall Average Score: {results['overall_average']:.2f}")
print(f"Valid Scores Processed: {results['valid_count']}")
print(f"Invalid Scores: {results['total_count'] - results['valid_count']}")

print("\nClass Averages:")
for cls, avg in results["class_averages"].items():
    print(f"  {cls}: {avg:.2f}")

print("\nSubject Averages:")
for subj, avg in results["subject_averages"].items():
    print(f"  {subj}: {avg:.2f}")
