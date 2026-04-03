import csv
import os
import re

# ——— CONFIG ———
INPUT_CSV   = 'restructuring_reasons_summary.csv'
OUTPUT_CSV  = 'restructuring_reasons_summary_normalized.csv'

# common filler words to strip when normalizing
STOPWORDS = {
    'the', 'and', 'to', 'of', 'for', 'in', 'a', 'an',
    'on', 'by', 'with', 'from', 'its', 'their', 'our',
}
# —————————

def make_key(text):
    """
    Lowercase, strip punctuation, split into words,
    remove stopwords, then rejoin.
    """
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    words = cleaned.split()
    filtered = [w for w in words if w not in STOPWORDS]
    key = ' '.join(filtered)
    return key or text.lower()

def normalize_reasons(input_csv, output_csv):
    """
    Reads input_csv, merges rows whose 'Reason' normalize to the same key,
    summing their counts, and writes the result to output_csv.
    """
    merged = {}
    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header[:2] != ['Reason', 'Count']:
            raise ValueError(f"Expected header ['Reason','Count'], got {header}")

        for row in reader:
            if len(row) < 2:
                continue
            reason, count_str = row[0].strip(), row[1].strip()
            try:
                count = int(count_str)
            except ValueError:
                continue

            key = make_key(reason)
            if key in merged:
                merged[key]['count'] += count
            else:
                merged[key] = {'repr': reason, 'count': count}

    # write alphabetically by the representative reason
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Reason', 'Count'])
        for data in sorted(merged.values(), key=lambda d: d['repr'].lower()):
            writer.writerow([data['repr'], data['count']])

    print(f"Normalized summary written to {output_csv}, sorted alphabetically.")

if __name__ == '__main__':
    if not os.path.exists(INPUT_CSV):
        print(f"Error: input file '{INPUT_CSV}' not found.")
    else:
        normalize_reasons(INPUT_CSV, OUTPUT_CSV)
