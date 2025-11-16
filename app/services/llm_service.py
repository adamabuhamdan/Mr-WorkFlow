import io
from typing import Any, Dict, List
import json

import google.generativeai as genai

from app.config import settings


STAGE_DEFINITIONS = [
    {
        "id": "01_Ideation_Stage",
        "label": "Ideation Stage",
        "description": "Idea generation, problem discovery, customer interviews, opportunity framing.",
    },
    {
        "id": "02_Validation_Stage",
        "label": "Validation Stage",
        "description": "MVPs, experiments, user testing, rapid learning, validating problem-solution fit.",
    },
    {
        "id": "03_Product_Building_Stage",
        "label": "Product Building Stage",
        "description": "Product design, UX, feature development, building something people can use repeatedly.",
    },
    {
        "id": "04_Growth_Traction_Stage",
        "label": "Growth & Traction Stage",
        "description": "Acquisition channels, go-to-market, early traction, crossing the adoption gap.",
    },
    {
        "id": "05_Funding_Stage",
        "label": "Funding Stage",
        "description": "Fundraising strategy, angels, VCs, term sheets, negotiations, investor readiness.",
    },
    {
        "id": "06_Team_Leadership_Stage",
        "label": "Team & Leadership Stage",
        "description": "Hiring, culture, leadership, communication, managing people and teams.",
    },
    {
        "id": "07_Scaling_Stage",
        "label": "Scaling Stage",
        "description": "Hypergrowth, scaling systems, OKRs, performance management, scaling operations.",
    },
    {
        "id": "08_Strategic_Maturity_Stage",
        "label": "Strategic Maturity Stage",
        "description": "Long-term strategy, competitive advantage, execution discipline, strategic positioning.",
    },
]


class LLMService:
    """Wrapper around Google Gemini used to generate answers and classify stages."""

    def __init__(self) -> None:
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required")

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # ------------------ Stage detection (multi-stage) ------------------ #

    def detect_stages(self, question: str) -> List[str]:
        """Use Gemini to detect which stages are relevant to the user question.

        Returns a list of stage IDs such as:
        ["01_Ideation_Stage", "02_Validation_Stage"]
        or an empty list if no stage is clearly relevant.
        """
        stages_block_lines = []
        for s in STAGE_DEFINITIONS:
            stages_block_lines.append(
                f'- "{s["id"]}": {s["label"]} — {s["description"]}'
            )
        stages_block = "\n".join(stages_block_lines)

        prompt = f"""You are a classifier that maps user questions to startup lifecycle stages.

You are given a list of stages (with IDs, names, and descriptions) and a user question.
Your task is to return ALL stages that are relevant to answering this question.

Stages:
{stages_block}

User question:
{question}

Instructions:
1. Consider that the question may be in English or Arabic.
2. Choose every stage where the question would reasonably need knowledge from that stage.
   - For example, a question mixing funding and growth should select both "05_Funding_Stage" and "04_Growth_Traction_Stage".
3. If no stage clearly matches, return an empty list.
4. Your response MUST be a valid JSON array of strings, using ONLY the stage IDs.
   - Example: ["01_Ideation_Stage", "02_Validation_Stage"]
   - Example (no match): []

Return ONLY the JSON array. Do not add any explanation.
"""

        try:
            response = self.model.generate_content(prompt)
            raw = getattr(response, "text", "").strip()
            # Try to parse JSON directly
            stages = json.loads(raw)
            if isinstance(stages, list) and all(isinstance(x, str) for x in stages):
                return stages
        except Exception:
            # Fall back to a very simple heuristic: extract known IDs from the text
            text = (raw if "raw" in locals() else "").strip()
            detected: List[str] = []
            for s in STAGE_DEFINITIONS:
                if s["id"] in text:
                    detected.append(s["id"])
            return detected

        # If parsing failed and no IDs were found, return empty list
        return []

    # ------------------ image (multi-model) ------------------ #
    def generate_response_with_image(
        self,
        question: str,
        image_bytes: bytes,
        mime_type: str,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Generate a response based on a user question and an uploaded image.

        This uses Gemini's multimodal capabilities (vision + text).
        """

        # Build system prompt depending on the requested language
        if language == "ar":
            system_prompt = """You are an expert startup and product advisor.

You receive:
1) A user question written in Arabic or English.
2) An image (for example: a UI mockup, pitch deck slide, product screenshot, or diagram).

Your task:
- Answer ONLY in Modern Standard Arabic.
- Analyze the image and relate your answer directly to what you see.
- Combine the visual information with the user's question.
- Give practical, actionable advice suitable for startup founders.
- If the image is not very relevant, say that briefly and answer based on what you can infer.

Be concise, structured, and helpful."""
        else:
            system_prompt = """You are an expert startup and product advisor.

You receive:
1) A user question.
2) An image (such as a UI mockup, pitch deck slide, product screenshot, or diagram).

Your task:
- Analyze the image and relate your answer directly to what you see.
- Combine the visual information with the user's question.
- Provide clear, practical, and actionable advice for startup founders.
- If the image is not very relevant, state that briefly and still try to give helpful guidance.
- Do not mention internal implementation details or the fact that you are a model.

