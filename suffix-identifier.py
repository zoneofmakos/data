import csv
import re

filename = "combined.csv"

suffixes = set()

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        if len(row) < 2:
            continue

        link = row[1].strip().strip("/")

        # Find the first 4-digit year and capture everything after it
        m = re.search(r"\b(19|20)\d{2}-(.+)$", link)
        if m:
            suffixes.add(m.group(2))

print(f"Found {len(suffixes)} unique suffixes:\n")

for suffix in sorted(suffixes):
    print(suffix)
