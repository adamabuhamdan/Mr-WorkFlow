# 🚀 Mr WorkFlow AI

> **Multi-Modal, Stage-Aware AI Mentor for Founders**

Mr WorkFlow AI is a production-ready startup advisor that combines RAG, Gemini Pro, Gemini Vision, and PDF intelligence to deliver contextual, accurate, and deeply actionable guidance for founders at every stage of their journey.

Built for Google's Hackathon | Powered by Qdrant, LangChain & Gemini

---

## 🌟 Key Features

### ✅ 1. Text-Based Startup Advisory (RAG Engine)

Get expert answers to startup questions like:
- "How do I validate my MVP?"
- "How do I prepare for pre-seed funding?"
- "How do I grow early traction?"
- "How do I build a scalable team?"

**Pipeline:**
```
Stage Detection → Semantic Retrieval → Gemini Pro Generation
```

### 🖼️ 2. Image Analysis (Gemini Vision)

Upload and analyze:
- Pitch deck slides
- UI/UX screenshots
- Diagrams & flowcharts

**Get feedback on:**
- Slide critique
- UI/UX recommendations
- Narrative flow evaluation
- Investor-readiness improvements

### 📄 3. PDF Intelligence

Upload full documents (pitch decks, business plans, market analysis) for:
- Slide-by-slide interpretation
- Missing section detection
- Competitive positioning critique
- Traction & metrics evaluation
- Clarity & investor-readiness scoring

---

## 🧠 Advanced RAG Knowledge Base

The core power of Mr WorkFlow AI lies in its curated knowledge base built from:

✔️ **15+ books** on startups, scaling, growth, funding, and leadership  
✔️ **Real case studies** from: OpenAI, Stripe, Notion, Perplexity, Linear, Vercel, Midjourney (2023–2025)  
✔️ **9 years** of practical founder experience in business & sales

### 📘 The 8-Stage Knowledge Model

1. **Ideation** – Opportunity spotting, problem discovery
2. **Validation** – MVP iteration, user interviews, rapid experiments
3. **Product Building** – MVP → V1 → V2, UX, stickiness
4. **Growth & Traction** – Channels, acquisition, early distribution
5. **Funding** – Angel/VC mechanics, negotiation, term sheets
6. **Team & Leadership** – Culture, hiring, founder mindset
7. **Scaling** – Operations, growth loops, systems, OKRs
8. **Strategic Maturity** – Moats, execution, long-term advantage

Each vector includes:
- Stage classification
- Topic categorization
- Complexity level
- Actionable advice
- Real 2025 examples
- Common pitfalls to avoid

---

## 🏗️ System Architecture

### Frontend
- **Technology**: HTML, CSS, JavaScript (lightweight, no frameworks)
- **Interface**: 3-tab layout
  - Text Chat (RAG)
  - Image Analysis
  - File Analysis
- **Features**: 
  - Asynchronous fetch API
  - Stage detection display
  - Drag-and-drop uploads

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI
- **AI Models**: 
  - Gemini Pro (text generation)
  - Gemini Vision (image analysis)
- **Vector DB**: Qdrant Cloud
- **Tools**: LangChain 0.3.x
- **Embeddings**: Sentence Transformers (all-mpnet-base-v2)

### Vector Database Architecture

**Qdrant Cloud** provides:
- High-speed semantic search
- Scalable cloud storage
- Metadata filtering
- Production-grade reliability

**Stored Metadata:**
```json
{
  "stage": "Validation",
  "topic": "MVP",
  "source_book": "The Lean Startup",
  "tags": ["experiments", "early_stage"],
  "complexity": "intermediate",
  "example_year": 2025
}
```

**Retrieval Flow:**
```
User Question → Embedding → Stage Filter → Qdrant Search → Top-k Results → Gemini Pro → Answer
```

---

## 🐳 Docker Deployment

### Build
```bash
docker build -t startup-advisor .
```

### Run
```bash
docker run -p 8000:8000 startup-advisor
```

---

## ☁️ Cloud Deployment

### AWS EC2 + ECR
- Containerized backend
- NGINX reverse proxy support
- Auto-start using systemd
- Secure environment variables

---

## 🔥 Example Knowledge Vector

```yaml
advice_1:
  stage: Idea
  topic: customer_interviews
  complexity: beginner
  tags: [facts_over_opinions, customer_truth, early_stage]
  
  advice: |
    Focus every conversation on the customer's past behavior 
    instead of their opinions.
  
  why: |
    Past behavior is the only reliable predictor of real demand.
  
  example_2025: |
    When Notion interviewed enterprise teams in 2025, they asked 
    about the last six months of workflow failures instead of 
    pitching new AI features.
  
  avoid:
    - hypotheticals
    - future_promises
    - generic_opinions
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional)
- Qdrant Cloud account
- Google AI API key (Gemini)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/mrworkflow-ai.git
cd mrworkflow-ai
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export GOOGLE_API_KEY="your_gemini_api_key"
export QDRANT_URL="your_qdrant_url"
export QDRANT_API_KEY="your_qdrant_api_key"
```

4. Run the application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. Open your browser
```
http://localhost:8000
```

---

## 📚 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI |
| AI Models | Gemini Pro, Gemini Vision |
| Vector Database | Qdrant Cloud |
| Embeddings | Sentence Transformers |
| Orchestration | LangChain 0.3.x |
| Frontend | Vanilla JS, HTML, CSS |
| Containerization | Docker |
| Cloud | AWS EC2, ECR |

---

## 🎯 Use Cases

- **Pre-seed founders** seeking validation strategies
- **Early-stage teams** building their first product
- **Growth-stage startups** optimizing traction channels
- **Fundraising founders** preparing pitch decks
- **Solo founders** needing expert guidance 24/7

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

Built with insights from:
- The Lean Startup (Eric Ries)
- Zero to One (Peter Thiel)
- The Mom Test (Rob Fitzpatrick)
- And 12+ other essential startup books

Real case studies from: OpenAI, Stripe, Notion, Perplexity, Linear, Vercel, Midjourney

---

## 📧 Contact

For questions or feedback, please reach out or open an issue.

---

**Made with ❤️ for founders building the future**