Be concise, structured, and helpful."""

        img = {
            "mime_type": mime_type,
            "data": image_bytes,
        }

        try:
            response = self.model.generate_content(
                [
                    system_prompt,
                    question,
                    img,
                ]
            )
            return {
                "answer": getattr(response, "text", ""),
                "success": True,
            }
        except Exception as e:  # noqa: BLE001
            error_msg = "Sorry, an error occurred while processing the image."
            return {
                "answer": f"{error_msg} Details: {e}",
                "success": False,
            }
    



    # ------------------ file (multi-model) ------------------ #
    def generate_response_with_file(
        self,
        question: str,
        file_bytes: bytes,
        filename: str,
        mime_type: str,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Generate a response based on a user question and an uploaded file.

        This uses Gemini's multimodal capabilities (file + text),
        for example with PDFs, markdown, or text documents.
        """

        # Build system prompt depending on the requested language
        if language == "ar":
            system_prompt = """You are an expert startup, business, and product advisor.

You receive:
1) A user question written in Arabic or English.
2) An uploaded file (for example: a pitch deck PDF, startup report, or business document).

Your task:
- Answer ONLY in Modern Standard Arabic.
- Read and understand the file content.
- Combine the information from the file with the user's question.
- Provide clear, practical, and actionable advice for startup founders.
- If the file is long, focus only on the most relevant sections.
- If the file is not very relevant, say that briefly and still try to give helpful guidance."""
        else:
            system_prompt = """You are an expert startup, business, and product advisor.

You receive:
1) A user question.
2) An uploaded file (such as a pitch deck PDF, startup report, or business document).

Your task:
- Read and understand the file content.
- Combine the information from the file with the user's question.
- Provide clear, practical, and actionable advice for startup founders.
- If the file is long, focus only on the most relevant sections.
- If the file is not very relevant, state that briefly and still try to be helpful.
- Do not mention internal implementation details or that you are an AI model.

Be concise, structured, and helpful."""

        # Wrap bytes in a file-like object for upload
        file_obj = io.BytesIO(file_bytes)

        try:
            # Upload the file to Gemini's file API
            uploaded_file = genai.upload_file(
                file_obj,
                mime_type=mime_type,
                display_name=filename,
            )

            # Call the multimodal model with system prompt + file + question
            response = self.model.generate_content(
                [
                    system_prompt,
                    uploaded_file,
                    question,
                ]
            )

            return {
                "answer": getattr(response, "text", ""),
                "success": True,
            }
        except Exception as e:  # noqa: BLE001
            error_msg = (
                "Sorry, an error occurred while processing the file."
                if language == "en"
                else "عذرًا، حدث خطأ أثناء معالجة الملف."
            )
            return {
                "answer": f"{error_msg} Details: {e}",
                "success": False,
            }

    # ------------------ Answer generation ------------------ #
    def generate_response(
        self,
        question: str,
        context_documents: List[Dict[str, Any]],
        language: str = "en",
    ) -> Dict[str, Any]:
        """Generate a response based on the user question and retrieved documents."""

        # Build a plain-text context block from the retrieved documents
        context_lines: List[str] = []
        sources_used: set[str] = set()

        for doc in context_documents:
            source = doc.get("source", "unknown")
            content = doc.get("content", "").strip()
            if not content:
                continue

            context_lines.append(f"Source: {source}\nContent:\n{content}\n")
            sources_used.add(source)

        context_text = "\n".join(context_lines)

        if language == "ar":
            system_prompt = f"""You are an expert advisor in entrepreneurship, innovation, and startup growth.

Your task is to answer the user's question **in Modern Standard Arabic only**, using the reference content below as your primary knowledge base.

Reference content:
{context_text}

Guidelines:
1. Answer in **Modern Standard Arabic** only.
2. Provide clear, practical, and actionable advice that a startup founder can apply.
3. When it helps, connect related concepts such as customer discovery, validation, experimentation, funding, growth, and team building.
4. You may combine insights from multiple sources if that leads to a better answer.
5. Do **not** mention any book titles, authors, or source file names explicitly.
6. If the reference content does not fully answer the question, infer reasonable advice from the principles you see and state that you are generalizing.
7. If the question is completely outside business, startups, or innovation, politely say that this is out of scope.

User question:
{question}

Now produce a structured, helpful answer **in Arabic** that applies the reference content to the user's situation."""
        else:
            system_prompt = f"""You are an expert advisor in entrepreneurship, innovation, and startup growth.

Your task is to answer the user's question **in English**, using the reference content below as your primary knowledge base.

Reference content:
{context_text}

Guidelines:
1. Answer in clear, concise, and practical English.
2. Focus on concrete, actionable advice that a startup founder can apply.
3. When useful, connect related concepts such as customer discovery, validation, experimentation, funding, growth, and team leadership.
4. You may synthesize insights from multiple sources if that improves the answer.
5. Do **not** mention any book titles, authors, or internal file names explicitly.
6. If the reference content only partially covers the question, explicitly explain your assumptions and generalize from the available concepts.
7. If the question is clearly outside the startup / business domain, politely state that it is out of scope.

User question:
{question}

Now produce a structured, helpful answer **in English** based on the reference content above."""

        try:
            response = self.model.generate_content(system_prompt)
            return {
                "answer": getattr(response, "text", ""),
                "sources": list(sources_used),
                "context_used": len(context_documents),
            }
        except Exception as e:  # noqa: BLE001
            error_msg = "Sorry, an error occurred while processing your request."
            return {
                "answer": f"{error_msg} Details: {e}",
                "sources": [],
                "context_used": 0,
            }
