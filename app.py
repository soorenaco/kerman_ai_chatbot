"""
سامانه پیشنهادگر سرمایه‌گذاری کرمان
Kerman Investment Advisory Chatbot
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List
import json, pickle, os, numpy as np
from openai import OpenAI

# =====================
# تنظیمات / Settings
# =====================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH", "projects.index")
METADATA_PATH = os.getenv("METADATA_PATH", "projects_metadata.pkl")

app = FastAPI(title="Kerman Investment Advisor")

# =====================
# بارگذاری مدل‌ها
# =====================
print("Loading embedding model...")
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

print("Loading FAISS index...")
import faiss
index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, 'rb') as f:
    meta = pickle.load(f)

projects = meta['projects']
project_texts = meta['texts']
print(f"Loaded {len(projects)} projects ✓")

# OpenRouter client — از ایران کار می‌کنه
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# =====================
# System Prompt دوزبانه
# =====================
SYSTEM_PROMPT = """You are «Kerman Investment Advisor» / «مشاور هوشمند سرمایه‌گذاری کرمان».

LANGUAGE RULE (VERY IMPORTANT):
- If the user writes in Persian/Farsi → respond ONLY in Persian
- If the user writes in English → respond ONLY in English
- Never mix languages in a single response

YOUR ROLE:
You help investors find the best investment opportunities in Kerman Province, Iran.
Gather info through friendly conversation:
1. Budget / بودجه
2. Preferred sector / حوزه (agriculture/mining/services/energy/technology)
3. Region / منطقه (north/center/southwest/southeast)
4. Risk tolerance / سطح ریسک (low/medium/high)
5. Return period / دوره بازگشت

RESPONSE RULES:
- Only use information from the provided project data
- Always explain WHY you recommend a project
- Show key metrics: investment amount, IRR%, payback period, risk level
- If no exact match, suggest closest alternatives
- Keep responses concise but informative
- Ask follow-up questions when needed"""


# =====================
# توابع اصلی
# =====================
def search_projects(query: str, top_k: int = 4):
    query_vec = embedder.encode(
        [query], normalize_embeddings=True
    ).astype(np.float32)
    scores, indices = index.search(query_vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1 and score > 0.15:
            results.append({
                'project': projects[idx],
                'text': project_texts[idx],
                'score': float(score)
            })
    return results


def build_context(retrieved):
    if not retrieved:
        return "No matching projects found. / پروژه مرتبطی یافت نشد."
    context = "RELEVANT PROJECTS / پروژه‌های مرتبط:\n\n"
    for i, r in enumerate(retrieved, 1):
        context += f"--- Project {i} / پروژه {i} ---\n"
        context += r['text'] + "\n\n"
    return context


def chat_rag(user_message: str, history: list) -> str:
    retrieved = search_projects(user_message)
    context = build_context(retrieved)
    augmented = f"{context}\nUser message / پیام کاربر: {user_message}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-8:]:
        messages.append(msg)
    messages.append({"role": "user", "content": augmented})

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",  # مدل رایگان OpenRouter
        messages=messages,
        max_tokens=1024,
        temperature=0.3,
    )
    return response.choices[0].message.content


# =====================
# API Routes
# =====================
class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []


class ChatResponse(BaseModel):
    reply: str
    retrieved_count: int


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        retrieved = search_projects(req.message)
        reply = chat_rag(req.message, req.history)
        return ChatResponse(reply=reply, retrieved_count=len(retrieved))
    except Exception as e:
        import traceback
        print("=== ERROR ===")
        print(traceback.format_exc())
        print("=============")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "projects": len(projects)}


@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)