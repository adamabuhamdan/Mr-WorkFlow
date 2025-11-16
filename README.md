# 🚀 Startup Advisor AI  
**Multi-Modal, Stage-Aware AI Mentor for Founders**

Startup Advisor AI is an intelligent, multi-modal advisory system that guides founders across the entire startup lifecycle.  
It combines **RAG (Retrieval-Augmented Generation)**, **Gemini Vision**, and **PDF intelligence** to deliver accurate, contextual, and actionable startup guidance.

This project was built for the Google Hackathon and showcases production-level architecture, clean multi-model integration, and real startup knowledge.

---

## 🌟 Key Features

### ✅ 1. Text-Based Startup Advisory (RAG)
Ask any startup-related question such as:
- “How do I validate my MVP?”
- “How do I prepare for seed funding?”
- “How do I grow early traction?”

The system:
1. Automatically detects the relevant startup stages  
2. Retrieves context from a curated knowledge base  
3. Generates grounded, structured answers using Gemini Pro  

### 🖼️ 2. Image Analysis (Gemini Vision)
Upload any slide, pitch deck image, diagram, or UI screenshot.

The system can:
- Critique pitch deck slides  
- Suggest improvements  
- Analyze UI/UX  
- Detect weak storytelling  
- Provide investor-focused recommendations  

### 📄 3. File Analysis (PDF Intelligence)
Upload PDFs such as:
- Pitch decks  
- Business reports  
- Strategy documents  
- Research summaries  

Gemini Vision extracts content and returns:
- Slide-by-slide feedback  
- Missing elements  
- Narrative improvements  
- Investor-readiness assessment  
- Market & traction clarity  

---

## 🧠 Startup Knowledge Base (RAG Engine)

The system uses a structured dataset representing **8 startup stages**, each containing distilled principles from foundational startup literature.

### 📘 **The 8 Stages**
1. **Ideation** – Problem discovery, value creation, opportunity spotting  
2. **Validation** – MVP building, user testing, rapid experiments  
3. **Product Building** – UX, habit formation, product psychology  
4. **Growth & Traction** – Channels, acquisition, crossing the chasm  
5. **Funding** – Angel investing, VC negotiation, term sheets  
6. **Team & Leadership** – Culture, leadership, roles, founder challenges  
7. **Scaling** – Hypergrowth, OKRs, team expansion  
8. **Strategic Maturity** – Long-term advantage, strategy execution  

The knowledge base is stored in **Qdrant Cloud**, using:
- Sentence Transformers embeddings  
- Rich metadata (stage, book, topic, tags)  
- High-performance semantic search  

---

## 🏗️ System Architecture

### **Frontend**
- HTML + CSS + JavaScript  
- Clean, modern 3-tab interface:
  - Text Chat (RAG)
  - Image Analysis
  - File Analysis
- Multi-modal inputs (text, image, PDF)
- Async fetch API  
- Badged stage detection  
- Zero dependencies, deployable on any static hosting  

### **Backend**
- FastAPI  
- Python 3.11  
- Gemini Pro & Gemini Vision  
- Qdrant Cloud Vector Database  
- LangChain 0.3.x  
- Dockerized microservice  
- Stage detection + multi-stage retrieval  
- Markdown ingestion pipeline  

---

## 🐳 Docker Deployment

### Build:
```bash
docker build -t startup-advisor .
