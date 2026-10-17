import json
import random
from urllib.parse import urlencode
from urllib.request import urlopen

DATASET = "syvai/danish-personas"
CONFIG = "default"
SPLIT = "train"
API = "https://datasets-server.huggingface.co"


def get_json(endpoint: str, **params: object) -> dict:
    url = f"{API}/{endpoint}?{urlencode(params)}"
    with urlopen(url, timeout=15) as response:
        return json.load(response)

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

def main() -> None:
    metadata = get_json("size", dataset=DATASET)
    split = next(
        item for item in metadata["size"]["splits"]
        if item["config"] == CONFIG and item["split"] == SPLIT
    )
    total = split["num_rows"]

    indices = random.Random(42).sample(range(total), 20)
    personas = []

    for index in indices:
        data = get_json(
            "rows",
            dataset=DATASET,
            config=CONFIG,
            split=SPLIT,
            offset=index,
            length=1,
        )
        personas.append(data["rows"][0]["row"])


    prepared = [
        {
            "persona_key": row["persona_id"],
            "persona": persona_fields(row),
        }
        for row in personas
    ]

    keys = [item["persona_key"] for item in prepared]
    if len(prepared) != 20 or len(set(keys)) != 20:
        raise ValueError("Нужно ровно 20 разных персон")

    for item in prepared:
        person = item["persona"]
        if not person["description"] or any(
            score is None for score in person["ocean"].values()
        ):
            raise ValueError(f"Неполные данные персоны {item['persona_key']}")

    print(f"Подготовлено персон: {len(prepared)}")
    print("Первая:", prepared[0]["persona_key"], prepared[0]["persona"]["age"])
    print("Описание:", prepared[0]["persona"]["description"][:150])


if __name__ == "__main__":
    main()