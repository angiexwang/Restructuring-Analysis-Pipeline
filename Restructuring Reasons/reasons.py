import os
import csv

# ——— CONFIG ———
INPUT_FOLDER = 'gpt'       # ← change to your folder path
OUTPUT_CSV   = 'restructuring_reasons_gpt.csv'
MATCH_KEY    = "management stated reasons"
# —————————

def extract_reasons_from_file(filepath, match_key):
    """
    Reads a CSV that has header: Question,Answer 1,…Answer N
    Finds the row where the first column contains match_key (case‐insensitive),
    then returns all non‐empty cells in columns 2…end as reasons.
    """
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # skip header
        for row in reader:
            if not row:
                continue
            first = row[0].strip().lower()
            if match_key in first:
                # grab everything in columns 2…end
                return [cell.strip() for cell in row[1:] if cell and cell.strip()]
    return []

def main():
    tally = {}

    for fname in sorted(os.listdir(INPUT_FOLDER)):
        if not fname.lower().endswith('.csv'):
            continue
        path = os.path.join(INPUT_FOLDER, fname)
        reasons = extract_reasons_from_file(path, MATCH_KEY)
        if not reasons:
            print(f"[SKIP] no '{MATCH_KEY}' row in {fname}")
            continue
        print(f"[OK]  found {len(reasons)} reason(s) in {fname}")
        for r in reasons:
            tally[r] = tally.get(r, 0) + 1

    # Write summary out
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(['Reason', 'Count'])
        for reason, count in sorted(tally.items(), key=lambda x: -x[1]):
            writer.writerow([reason, count])

    print(f"\nDone! {len(tally)} unique reasons written to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
