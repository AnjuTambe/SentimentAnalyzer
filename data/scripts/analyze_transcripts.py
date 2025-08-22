import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


input_folder = "scripts"
output_folder = "../../analysis"

os.makedirs(output_folder, exist_ok=True)

PROMPT_TEMPLATE = """
You are a financial analyst assistant. Analyze this earnings call transcript below and extract:
1. Management Sentiment (positive, neutral, negative)
2. Q&A Sentiment (tone during analyst-executive interaction)
3. Quarter-over-Quarter Tone Change (compared to previous non-missing quarter e.g. Q3 vs Q1)
4. Strategic Focuses (3–5 key themes the management emphasized)

Return output in JSON format.

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

transcripts = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])

print(f"transcripts {transcripts}")

for filename in transcripts:
    print("test")
    with open(os.path.join(input_folder, filename), "r") as f:
        transcript = f.read()

    prompt = PROMPT_TEMPLATE.format(transcript=transcript[:8000])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    analysis = response["choices"][0]["message"]["content"]
    print(f"Analyzed: {analysis}")
    out_file = filename.replace(".txt", "_analysis.json")

    with open(os.path.join(output_folder, out_file), "w") as f:
        f.write(analysis)

    print(f"Analyzed: {filename}")

print("Analysis complete for all transcripts.")
