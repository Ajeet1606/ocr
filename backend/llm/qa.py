import subprocess

def load_markdown(path="outputs/document.md"):
    with open(path, "r") as f:
        return f.read()

def build_prompt(document, question):
    return f"""
You are a strict assistant.

Answer the question ONLY using the document below.
If the answer is not present, say exactly:
"Not present in the document."

Document:
{document}

Question:
{question}

Answer:
""".strip()


def ask_llm(prompt, model="mistral"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()
