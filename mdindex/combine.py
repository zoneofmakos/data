import csv
from pathlib import Path

input_dir = Path(".")
output_file = "combined.csv"

csv_files = sorted(input_dir.glob("*.csv"))
seen_links = set(
    [
        "/tamil-2025-movies-tamil-movie/",
        "/go-to-tamil-2024-movies-page-tamil-movie/",
        "/2024-tamil-movie/",
        "/tamil-2026-movies/",
        "/bigg-boss-2025-tamil-season-9/",
    ]
)

with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)

    for csv_file in csv_files:
        if csv_file.name == output_file:
            continue

        print(f"Processing {csv_file.name}")

        with open(csv_file, "r", newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)

            for row in reader:
                if len(row) < 2:
                    continue

                link = row[1].strip()

                if link in seen_links:
                    continue

                seen_links.add(link)
                writer.writerow(row)

print(f"\nDone! Combined {len(csv_files)} files into {output_file}")
print(f"Unique links written: {len(seen_links)}")
