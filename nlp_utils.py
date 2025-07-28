from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

model = SentenceTransformer("all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

def compute_relevance_scores(sections, persona, task):
    query = persona + " | " + task
    query_embedding = model.encode(query, convert_to_tensor=True)

    for sec in sections:
        sec_embedding = model.encode(sec["text"], convert_to_tensor=True)
        sec["score"] = float(util.cos_sim(query_embedding, sec_embedding)[0][0])

    return sorted(sections, key=lambda x: -x["score"])

def summarize_section(text, max_length=100):
    try:
        summary = summarizer(text[:1000], max_length=max_length, min_length=30, do_sample=False)[0]["summary_text"]
        return summary
    except:
        return text[:max_length]
