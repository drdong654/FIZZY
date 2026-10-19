import os

from datasets import load_dataset

ds = load_dataset("syvai/danish-personas")      # DatasetDict: {"train": Dataset}
personas = ds["train"]                          # the dataset itself, ~100,000 rows

# 1. Look inside
print(personas)                 # row count and column names
print(personas.features)        # column types
print(personas[0])              # one full persona