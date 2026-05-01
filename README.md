# 🎓 Fake Certificate & Internship Detection System

An AI + Blockchain powered platform that detects **fake certificates** and **fraudulent internship opportunities** using Machine Learning, NLP, Computer Vision, and Blockchain security.

---

# 🚨 Problem Statement

In today’s digital world, AI is being misused to:
- Generate fake certificates and degrees  
- Edit real certificates to manipulate identity  
- Create fake internship opportunities and scam students  

These frauds lead to financial loss, trust issues, and fake hiring decisions.

---

# 💡 Why We Chose This Problem

We chose this problem because it is real and widely affecting students.  
Many students around us have lost money due to fake internship scams.

Our goal is to:
- Prevent fraud  
- Protect students  
- Improve trust in digital hiring systems  

---

# 🧠 Our Solution

We built a smart verification system using:

### 🤖 AI + NLP (Natural Language Processing)
- Detects fake internship emails  
- Identifies scam patterns using text analysis  
- Uses **Gemini API** for advanced language understanding and classification  
- Hugging Face models used for NLP preprocessing and classification  

### 👁️ Computer Vision
- OpenCV for image preprocessing  
- CNN for detecting certificate tampering  
- Tesseract OCR for extracting text from images  

### ⛓️ Blockchain Security
- Stores verified certificates securely  
- Prevents tampering or modification  
- Ensures transparency and trust  

### 🔐 NFT + MetaMask Integration
- Certificates can be minted as NFTs  
- MetaMask login enables secure blockchain authentication  
- Provides global ownership verification  

---

# 📊 Dataset Used

### 📧 Internship Dataset
- Kaggle datasets (email scam datasets)  
- Hugging Face datasets for NLP training  
- Generated real + fake internship emails  
- Cleaned and filtered data for training  

### 🎓 Certificate Dataset
- Real certificates collected  
- Fake/edited certificates generated manually  
- Used for training AI models  

👉 More dataset = better accuracy

---

# ⚙️ Tech Stack

## ⛓️ Blockchain

- **Ganache**
  - Local blockchain simulation tool  
  - Runs on HTTP server  
  - Used for testing smart contracts  

- **Remix IDE**
  - Smart contract development tool  
  - Used to write and deploy Solidity contracts  

- **MetaMask**
  - Blockchain wallet for authentication  
  - Used for login and NFT verification  

- **NFT Integration**
  - Certificates minted as NFTs  
  - Ensures ownership and traceability

---

## 🤖 Artificial Intelligence

- **TensorFlow**
  - Deep learning framework for training models  

- **CNN (Convolutional Neural Network)**
  - Detects fake or edited certificates  

- **NLP (Natural Language Processing)**
  - Detects scam internship emails  
  - Works with Gemini API + Hugging Face models  

- **Gemini API**
  - Used for advanced AI-based text understanding  
  - Helps classify internship emails as real or fake  

- **Hugging Face**
  - Used for pre-trained NLP models  
  - Improves text classification accuracy  

- **Tesseract OCR**
  - Extracts text from images  

- **OpenCV**
  - Image preprocessing (noise removal, resizing, enhancement)  

---

## 🌐 Backend & Web Frameworks

- **Flask (Python)**
  - Lightweight backend framework  
  - Handles AI model integration and API routing  

- **FastAPI (Python)**
  - High-performance API framework  
  - Used for fast prediction endpoints  

👉 Flask + FastAPI together provide both flexibility and speed  

---

# ✨ Features

- 🔍 Fake certificate detection  
- 📧 Internship scam detection using NLP  
- 👁️ Image forgery detection using OpenCV + CNN  
- 🤖 AI-based classification using Gemini API  
- 🧠 Hugging Face NLP integration  
- ⛓️ Blockchain-based secure storage  
- 🔐 MetaMask login authentication  
- 🪙 NFT-based certificate ownership  
- ⚡ Real-time prediction system  
- 🛠️ Debugging support feature  

---

# 🛠️ How It Works

1. User uploads certificate or internship email  
2. OpenCV preprocesses image (if any)  
3. Tesseract extracts text  
4. NLP (Gemini + Hugging Face) analyzes email  
5. CNN + TensorFlow analyze certificate authenticity  
6. Flask/FastAPI handles API requests  
7. Blockchain (Ganache + Remix + MetaMask) stores verified data  
8. Optional NFT minting for certificates  

---

# 🔮 Future Scope
- Integration with internship portals
- Integration with job portals
- Expanding datasets for higher accuracy
- Mobile application development
- Partnerships with universities & companies
- Global certificate verification system
- Continuous improvement using real-world data
- More dataset → higher AI accuracy



# 🌐 Website Link

👉 https://your-website-link-here.com  

---

# 🚀 How to Use

### 1. Clone Repository
```bash
git clone https://github.com/your-username/project-name.git

2. Install Dependencies
pip install -r requirements.txt


3. Run Backend (Flask or FastAPI)
python app.py
or
uvicorn main:app --reload

4. Open in Browser
http://127.0.0.1:5000
```

---

# 🌐 Chrome Extension (Quick Internship Checker)

Step 1:
Download extension folder from repository -> [email-scam-extension.zip](https://github.com/user-attachments/files/27266691/email-scam-extension.zip)


Step 3:
Enable Developer Mode

Step 4:
Click Load Unpacked

Step 5:
Select extension folder

Step 6:
Extension is now active 


---

