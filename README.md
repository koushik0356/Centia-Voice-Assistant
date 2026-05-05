# 🎙️ Centia – AI Voice Assistant for Centurion University

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat&logo=flask&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6B6B?style=flat)
![LangChain](https://img.shields.io/badge/LangChain-Text_Splitting-1E90FF?style=flat)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-BAAI%2Fbge_small-green?style=flat)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM_API-FF6B9D?style=flat&logo=openai)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_SDK-00A67E?style=flat&logo=openai)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript&logoColor=black)

**Centia** is an intelligent, conversational voice assistant designed to provide students, faculty, and visitors with instant, accurate information about Centurion University of Technology and Management (CUTM-AP). Powered by advanced RAG (Retrieval-Augmented Generation) technology and a custom LLM pipeline, Centia delivers natural, human-like responses through a modern web interface.

![Centia Dashboard](static/logo.png)


**Backend**: Python 3.8+, Flask  
**LLM & API**: OpenRouter (Arcee AI), OpenAI SDK  
**Vector Database**: ChromaDB  
**Embeddings**: Sentence Transformers (`BAAI/bge-small-en-v1.5`)  
**Text Processing**: LangChain Text Splitters  
**Frontend**: HTML5, CSS3, Vanilla JavaScript  
**Environment**: Python-dotenv

---

## ✨ Key Features

- **🎤 Voice-Optimized Responses**: All outputs are formatted for natural speech synthesis—no markdown, lists, or special characters
- **🧠 RAG-Powered Intelligence**: Hybrid retrieval system combining vector similarity search with intelligent query optimization
- **📚 Comprehensive Knowledge Base**: Indexed academic programs, courses, research initiatives, and university facilities
- **💬 Conversational Context**: Maintains conversation history for pronoun resolution and context-aware responses
- **⚡ Fast & Scalable**: Sub-second response times using ChromaDB vector database and Arcee AI's optimized LLM
- **🎯 Smart Intent Routing**: Automatically detects broad queries vs. specific ones, serving comprehensive overviews when needed
- **🌐 Modern Web Interface**: Clean, accessible UI built with Flask and vanilla JavaScript

---

## 🏗️ Architecture

### System Overview

```
User Query (Web UI)
        ↓
   [Flask App]
        ↓
   Query Optimizer (Expands acronyms, resolves pronouns)
        ↓
   RAG Pipeline (Intent Detection + Vector Retrieval)
        ├─→ Broad Query? → Load Master Report
        └─→ Specific? → ChromaDB Similarity Search
        ↓
   LLM Generation (Arcee AI / OpenRouter)
        ↓
   Conversational Response (Stored in History)
        ↓
   User (Browser UI)
```

### Component Breakdown

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **Frontend** | User interface for chat interaction | Flask + HTML/CSS/JavaScript |
| **Query Optimizer** | Expands acronyms (CSE→Computer Science & Engineering) and resolves pronouns | OpenAI API (via OpenRouter) |
| **RAG Pipeline** | Retrieves relevant university documents using vector similarity | ChromaDB + Sentence Transformers |
| **Embedding Model** | Converts text to semantic vectors | `BAAI/bge-small-en-v1.5` |
| **LLM** | Generates conversational responses | `arcee-ai/trinity-large-preview:free` (OpenRouter) |
| **Vector DB** | Stores indexed document chunks with metadata | ChromaDB (Persistent) |
| **Index Builder** | Pre-processes markdown files and builds the vector database | `build_index.py` |

---

## 📦 Tech Stack

- **Backend**: Python 3.8+, Flask
- **LLM & API**: OpenRouter (Arcee AI), OpenAI SDK
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (`BAAI/bge-small-en-v1.5`)
- **Text Processing**: LangChain Text Splitters
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Environment**: Python-dotenv for configuration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An OpenRouter API key ([Get one free here](https://openrouter.ai))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Centia-Voice-Assistant.git
   cd Centia-Voice-Assistant
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. **Build the knowledge base index**:
   ```bash
   python build_index.py
   ```
   This processes all markdown files in the `Data/` folder and creates the ChromaDB vector index.

6. **Run the application**:
   ```bash
   python app.py
   ```
   The app will start at `http://localhost:5000`

---

## 📖 Usage

### For Users

1. Open the web interface at `http://localhost:5000`
2. Ask natural questions about the university:
   - "What programs do you offer?"
   - "Tell me about the Computer Science program"
   - "What are the research initiatives?"
   - "How can I contact the CSE department?"

3. Responses are displayed in the chat window and optimized for voice synthesis

### Example Queries

| Query Type | Example | Response |
|-----------|---------|----------|
| Broad Overview | "What programs are available?" | Returns master report covering all programs |
| Specific Program | "Tell me about ECE" | Retrieves ECE-specific documentation |
| Acronym Expansion | "What is CSE?" | Optimizer expands to "Computer Science & Engineering" |
| Contextual | "What courses do they offer?" (after program mention) | Retrieves courses from previously mentioned program |

---

## 📁 Project Structure

```
Centia-Voice-Assistant/
├── app.py                              # Flask application & chat endpoint
├── config.py                           # Configuration, API keys, system prompts
├── rag_pipeline.py                     # RAG logic, context retrieval, query optimization
├── build_index.py                      # Markdown ingestion & ChromaDB indexing
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (not in repo)
├── Data/                              # Knowledge base documents
│   ├── CUTMAP_FINAL_COMPLETE_REPORT.md    # Master report for broad queries
│   ├── Centurion_Prod_Labs.md
│   ├── CUTM_Research_Data.md
│   ├── CUTM_Skill_Courses.md
│   └── Programs/                       # Individual program documents
│       ├── CUTM_B_Tech_CSE_AIML_Report.md
│       ├── CUTM_BTech_CSE_Report.md
│       ├── CUTM_CSE_DataScience.md
│       └── ... (more programs)
├── templates/
│   └── index.html                      # Chat interface UI
├── static/
│   └── logo.png                        # University logo
├── chroma_db/                          # Vector database (created by build_index.py)
└── README.md                           # This file
```

---

## ⚙️ Configuration

### Key Settings in `config.py`

```python
# LLM Configuration
API_KEY = "your_openrouter_api_key"
BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "arcee-ai/trinity-large-preview:free"

# RAG Configuration
DB_FOLDER = "./chroma_db"              # Where vector DB is stored
COLLECTION_NAME = "university_data"    # ChromaDB collection name
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
DATA_FOLDER = "Data"                   # Source documents
TOP_K_DOCS = 10                        # Documents to retrieve per query

# Intent Keywords
BROAD_QUERY_KEYWORDS = [
    "all programs", "what programs", "programs offered", ...
]
```

### Customization Tips

- **Change LLM Model**: Update `LLM_MODEL` in `config.py` (ensure it's available via OpenRouter)
- **Adjust Response Temperature**: Modify the `temperature` parameter in `app.py`'s chat endpoint (0.0 = deterministic, 1.0 = creative)
- **Add More Documents**: Place markdown files in `Data/` and run `build_index.py` again
- **Tune Retrieval**: Adjust `TOP_K_DOCS` to retrieve more/fewer context documents

---

## 🔄 Workflow: How Centia Works

### Step 1: Index Building (One-time Setup)
```
Data/ (Markdown files)
    ↓
MarkdownHeaderTextSplitter (chunks by headers)
    ↓
Sentence Transformer Embeddings
    ↓
ChromaDB Storage (with metadata)
```

### Step 2: Query Processing (Real-time)
```
User Input
    ↓
Query Optimizer (LLM expansion: "CSE" → "Computer Science & Engineering")
    ↓
Intent Detection (Is it a broad query?)
    ├─ YES → Load CUTMAP_FINAL_COMPLETE_REPORT.md
    └─ NO  → Vector similarity search in ChromaDB
    ↓
Context Injection (Append to message)
    ↓
LLM Generation (Arcee AI produces conversational response)
    ↓
Response Formatting (Remove markdown, optimize for speech)
    ↓
Add to Conversation History
    ↓
Return to User
```

---

## 🛠️ Development & Maintenance

### Rebuilding the Index

If you add or modify documents in `Data/`:

```bash
python build_index.py
```

This will:
- Scan all `.md` files in `Data/` and subdirectories
- Split documents by markdown headers
- Generate embeddings
- Store in ChromaDB
- Report indexed document count

### Monitoring & Logs

- **Query Optimization**: Check console for `🔍 Original: ... | Optimized: ...`
- **Document Retrieval**: Look for `📄 Router selected X chunk(s):`
- **Errors**: Enable Flask debug mode for detailed stack traces

### Testing the RAG Pipeline

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
context = rag.retrieve_context("Tell me about CSE programs")
print(context)
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `WARNING: ChromaDB collection not found` | Run `python build_index.py` to create the index |
| `API key error` | Verify `OPENROUTER_API_KEY` is set in `.env` |
| `No documents retrieved` | Check that markdown files are in `Data/` folder and properly formatted |
| `Slow responses` | Reduce `TOP_K_DOCS` in `config.py` or upgrade the LLM model |
| `404 on /chat endpoint` | Ensure Flask is running and URL is `http://localhost:5000/chat` with POST method |
| `Markdown characters in response` | The response formatter should remove them—check that `SYSTEM_INSTRUCTION` is properly loaded |

---

## 🔐 Security Considerations

- **API Key**: Never commit `.env` file to version control—add it to `.gitignore`
- **CORS**: Frontend is served from the same origin; for cross-origin requests, configure Flask-CORS
- **Input Validation**: User inputs are passed to the LLM—consider adding input sanitization for production
- **Rate Limiting**: For public deployments, implement rate limiting on the `/chat` endpoint

---

## 📊 Performance Notes

- **Embedding Time**: ~100ms per query (Sentence Transformer)
- **Retrieval Time**: ~50ms (ChromaDB vector search)
- **LLM Generation**: ~1-3 seconds (Arcee AI via OpenRouter)
- **Total Response Time**: ~2-4 seconds

To improve performance:
- Use a faster embedding model (trade-off: accuracy)
- Deploy ChromaDB closer to the app
- Cache frequently asked questions
- Use async LLM calls for multiple queries

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and commit (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Areas for Contribution
- Adding more university documents
- Improving the UI/UX
- Optimizing the RAG pipeline
- Adding multi-language support
- Implementing voice synthesis/recognition

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 📧 Support & Contact

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact the development team at `support@centurionuniversity.ac.in`

---

## 🙏 Acknowledgments

- **Centurion University of Technology and Management (CUTM-AP)** for providing the knowledge base
- **OpenRouter** for LLM API access
- **ChromaDB** for the vector database
- **Hugging Face** for the Sentence Transformers embedding model

---

**Built with ❤️ for the Centurion University Community**
