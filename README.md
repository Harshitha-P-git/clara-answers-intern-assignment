# Clara Answers: Zero-Cost Automation Pipeline

## 🎥 Video Demonstration
**Watch the submission video here: [CLICK HERE TO PASTE YOUR LOOM LINK]**

This project automates the creation and update of Retell AI Voice Agent configurations from Demo and Onboarding call transcripts.

## Architecture

1.  **Ingestion**: Transcripts are placed in a local folder.
2.  **Pipeline A (Demo -> v1)**: Extracts initial business rules into a structured **Account Memo JSON** and generates a **Retell Agent Draft Spec**.
3.  **Pipeline B (Onboarding -> v2)**: Merges onboarding data with v1 assets, overrides outdated info, and generates a **v2 Memo**, **v2 Agent Spec**, and a **Changelog**.
4.  **Orchestration**: Managed via **n8n** (self-hosted/local) using command execution nodes.
5.  **Storage**: Versioned JSON files in the `/outputs` directory.

## Getting Started

### Prerequisites
- Python 3.x
- n8n (local or desktop version)

### Local Setup
1.  Clone the repository.
2.  Ensure you have a `scripts` folder with `pipeline_a.py` and `pipeline_b.py`.

### Running the Pipeline
To process the example "Ben's Electric" account:
```powershell
python scripts/pipeline_a.py
python scripts/pipeline_b.py
```

### n8n Setup
1.  Open n8n.
2.  Import `workflows/n8n_export.json`.
3.  Update the path parameters in the "Local File Trigger" node to match your local input directory.

## Output Structure
- `outputs/accounts/<account_id>/v1/`: Initial demo results.
- `outputs/accounts/<account_id>/v2/`: Final operational configuration and `changelog.md`.

## GitHub Deployment

To submit your assignment, you need to upload this folder to a GitHub repository:

1.  **Initialize Git**:
    ```powershell
    git init
    git add .
    git commit -m "Initial commit: Clara Answers Automation Pipeline"
    ```
2.  **Create Repository**:
    - Go to [GitHub](https://github.com/new) and create a repository named `clara-answers-intern-assignment`.
3.  **Push to GitHub**:
    ```powershell
    git remote add origin https://github.com/YOUR_USERNAME/clara-answers-intern-assignment.git
    git branch -M main
    git push -u origin main
    ```

## Dashboard & Batch Processing
- Run `python scripts/process_batch.py` to generate the full dataset (10 samples).
- Open `dashboard.html` in any browser to view a summary of the accounts and generated artifacts.

## Known Limitations
- Extraction is currently simulated for the demo. In production, this would use a zero-cost LLM API (like Groq or local Ollama).
- n8n nodes use local paths which need adjustment per machine.

## Future Improvements
- Integrate with a real task tracker API (Asana/Trello).
- Add a React-based "Diff Viewer" for better visibility of v1 vs v2.
- Implement real-time transcription using local Whisper.
