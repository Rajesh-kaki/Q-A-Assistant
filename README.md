# Financial Doc Q&A Assistant

Upload a PDF or Excel file and ask questions. Runs fully local using Ollama.

## Setup
1) Create env (optional)
   conda create -n finrag python=3.12 -y
   conda activate finrag

2) Install deps
   pip install -r requirements.txt

3) Pull local models (one time)
   ollama pull nomic-embed-text
   ollama pull llama3.2:3b

## Run
streamlit run app.py
if PATH warnings appear:
python -m streamlit run app.py

## Use
- Upload a PDF/XLSX in the sidebar.
- Click “Build / Load Index”.
- Ask a question (e.g., “What is the Pre-tax Profit in 2023?”).
- Expand “Sources” to see supporting text.

## Notes
- Requires Ollama running at http://localhost:11434
- Excel lock files starting with `~$` are ignored.
- To reset the vector DB, delete the `chroma_db/` folder.

- <img width="1914" height="1006" alt="Screenshot 2025-09-18 014211" src="https://github.com/user-attachments/assets/1c1e445e-d59d-42a4-a195-ff342cb96a5e" />

