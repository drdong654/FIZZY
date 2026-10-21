import csv, os

from datasets import load_dataset


ds = load_dataset("syvai/danish-personas")      # DatasetDict: {"train": Dataset}
personas = ds["train"]                          # the dataset itself, ~100,000 rows

columns = ["persona_id", "age", "sex", "region", "persona"] # Выбираем только нужные колонки
sample = personas.select(range(20)).select_columns(columns) # Выбираем первые 20 строк и только нужные колонки


rows = [
    {
        "id": item["persona_id"],
        "age": item["age"],
        "gender": item["sex"],
        "region": item["region"],
        "description": item["persona"],
    }
    for item in sample
]
os.makedirs("data", exist_ok=True)
with open("data/personas_20.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved: data/personas_20.csv")

    