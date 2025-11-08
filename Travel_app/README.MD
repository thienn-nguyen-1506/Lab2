✈️ AI Travel Itinerary Generator
This app uses a Streamlit frontend (local) to call a FastAPI/Ollama backend (on Colab).

⚙️ How to Run
1. Backend (Google Colab)
Open Backend.ipynb in Google Colab.

Set Runtime to T4 GPU (Runtime -> Change runtime type).

Run Cell 1 (Install) and Cell 2 (Start Servers & Pull Model). This may take a few minutes.

Run Cell 3 (Xterm).

In the Xterm terminal window that appears, paste and run:

Bash

ssh -p 443 -R0:localhost:8000 qr@a.pinggy.io
Copy the public Pinggy URL (e.g., http://name.a.pinggy.link).

2. Frontend (Local Machine)
Install dependencies:

Bash

pip install -r requirements.txt
Open app.py in an editor.

Find LLM_SERVER_URL and paste your Pinggy URL (keep the /generate_itinerary part):

Python

LLM_SERVER_URL = "http://[YOUR-PINGGY-URL-HERE]/generate_itinerary"
Run the app:

Bash

streamlit run app.py
🔑 Login
Username: 24127546

Password: hihihi