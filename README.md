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
