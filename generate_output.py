import datetime
import os

def build_output_json(documents, persona, job, extracted, refined):
    return {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": i + 1,
                "page_number": sec["page_number"]
            }
            for i, sec in enumerate(extracted)
        ],
        "subsection_analysis": refined
    }
