import csv

input_path = "data/cleaned_injection_prompts.csv"
output_path = "data/fixed_injection_prompts.csv"

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for i, row in enumerate(reader):
        if len(row) == 2:
            writer.writerow(row)
        else:
            print(f" Skipping malformed line {i + 1}: {row}")
