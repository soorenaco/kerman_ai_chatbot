![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-00A3E0?style=for-the-badge)
![LLM](https://img.shields.io/badge/LLM-Llama%203.3-FF6F00?style=for-the-badge)

**Intelligent RAG-based chatbot for discovering investment opportunities in Kerman Province**


---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 About

**Kerman Investment Advisory Chatbot** is an intelligent RAG (Retrieval-Augmented Generation) system designed to introduce and recommend investment opportunities in Kerman Province.

Users can ask questions in **Persian or English**, and the system retrieves the most relevant projects using semantic search, then generates accurate, context-aware answers with the help of a powerful LLM.

---

## ✨ Features

- ✅ Semantic search across investment projects using multilingual embeddings
- ✅ Full support for **Persian** and **English**
- ✅ Simple and clean web interface
- ✅ Integration with powerful LLMs via OpenRouter (Llama 3.3 70B)
- ✅ Fast vector search using **FAISS**
- ✅ Rich project data including financial analysis, IRR, payback period, risks, and more

---

## 🛠 Tech Stack

| Technology | Description |
|------------|-------------|
| **Backend** | FastAPI + Python |
| **Embedding** | `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` |
| **Vector Search** | FAISS |
| **LLM** | Llama 3.3 70B (via OpenRouter) |
| **Frontend** | HTML + JavaScript |

---

## 📁 Project Structure

```text
kerman_ai_chatbot/
├── app.py                      # Main API and chatbot logic
├── dataset_v11.json            # Investment projects database
├── projects.index              # FAISS vector index
├── projects_metadata.pkl       # Project metadata
├── Index.html                  # Main web page
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ✅ Prerequisites

- Python 3.10 or higher
- OpenRouter API Key
- pip package manager

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/soorenaco/kerman_ai_chatbot.git
cd kerman_ai_chatbot
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# or
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## 💻 Usage

### Run the server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser and go to:

```text
http://localhost:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a question and receive an AI-generated answer |
| GET | `/` | Serve the main web interface |

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

Made with ❤️ Mohammad Yasin Baloochi

</div>
