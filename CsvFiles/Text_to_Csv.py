import csv
import itertools

txt_file = r"c:\users\lorib\documents\passwordreset.txt"
csv_file = r"c:\users\lorib\documents\passwordreset.csv"

with open(txt_file, 'r') as infile, open(csv_file, 'w') as outfile:
    stripped = (line.strip() for line in infile)
    lines = (line.split('\t') for line in stripped if line)
    writer = csv.writer(outfile)
    writer.writerows(lines)
