<div align="center">

  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&pause=1000&color=FF3B30&center=true&vCenter=true&width=800&lines=Detecting+Predatory+Clauses+Instantly...;AI-Powered+Terms+of+Service+Scanner...;Protecting+Your+Digital+Rights...;Risk+Intel+Extension+" alt="Typing SVG" />

  <br><br>

  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Magnifying%20Glass%20Tilted%20Left.png" alt="Magnifying Glass" width="80" />
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Symbols/Warning.png" alt="Warning" width="80" />
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Shield.png" alt="Shield" width="80" />

  <h1>🛡️ Risk Intel - TOS Dark Pattern Detector</h1>

  <p>
    <b>Never blindly agree to harmful Terms of Service again!</b><br>
    Risk Intel is an AI-powered Chrome Extension designed to scan long, confusing legal documents in real time,<br> 
    highlighting predatory clauses exactly where they live on the web page.
  </p>

</div>

---

## 📖 Table of Contents
1. [What We Have Done](#-what-we-have-done)
2. [Technologies Used](#-technologies-used)
3. [File Structure](#-file-structure)
4. [Problems Faced & How We Resolved Them](#-problems-faced--how-we-resolved-them)
5. [The Unique Thing We've Done](#-the-unique-thing-weve-done)
6. [Drawbacks](#-drawbacks)
7. [Installation & Setup](#-installation--setup)
   - [Download CRX File](#-install-the-extension-crx-file)
8. [Architecture Mind Map](#-architecture-mind-map)
9. [Extension Workflow (Infographic)](#-extension-workflow-infographic)
10. [Outro](#-outro)

---

## 🚀 What We Have Done

We successfully researched, trained, and deployed an end-to-end Machine Learning pipeline connected to a dynamic browser extension. 
By combining Python data science libraries directly with standard web development tools, we've bridged the gap between raw natural language processing and an interactive user experience.

1. **The Brain (`app.py`)**: A local FastAPI backend that loads a pre-trained scikit-learn model (`tos_model.pkl`) to classify incoming text as either safe or predatory.
2. **The Eyes (`content.js`)**: A Chrome extension content script that automatically extracts paragraphs (`<p>`) and list items (`<li>`) from any web page you visit.
3. **The Voice (DOM Manipulation)**: Dynamic in-browser highlighting. If a clause is flagged as predatory (scoring above our 80% confidence threshold), the extension visually alerts the user by injecting a red background (`#ffe6e6`) and a robust solid red border to that specific HTML element.

---

## 🛠️ Technologies Used

Building an application of this scale required a diverse technology stack spanning from data compilation to frontend visualization:

- **Frontend & Browser**
  - HTML5 & CSS3 (For the `popup.html` interface)
  - Vanilla JavaScript (ES6+ for `content.js` DOM extraction and REST APIs)
  - Google Chrome Extension Manifest V3 (`manifest.json`)
- **Backend Infrastructure**
  - **Python 3.10+**: The core language powering the logic.
  - **FastAPI**: Used for ultra-fast, asynchronous API endpoint generation.
  - **Uvicorn**: An ASGI web server implementation for Python.
- **Machine Learning & Data Science**
  - **Scikit-Learn**: Used heavily in `train_model.py` for TF-IDF vectorization and classification.
  - **Joblib**: Used for exporting and importing the trained `tos_model.pkl` weights.
  - **Pandas**: Crucial for structuring and cleaning the original `tos_data.csv` corpus.
  - **Jupyter Notebooks**: `main.ipynb` act as the initial research sandbox.

---

## 📂 File Structure

Understanding where everything is located is critical for future maintenance and open-source contributions. Here is the current directory layout:

```text
📦 project-72-rag-extension
 ┣ 📂 tos_extension                 # The Chrome Extension Source Code
 ┃ ┣ 📜 content.js                  # Scans page, manipulates DOM, requests API
 ┃ ┣ 📜 manifest.json               # V3 Manifest, permissions (activeTab, scripting)
 ┃ ┣ 📜 popup.html                  # HTML for the popup when you click the extension logo
 ┃ ┗ 📜 popup.js                    # Logic directing the popup UI
 ┣ 📂 tos_env                       # Virtual Environment for Python
 ┃ ┗ 📜 ...                         # Standard venv libraries
 ┣ 📜 app.py                        # FastAPI Backend Application Server
 ┣ 📜 main.ipynb                    # Jupyter Sandbox for Data Exploration
 ┣ 📜 predatory_clause_model.pkl    # Serialized ML Model (Alternative/Backup)
 ┣ 📜 requirements.txt              # Pip dependencies (fastapi, scikit-learn, joblib)
 ┣ 📜 test.html                     # Local test page containing dummy TOS clauses
 ┣ 📜 tos_data.csv                  # The raw corpus mapping texts to 0 or 1
 ┣ 📜 tos_extension.crx             # The Packaged Chrome Extension (INSTALLABLE!)
 ┣ 📜 tos_extension.pem             # Private Key generated during Chrome Packing
 ┣ 📜 tos_model.pkl                 # The Primary Serialized ML Model used in Production
 ┣ 📜 train_model.py                # Script to convert tos_data.csv into tos_model.pkl
 ┗ 📜 training_output.txt           # Logs regarding the precision/recall of the model
```

---

## 🤯 Problems Faced & How We Resolved Them

Developing a seamless bridge between a user's local browser and an ML server came with significant technical hurdles:

| Problem 🚨 | Our Resolution ✅ |
| :--- | :--- |
| **Too Many False Positives** <br> *Initially, the ML model was acting too aggressively, flagging perfectly safe sentences like "Welcome to our website" as predatory, which ruined the browsing experience.* | **High-Precision Thresholding** <br> We implemented a strict `CONFIDENCE_THRESHOLD = 0.80` manually inside our FastAPI backend (`app.py`). Rather than trusting a standard 50% split, the model now **only** flags sentences where it is >80% confident it exhibits a predatory pattern. |
| **CORS Blocked by Browser** <br> *Because `content.js` runs in the context of random websites (like `google.com`), Chrome blocks HTTP requests to `localhost:8000` for security (Cross-Origin Resource Sharing).* | **Backend & Manifest Updates** <br> We resolved this on two fronts. First, we added `CORSMiddleware` in `app.py` allowing `["*"]` origins. Secondly, we explicitly added `"http://localhost:8000/*"` to the `host_permissions` array in `manifest.json`. |
| **Inefficient Scanning & Server Crashes** <br> *When opening massive legal documents, the extension was sending hundreds of API requests for empty formatting `<div>`s, single characters, and 3-word sentences. It overloaded the network loop.* | **Dual-Layer Filtering** <br> We created a dual-check system. On the frontend, `content.js` uses string manipulation (`trim().length`) to drop anything under 30 characters. On the backend, `app.py` rejects texts composed of fewer than 4 words, saving processing power and reducing lag. |
| **Matching Data Formats** <br> *The model was failing to recognize text that contained weird punctuation or capitalization the user saw on the screen.* | **Regex Standardization** <br> We ensured the text cleaning phase (`clean_text` function) in the production backend `app.py` matches the preprocessing in `train_model.py` identically down to the regular expressions, guaranteeing model accuracy translates perfectly. |

---
