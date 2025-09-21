# 🌾 Arid Buddy – AI-Powered Chatbot for Students

**Arid Buddy** is a desktop-based **AI chatbot** built to assist students of **PMAS Arid Agriculture University, Rawalpindi** with academic and administrative queries.  

It uses a **Discriminative Machine Learning Model** (classification-based) to understand user queries and provide context-relevant responses. The project integrates a user-friendly desktop UI, a trained ML model, and an intent-response mapping system.

---

## 🚀 Features
- 💬 **Interactive Chat Interface** – simple, desktop-based chatbot UI.  
- 🎓 **Student Support** – answers academic, campus, and general student-related questions.  
- 🤖 **Discriminative ML Model** – classifies queries into intents and returns the most suitable response.  
- 📂 **Pre-trained Model** – trained on custom intent dataset (`intents.json`).  
- 🔄 **Extendable** – easily add new intents, responses, or retrain the model.  

---

## 🛠️ Tech Stack
- **GUI Framework:** Tkinter / CustomTkinter  
- **ML Libraries:** scikit-learn, TensorFlow/Keras (for model training & inference)  
- **Language:** Python 3  
- **Dataset:** Custom `intents.json` for student queries  

---


---

## ⚡ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Stranger-S8/Arid-Buddy-A-Chatbot.git
   cd Arid-Buddy-Chatbot
2.  **Create and activate virtual environment**
    python -m venv venv
    venv\Scripts\activate     # On Windows
    source venv/bin/activate  # On Mac/Linux
3. **Install dependencies**
    pip install -r requirements.txt
4. **Run the chatbot**
    python main.py
