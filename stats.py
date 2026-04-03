import os
import csv
import numpy as np
import pandas as pd
from collections import defaultdict

# List of folder paths to process
folders = ['hannah',
           'kristen',
           'krithika',
           'weiyang',
           'gpt']

# Questions to exclude from statistics (case-insensitive, exact match)
excluded_questions = {'cik', 'name', 'fiscal year end', 'url'}

def compute_statistics_by_item(folder_path):
    item_question_ratings = {
        'item7': defaultdict(list),
        'item8': defaultdict(list),
    }

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        lower_name = filename.lower()

        if 'item7' in lower_name:
            item_key = 'item7'
        elif 'item8' in lower_name:
            item_key = 'item8'
        else:
            continue

        # Handle CSV files
        if filename.endswith('.csv'):
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row:
                        continue
                    question = row[list(row.keys())[0]].strip()
                    if question.lower() in excluded_questions:
                        continue
                    try:
                        rating = int(row[list(row.keys())[1]])
                    except (ValueError, TypeError):
                        continue
                    if rating in (1, 2, 3):
                        item_question_ratings[item_key][question].append(rating)

        # Handle Excel files
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
            if df.shape[1] < 2:
                continue
            question_col = df.columns[0]
            rating_col = df.columns[1]
            for _, row in df.iterrows():
                question = str(row[question_col]).strip()
                if question.lower() in excluded_questions:
                    continue
                try:
                    rating = int(row[rating_col])
                except (ValueError, TypeError):
                    continue
                if rating in (1, 2, 3):
                    item_question_ratings[item_key][question].append(rating)

    # Write stats for each item
    folder_name = os.path.basename(os.path.normpath(folder_path))
    for item_key, question_ratings in item_question_ratings.items():
        output_file = f"{folder_name}_{item_key}_statistics.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for question, ratings in question_ratings.items():
                data = np.array(ratings)
                mean = np.mean(data)
                median = np.median(data)
                std_dev = np.std(data, ddof=1) if len(data) > 1 else 0.0
                q1 = np.percentile(data, 25)
                q3 = np.percentile(data, 75)
                count = len(data)

                f.write(f"Question: {question}\n")
                f.write(f"  Count: {count}\n")
                f.write(f"  Mean: {mean:.2f}\n")
                f.write(f"  Median: {median:.2f}\n")
                f.write(f"  Standard Deviation: {std_dev:.2f}\n")
                f.write(f"  Q1 (25th percentile): {q1}\n")
                f.write(f"  Q3 (75th percentile): {q3}\n")
                f.write("\n")
        print(f"Saved statistics for {item_key} in folder '{folder_name}' to '{output_file}'")

# Run it
for folder in folders:
    compute_statistics_by_item(folder)
