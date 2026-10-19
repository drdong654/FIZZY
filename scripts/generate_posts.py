from agno.agent import Agent
from agno.models.ollama import Ollama

from scripts.import_personas import load_personas


def main() -> None:
    sample = load_personas(limit=1)
    person = sample[0]["persona"]

    agent = Agent(
        model=Ollama(
            id="qwen3:4b",
            host="http://localhost:11434",
            api_key=None,
            options={"temperature": 0.8},
        ),
        markdown=False,
    )

    prompt = (
        "Write a realistic social media post in English about TechHeads 2026 "
        "from the perspective of this fictional person. "
        "Use their personality and background. The mood may be positive, "
        "neutral, or critical. Write only the post, 1–2 sentences.\n\n"
        f"Description (Danish): {person['description']}\n"
        f"Personality scores: {person['ocean']}"
    )

    result = agent.run(prompt)
    print(result.content)


if __name__ == "__main__":
    main()
