import csv
import json
import os
import random
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd

DATASET = "syvai/danish-personas"
CONFIG = "default"
SPLIT = "train"
API = "https://datasets-server.huggingface.co"
CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "personas_sample.json"


def get_json(endpoint: str, **params: object) -> dict:
    url = f"{API}/{endpoint}?{urlencode(params)}"
    for attempt in range(3):
        try:
            with urlopen(url, timeout=15) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise
            time.sleep(2**attempt)

    raise RuntimeError("Не удалось получить ответ Hugging Face")


def persona_fields(row: dict) -> dict:
    traits = (
        "openness",
        "conscientiousness",
        "extraversion",
        "agreeableness",
        "neuroticism",
    )

    return {
        "age": row["age"],
        "gender": row["sex"],
        "region": row["region"],
        "occupation": row.get("job_title") or row.get("job_function"),
        "ocean": {trait: row[f"{trait}_score"] for trait in traits},
        "description": row["persona"],
    }


def load_personas(limit: int = 20) -> list[dict]:
    if not 1 <= limit <= 20:
        raise ValueError("limit должен быть от 1 до 20")

    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        if cache["dataset"] != DATASET:
            raise ValueError("Кэш относится к другому датасету")
    else:
        metadata = get_json("size", dataset=DATASET)
        split = next(
            item for item in metadata["size"]["splits"]
            if item["config"] == CONFIG and item["split"] == SPLIT
        )
        cache = {"dataset": DATASET, "total": split["num_rows"], "rows": {}}

    indices = random.Random(42).sample(range(cache["total"]), 20)[:limit]
    personas = []

    for index in indices:
        key = str(index)
        if key not in cache["rows"]:
            data = get_json(
                "rows",
                dataset=DATASET,
                config=CONFIG,
                split=SPLIT,
                offset=index,
                length=1,
            )
            cache["rows"][key] = data["rows"][0]["row"]
            CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = CACHE_PATH.with_suffix(".tmp")
            temporary_path.write_text(
                json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            temporary_path.replace(CACHE_PATH)
        personas.append(cache["rows"][key])

    prepared = [
        {
            "persona_key": row["persona_id"],
            "persona": persona_fields(row),
        }
        for row in personas
    ]

    keys = [item["persona_key"] for item in prepared]
    if len(prepared) != limit or len(set(keys)) != limit:
        raise ValueError(f"Нужно ровно {limit} разных персон")

    for item in prepared:
        person = item["persona"]
        if not person["description"] or any(
            score is None for score in person["ocean"].values()
        ):
            raise ValueError(f"Неполные данные персоны {item['persona_key']}")

    return prepared


# Загрузка в базу подготовить в CSV и отправить в DBeaver, чтобы потом использовать в генерации постов ЛИБО через SQl




if __name__ == "__main__":
    sample = load_personas()
    rows = [
        {"persona_key": item["persona_key"], **item["persona"],
        "ocean": json.dumps(item["persona"]["ocean"])}   # dict → JSON string for the CSV
        for item in sample
    ]

    os.makedirs("data", exist_ok=True)
    with open("data/personas_20.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Saved: data/personas_20.csv")
    #sample.to_csv("data/personas_20.csv", index=False)
    print(len(sample))

    #print(f"Подготовлено персон: {len(sample)}")
    #print("Первая:", sample[0]["persona_key"], sample[0]["persona"]["age"])

