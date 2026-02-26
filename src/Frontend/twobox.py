import requests
import gradio as gr
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
import os
# URL for Flask backend URL
FLASK_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5002")
# Globals used by graph functions (kept for your later graph tabs)
TOP_5_CWE = []
TOP_5_ATTACKS = []






def get_backend_message_bert(message: str, mdl: str,engine: str) -> str:
    bot_message = "Error: Attempt failed"
    try:
        if mdl == "BGE":
            mdl = "BAAI"
        response = requests.post(f"{FLASK_BACKEND_URL}/search?model={mdl}", json={"query": message}, timeout=300)
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


def get_summary(query: str, message: str, engine: str) -> str:
    bot_message = "Error: Attempt failed"
    try:
        response = requests.post(f"{FLASK_BACKEND_URL}/summary?summarizer={engine}", json={"query": query, "message": message}, timeout=120)
        if response.status_code == 200:
            data = response.json()
            summary = data.get("Summary","")
            
    except Exception as e:
        summary = f"Error: Couldn't connect to backend - {e}"
    return summary


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

    full_text = get_backend_message_bert(message, selected_model,summarizer_engine)
    print(full_text,flush=True)
    # Keep your top-5 extraction for later graphs
    get_top_responses(full_text)


    return full_text


def handle_summary(message: str, cwe_lists: str, summarizer_engine: str):
    if not message or not message.strip():
        return "Please enter a vulnerability description.", ""

    full_text = get_summary(message, cwe_lists, summarizer_engine)
    print(full_text,flush=True)
    # Keep your top-5 extraction for later graphs
    get_top_responses(full_text)


    return full_text



def clear_all():
    return "", "", ""  # msg, summary_box, list_box

# --------------------------
# Gradio interface
# --------------------------
with gr.Blocks() as demo:
    gr.Markdown("## CWE and ATT&CK Semantic Search")

    with gr.Row():
        with gr.Column(scale=1, min_width=500):
            msg = gr.Textbox(label="Text Description", lines=4)

            with gr.Row():
                model_selector = gr.Dropdown(
                    choices=["BERT", "GPT-OSS", "BGE","E5","LaBSE"],
                    value="BERT",
                    label="Embedding Model",
                )
                summarizer_selector = gr.Dropdown(
                    choices=["None", "GPT-OSS", "LLAMA3.1"],
                    value="None",
                    label="Summarization Engine",
                )

            with gr.Row():
                btn = gr.Button("Submit")
                sum = gr.Button("Summarize")

    # ✅ Side-by-side outputs
    with gr.Row():
        with gr.Column(scale=1):
            list_box = gr.Textbox(label="Relevant CWEs and ATT&CK Techniques", lines=22)
        with gr.Column(scale=1):
            summary_box = gr.Textbox(label="Summary Output", lines=22)
       

    # Wire actions
    btn.click(handle_query, inputs=[msg, model_selector, summarizer_selector], outputs=[ list_box])
    sum.click(handle_summary, inputs=[msg, list_box, summarizer_selector], outputs=[ summary_box])

    msg.submit(handle_query, inputs=[msg, model_selector, summarizer_selector], outputs=[ list_box])

    # clear.click(clear_all, outputs=[msg, summary_box, list_box])

print("Launching Gradio UI...",flush=True)
demo.launch(server_name="0.0.0.0", server_port=7860)
