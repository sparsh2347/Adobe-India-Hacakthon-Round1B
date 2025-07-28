import json
import os
import datetime
from pdf_parse import extract_sections_from_pdfs
from nlp_utils import compute_relevance_scores, summarize_section
from generate_output import build_output_json

# --- Load Input JSON ---
INPUT_DIR = "input/Collection 2"
INPUT_JSON_PATH = os.path.join(INPUT_DIR, "challenge1b_input.json")

with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
    input_data = json.load(f)

challenge_id = input_data["challenge_info"]["challenge_id"]
documents_info = input_data["documents"]
persona = input_data["persona"]["role"]
job = input_data["job_to_be_done"]["task"]

# --- Prepare list of file paths ---
pdf_dir = "input/Collection 2/PDFs"
pdf_files = [os.path.join(pdf_dir, doc["filename"]) for doc in documents_info]
pdf_filenames = [doc["filename"] for doc in documents_info]

# --- Extract & Score ---
sections = extract_sections_from_pdfs(pdf_files)
ranked = compute_relevance_scores(sections, persona, job)
top_sections = ranked[:5]

# --- Refine text ---
refined = []
for sec in top_sections:
    refined_text = summarize_section(sec["text"])
    refined.append({
        "document": sec["document"],
        "refined_text": refined_text,
        "page_number": sec["page_number"]
    })

# --- Build Output ---
output = build_output_json(pdf_filenames, persona, job, ranked[:5], refined)

# --- Save to output folder ---
os.makedirs("output", exist_ok=True)
with open("output/challenge1b_output.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Output written to output/challenge1b_output.json")
