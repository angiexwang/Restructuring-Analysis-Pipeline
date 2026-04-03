import os
import csv
import pandas as pd

# ——— CONFIG ———
INPUT_FOLDER = 'restructuring_reasons'      # folder with .csv files
OUTPUT_CSV   = 'restructuring_reasons_summary.csv'  # merged output file
# —————————

def normalize_reason(reason):
    """Standardize reason string for deduplication: lowercase and strip."""
    return reason.strip().lower()

def main():
    combined = {}

    for fname in sorted(os.listdir(INPUT_FOLDER)):
        if not fname.lower().endswith('.csv'):
            continue
        fullpath = os.path.join(INPUT_FOLDER, fname)
        df = pd.read_csv(fullpath, header=0)

        for _, row in df.iterrows():
            try:
                reason_raw = str(row.iloc[0]).strip()
                count = int(row.iloc[1])
            except (IndexError, ValueError, TypeError):
                print(f"[WARN] Skipping bad row in {fname}")
                continue

            reason_key = normalize_reason(reason_raw)
            if reason_key in combined:
                combined[reason_key]['count'] += count
            else:
                combined[reason_key] = {'original': reason_raw, 'count': count}

        print(f"[OK] Processed {fname}")

    # Write final output sorted alphabetically by reason
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(['Reason', 'Count'])
        for reason_key in sorted(combined.keys()):
            item = combined[reason_key]
            writer.writerow([item['original'], item['count']])

    print(f"\nDone! {len(combined)} unique reasons written to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
