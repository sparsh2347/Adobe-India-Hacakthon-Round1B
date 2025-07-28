import pdfplumber
import os

def extract_sections_from_pdfs(pdf_paths):
    sections = []
    for path in pdf_paths:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
                lines = group_by_lines(words)
                for line in lines:
                    text = " ".join([w['text'] for w in sorted(line, key=lambda w: w['x0'])])
                    font_size = line[0].get("size", 10)  # fallback
                    sections.append({
                        "document": os.path.basename(path),
                        "page_number": i + 1,
                        "section_title": text[:40],
                        "text": text,
                        "font_size": font_size
                    })
    return sections

def group_by_lines(words, y_tolerance=5):
    from collections import defaultdict
    lines = defaultdict(list)
    for word in words:
        key = round(word["top"] / y_tolerance) * y_tolerance
        lines[key].append(word)
    return list(lines.values())
