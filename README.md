# 🛒 FP-Growth Product Recommender System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit">
  <img src="https://img.shields.io/badge/Machine%20Learning-FP--Growth-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Data%20Mining-Association%20Rules-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Dataset-UCI%20Online%20Retail-yellow?style=for-the-badge">
</p>

<p align="center">
  <b>🚀 Intelligent Product Recommendation System using FP-Growth Algorithm</b><br>
  <i>From transaction data → to real-time recommendations</i>
</p>

---

## 📌 Overview

This project implements a **product recommendation system** based on:

- 🧠 **FP-Growth algorithm** (Frequent Pattern Mining)
- 🔗 **Association Rules**
- 🛒 **Basket-based recommendation logic**

It analyzes e-commerce transaction data to suggest **relevant complementary products** in real time.

---

## 🎯 Key Features

✨ **High-performance pattern mining**
- FP-Growth (faster than Apriori)
- No candidate generation

📊 **Association Rules**
- Support
- Confidence
- Lift

💡 **Smart Recommendations**
- Based on user's shopping basket
- Ranked by relevance

🖥️ **Dual Interface**
- CLI (Terminal)
- Web App (Streamlit)

💾 **Model Persistence**
- Save & reload trained models
- No retraining needed

---

## 🧱 Project Architecture

```bash
.
fpgrowth-recommender/
│
├── 📁 data/                     # Dataset (non versionné idéalement)
│   └── online_retail_II.xlsx
│
├── 📁 models/                   # Modèles sauvegardés
│   ├── fpgrowth.pkl
│   └── rules.pkl
│
├── 📁 src/                      # Code source principal
│   ├── data_preprocessing.py        # Nettoyage & transformation
│   ├── model.py                # FP-Growth + règles
│   └── recommender.py          # Logique de recommandation
│
├── 📄 app.py                    # Application Streamlit (UI)
├── 📄 main.py                   # Pipeline CLI
├── 📄 fpgrowth_recommender.ipynb # Notebook (exploration / tests)
│
├── 📄 requirements.txt          # Dépendances Python
├── 📄 README.md                 # Documentation du projet
├── 📄 .gitignore                # Fichiers ignorés Git
```
## ⚙️ Installation

### 1️⃣ Clone repository
```bash
    git clone https://github.com/your-username/fpgrowth-recommender.git
    cd fpgrowth-recommender
```
### 2️⃣ Create virtual environment
```bash
    python -m venv venv
    # Activate
    source venv/bin/activate        # macOS/Linux
    venv\Scripts\activate           # Windows
```
### 3️⃣ Install dependencies
```bash
  pip install -r requirements.txt
```
 
## Dataset
**📊 Source: UCI Machine Learning Repository**
**📦 File: Online Retail.xlsx**
**📈 Size: ~541k transactions**

```bash
    data/
└── online_retail_II.xlsx
```

## 🚀 Usage
### 🖥️ CLI Mode
--- 
▶️ **Train + Demo**
```bash
    python main.py --data data/online_retail_II.xlsx
```
🎯 **Interactive Mode**
```bash
    python main.py --data data/online_retail_II.xlsx --interactive
```
💾 **Load Saved Model**
```bash
    python main.py --load_rules models/rules.pkl --interactive
```
🌐 **Web App (Streamlit)**
```bash
    streamlit run app.py
```
💻 **Features**
    🛒 Multi-product selection
    🎚️ Dynamic sliders (confidence, lift)
    📊 Real-time recommendations
    📋 Full rule exploration

## 🧠 How It Works

### 1️⃣ Data Cleaning
      Remove cancelled invoices
      Remove negative quantities
      Drop missing values
      Remove duplicates
### 2️⃣ Basket Matrix
  **Binary encoding:**
    
      ```text
          Invoice × Product → {0,1}
      ```
### 3️⃣ FP-Growth
        - Extract frequent itemsets efficiently
       
### 4️⃣ Association Rules
        - Generate rules using confidence
        - Filter using lift
### 5️⃣ Recommendation Engine
      ```text
        If (antecedents ⊆ basket) → recommend consequents
      ```
## 📊 Example
### 🛒 Input Basket

**CHOCOLATE THIS WAY METAL SIGN**
**CHOCOLATE HOT WATER BOTTLE**
**COFFEE MUG CAT + BIRD DESIGN**

### 💡 Output Recommendations
```bash
    | Product                           | Confidence | Lift | Support |
    | --------------------------------- | ---------- | ---- | ------- |
    | HAND OVER THE CHOCOLATE SIGN      | 72%        | 3.45 | 0.023   |
    | HOT WATER BOTTLE TEA AND SYMPATHY | 68%        | 3.12 | 0.019   |
```
## ⚙️ Recommended Parameters
```bash
    | Parameter        | Value | Description          |
    | ---------------- | ----- | -------------------- |
    | `min_support`    | 0.03  | Frequency threshold  |
    | `min_confidence` | 0.5   | Rule reliability     |
    | `min_lift`       | 1.0   | Positive correlation |
```

## 🔧 Troubleshooting
```bash
    | Issue              | Fix                               |
    | ------------------ | --------------------------------- |
    | Module not found   | `pip install -r requirements.txt` |
    | Dataset not found  | Check file path                   |
    | No rules generated | Lower thresholds                  |
    | Streamlit error    | Run from root directory           |
```
## 📚 References
    - FP-Growth – MLxtend Documentation
    - UCI Online Retail Dataset
    - Agrawal & Srikant (1994)

## 🏆 Project Highlights
    ✔ Real-world dataset
    ✔ Scalable algorithm (FP-Growth)
    ✔ Interactive UI
    ✔ Production-ready structure

## 👤 Author

**Youssef Benyahia**
**📧 benyahiayoussef63@gmail.com**
