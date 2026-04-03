import os
import csv
import pandas as pd
import re

# ——— CONFIG ———
INPUT_FOLDER = 'hannah'                                # folder with .xlsx/.xls/.csv files
OUTPUT_CSV   = 'cost_breakdown_hannah.csv'      # summary output
MATCH_KEY    = 'break-down'                             # match substring (case-insensitive)
# —————————

def extract_reasons_from_file(path, match_key):
    """Reads a file (.csv or .xlsx), finds the row with match_key in column 1, and extracts non-blank cells in columns 2+."""
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path, dtype=str, on_bad_lines='skip', engine='python')
    else:
        df = pd.read_excel(path, dtype=str, sheet_name=0)

    for _, row in df.iterrows():
        if pd.isna(row.iloc[0]):
            continue
        first_col = str(row.iloc[0]).strip().lower().replace('“', '"').replace('”', '"')
        if match_key in first_col:
            return [str(cell).strip()
                    for cell in row.iloc[1:]
                    if pd.notna(cell) and str(cell).strip()]
    return []


def clean_text(text):
    """Strip after colon, remove non-letter characters, lowercase and strip."""
    text = text.split(':')[0]         # take part before colon
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove everything except letters and spaces
    return text.strip().lower()

def main():
    tally = {}
    for fname in sorted(os.listdir(INPUT_FOLDER)):
        if not fname.lower().endswith(('.xlsx', '.xls', '.csv')):
            continue
        fullpath = os.path.join(INPUT_FOLDER, fname)
        reasons = extract_reasons_from_file(fullpath, MATCH_KEY)
        if not reasons:
            print(f"[SKIP] no '{MATCH_KEY}' row in {fname}")
            continue
        print(f"[OK] found {len(reasons)} reason(s) in {fname}")
        for r in reasons:
            cleaned = clean_text(r)
            if cleaned:
                tally[cleaned] = tally.get(cleaned, 0) + 1

    # write summary CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(['Reason', 'Count'])
        for reason, count in sorted(tally.items(), key=lambda x: -x[1]):
            writer.writerow([reason, count])

    print(f"\nDone! {len(tally)} unique cleaned reasons written to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
