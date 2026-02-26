import requests
import gradio as gr
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# URL for Flask backend URL
FLASK_BACKEND_URL = "http://127.0.0.1:5002"

# Globals used by graph functions (kept for your later graph tabs)
TOP_5_CWE = []
TOP_5_ATTACKS = []


def summarize_query(query: str, summarizer_engine: str) -> str:
    """
    TEMP: You said you'll fix exact content later.
    For now:
      - "None" returns the same text
      - other options still return the same text (placeholder)
    """
    return query


def split_into_list_and_summary(full_text: str):
    """
    TEMP split:
      first half -> list tab
      last half  -> summary tab
    Replace later with a marker split when your backend format is stable.
    """
    if not full_text:
        return "", ""
    mid = len(full_text) // 2
    list_part = full_text[:mid].strip()
    summary_part = full_text[mid:].strip()
    return list_part, summary_part


def get_backend_message_bert(message: str, mdl: str) -> str:
    bot_message = "Error: Attempt failed"
    try:
        md1 = 'gptoss'
        response = requests.post(f"{FLASK_BACKEND_URL}/search-{mdl}", json={"query": message}, timeout=120)
        if response.status_code == 200:
            data = response.json()
            cwe_results = data.get("CWE Results", [])
            attack_results = data.get("Attack Results", [])

            # If backend returns strings (summaries), combine them directly
            if isinstance(cwe_results, str) or isinstance(attack_results, str):
                return f"Top CWE Results:\n\n{cwe_results}\n\nTop Attack Results:\n\n{attack_results}"

            # Otherwise assume list-of-dicts
            cwe_formatted = "\n\n".join(
                [
                    f"CWE ID: {res.get('CWE ID','N/A')}\n"
                    f"Name: {res.get('Name','N/A')}\n"
                    f"Cosine Similarity: {res.get('Similarity','N/A')}\n"
                    f"Description: {res.get('Description','')}\n"
                    f"Extended Description: {res.get('Extended Description','')}"
                    for res in (cwe_results or [])
                ]
            )

            attack_formatted = "\n\n".join(
                [
                    f"Attack ID: {res.get('Attack ID','N/A')}\n"
                    f"Name: {res.get('Name','N/A')}\n"
                    f"Cosine Similarity: {res.get('Similarity','N/A')}\n"
                    f"Description: {res.get('Description','')}"
                    for res in (attack_results or [])
                ]
            )

            bot_message = f"Top CWE Results:\n\n{cwe_formatted}\n\nTop Attack Results:\n\n{attack_formatted}"
        else:
            bot_message = f"Error: Backend responded with status code {response.status_code}"
    except Exception as e:
        bot_message = f"Error: Couldn't connect to backend - {e}"
    return bot_message


def get_top_responses(bot_message: str):
    """
    Populates TOP_5_CWE and TOP_5_ATTACKS based on regex matches in the bot_message.
    """
    global TOP_5_CWE, TOP_5_ATTACKS
    top_5_results = re.findall(r"CWE ID:\s*(\d+)", bot_message)
    top_5_attacks = re.findall(r"Name:\s*([^\n]+)", bot_message)

    TOP_5_CWE = [cwe_id for cwe_id in top_5_results]
    TOP_5_ATTACKS = [attack_name for attack_name in top_5_attacks][-5:]


def handle_query(message: str, selected_model: str, summarizer_engine: str):
    """
    Returns TWO outputs:
      1) summary text (Tab: Summary)
      2) list/raw text (Tab: List)
    """
    if not message or not message.strip():
        return "Please enter a vulnerability description.", ""

    if selected_model == "BERT":
        full_text = get_backend_message_bert(message, "bert")
    elif selected_model == "secBERT":
        full_text = get_backend_message_bert(message, "secbert")
    else:
        full_text = get_backend_message_bert(message, "securebert")

    # Keep your top-5 extraction for later graphs
    get_top_responses(full_text)

    # TEMP: split into two tabs
    list_text, summary_text = split_into_list_and_summary(full_text)

    # TEMP: summarizer dropdown hook (currently passthrough)
    summary_text = summarize_query(summary_text, summarizer_engine)

    return summary_text, list_text


def clear_all():
    return "", "", ""  # msg, summary_box, list_box


# --------------------------
# Gradio interface
# --------------------------
with gr.Blocks() as demo:
    gr.Markdown("## CWE and ATT&CK Semantic Search")

    with gr.Row():
        with gr.Column(scale=1, min_width=500):
            msg = gr.Textbox(label="Vulnerability Description", lines=4)

            with gr.Row():
                model_selector = gr.Dropdown(
                    choices=["BERT", "secBERT", "secureBERT"],
                    value="BERT",
                    label="Embedding Model",
                )
                summarizer_selector = gr.Dropdown(
                    choices=[ "GPT-OSS", "Llama"],
                    value="GPT-OSS",
                    label="Summarization Engine",
                )

            with gr.Row():
                btn = gr.Button("Submit")
                clear = gr.Button("Clear")

    with gr.Tabs():
        with gr.Tab("Summary"):
            summary_box = gr.Textbox(label="Summary Output", lines=14)
        with gr.Tab("List / Full Results"):
            list_box = gr.Textbox(label="List / Raw Output", lines=26)

    # Wire actions
    btn.click(handle_query, inputs=[msg, model_selector, summarizer_selector], outputs=[summary_box, list_box])
    msg.submit(handle_query, inputs=[msg, model_selector, summarizer_selector], outputs=[summary_box, list_box])

    clear.click(clear_all, outputs=[msg, summary_box, list_box])

print("Launching Gradio UI...")
demo.launch(share=True)
