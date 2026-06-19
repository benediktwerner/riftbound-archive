#!/usr/bin/env python3

import os, sys, re

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "RULES.pdf")
    exit(1)

file = sys.argv[1]

if not file.endswith(".pdf"):
    print("File is not a .pdf:", file)
    exit(1)

txtfile = file.replace(".pdf", ".txt")
outfile = file.replace(".pdf", "-unnumbered.txt")

if not os.path.isfile(txtfile):
    os.system(f"pdftotext -raw '{file}' > '{txtfile}'")

with open(txtfile) as f:
    text = f.read()

PATTERNS = [
    r"\d{3}\.?",
    r"\d{3}\.\d+\.?",
    r"\d{3}\.\d+\.[a-z]\.?",
    r"\d{3}\.\d+\.[a-z]\.\d+\.?",
    r"\d{3}\.\d+\.[a-z]\.\d+\.[a-z]\.?",
    r"\d{3}\.\d+\.[a-z]\.\d+\.[a-z]\.\d+\.?",
]

text = re.sub(r"\x0c", "\n", text)
text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)
text = re.sub(r"\n([^0-9])", r" \1", text)

for p in PATTERNS:
    text = re.sub(r"\n" + p + "-" + p, r" XXX-XXX", text)

for i, p in enumerate(PATTERNS):
    text = re.sub("^" + p + " ", "  " * i + "- ", text, flags=re.MULTILINE)
    text = re.sub(" " + p + " ", " XXX. ", text)
    text = re.sub(" " + p + "\n", " XXX.\n", text)
    text = re.sub(" " + p + ",", " XXX,", text)

with open(outfile, "w") as of:
    of.write(text)
