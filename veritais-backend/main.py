"""
Veritais - Backend de Verificação de Fake News
FastAPI + Novo SDK Google GenAI + Google Fact Check API
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import base64
import os
import json
from datetime import datetime

# Importação do NOVO SDK moderno e oficial do Google Gemini
from google import genai
from google.genai import types

# Importações internas
from models import SessionLocal, Verification, init_db
from factcheck import check_google_factcheck, check_newsapi
from analyzer import build_analysis_prompt, parse_verdict

# ─── Chave de API ────────────────────────────────────────────────────────────
GEMINI_KEY = "AQ.Ab8RN6Lyxw6dKkg2Hg5GCSwafNCu5dHfjqmSPuUfcZoBeaAjvA"

# MODELO UNIVERSAL: Compatível com chaves Vertex AI / AI Studio e Python 3.14
TARGET_MODEL = "gemini-2.5-flash"

# ─── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Veritais API",
    description="API de verificação de fake news com codificação estável do Gemini",
    version="1.1.3"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Em produção, mude para seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa banco de dados SQLite automaticamente
init_db()

# ─── Schemas ──────────────────────────────────────────────────────────────────

class URLRequest(BaseModel):
    url: str
    context: Optional[str] = ""

class TextRequest(BaseModel):
    text: str
    title: Optional[str] = ""

class VerificationResponse(BaseModel):
    id: int
    verdict: str                  # "VERDADEIRO" | "FALSO" | "SUSPEITO" | "INCONCLUSIVO"
    confidence: int               # 0–100
    summary: str
    analysis: str
    sources_found: list
    checked_at: str


# ─── Rotas ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "Veritais API (Stable Gemini Powered)",
        "status": "online",
        "endpoints": ["/verify/url", "/verify/text", "/verify/image", "/history"]
    }


@app.post("/verify/url", response_model=VerificationResponse)
async def verify_url(req: URLRequest):
    """Verifica uma notícia a partir de uma URL extraindo seu conteúdo."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as http:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; Veritais/1.0)"}
            page = await http.get(req.url, headers=headers)
            page_text = page.text[:4000]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Não foi possível acessar a URL: {str(e)}")

    factcheck_results = await check_google_factcheck(page_text[:500])

    prompt = build_analysis_prompt(
        content=page_text,
        url=req.url,
        extra_context=req.context,
        factcheck_data=factcheck_results
    )

    try:
        client_secure = genai.Client(api_key=GEMINI_KEY)
        response = client_secure.models.generate_content(
            model=TARGET_MODEL,
            contents=prompt,
        )
        raw_analysis = response.text
        verdict_data = parse_verdict(raw_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API do Gemini: {str(e)}")

    db = SessionLocal()
    try:
        verification = Verification(
            input_type="url",
            input_value=req.url,
            verdict=verdict_data["verdict"],
            confidence=verdict_data["confidence"],
            summary=verdict_data["summary"],
            analysis=raw_analysis,
            sources_found=json.dumps(factcheck_results),
        )
        db.add(verification)
        db.commit()
        db.refresh(verification)
        record_id = verification.id
        created_at = verification.created_at
    finally:
        db.close()

    return VerificationResponse(
        id=record_id,
        verdict=verdict_data["verdict"],
        confidence=verdict_data["confidence"],
        summary=verdict_data["summary"],
        analysis=raw_analysis,
        sources_found=factcheck_results,
        checked_at=created_at.isoformat()
    )


@app.post("/verify/text", response_model=VerificationResponse)
async def verify_text(req: TextRequest):
    """Verifica um texto ou afirmação diretamente via Gemini."""
    factcheck_results = await check_google_factcheck(req.text[:500])

    prompt = build_analysis_prompt(
        content=req.text,
        title=req.title,
        factcheck_data=factcheck_results
    )

    try:
        client_secure = genai.Client(api_key=GEMINI_KEY)
        response = client_secure.models.generate_content(
            model=TARGET_MODEL,
            contents=prompt,
        )
        raw_analysis = response.text
        verdict_data = parse_verdict(raw_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API do Gemini: {str(e)}")

    db = SessionLocal()
    try:
        verification = Verification(
            input_type="text",
            input_value=req.text[:500],
            verdict=verdict_data["verdict"],
            confidence=verdict_data["confidence"],
            summary=verdict_data["summary"],
            analysis=raw_analysis,
            sources_found=json.dumps(factcheck_results),
        )
        db.add(verification)
        db.commit()
        db.refresh(verification)
        record_id = verification.id
        created_at = verification.created_at
    finally:
        db.close()

    return VerificationResponse(
        id=record_id,
        verdict=verdict_data["verdict"],
        confidence=verdict_data["confidence"],
        summary=verdict_data["summary"],
        analysis=raw_analysis,
        sources_found=factcheck_results,
        checked_at=created_at.isoformat()
    )


@app.post("/verify/image", response_model=VerificationResponse)
async def verify_image(file: UploadFile = File(...)):
    """Analisa uma imagem em busca de desinformação com tratamento estrito de credencial."""
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Formato de imagem não suportado.")

    image_bytes = await file.read()

    instructions = """Você é um especialista em verificação de fatos e análise de mídia.
                    
Analise esta imagem e responda OBRIGATORIAMENTE em formato JSON válido com este formato exato:

{
  "verdict": "VERDADEIRO|FALSO|SUSPEITO|INCONCLUSIVO",
  "confidence": 85,
  "summary": "<resumo em 1 frase>",
  "analysis": "<análise detalhada em português>"
}

Considere:
- A imagem contém texto com afirmações falsas?
- A imagem parece ter sido manipulada digitalmente?
- O contexto visual sugere desinformação?
- Há inconsistências visuais ou elementos editados?"""

    try:
        client_secure = genai.Client(api_key=GEMINI_KEY)
        response = client_secure.models.generate_content(
            model=TARGET_MODEL,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=file.content_type,
                ),
                instructions
            ]
        )
        raw_analysis = response.text
        verdict_data = parse_verdict(raw_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API multimodal do Gemini: {str(e)}")

    db = SessionLocal()
    try:
        verification = Verification(
            input_type="image",
            input_value=file.filename or "imagem_enviada",
            verdict=verdict_data["verdict"],
            confidence=verdict_data["confidence"],
            summary=verdict_data["summary"],
            analysis=raw_analysis,
            sources_found=json.dumps([]),
        )
        db.add(verification)
        db.commit()
        db.refresh(verification)
        record_id = verification.id
        created_at = verification.created_at
    finally:
        db.close()

    return VerificationResponse(
        id=record_id,
        verdict=verdict_data["verdict"],
        confidence=verdict_data["confidence"],
        summary=verdict_data["summary"],
        analysis=raw_analysis,
        sources_found=[],
        checked_at=created_at.isoformat()
    )


@app.get("/history")
def get_history(limit: int = 20, skip: int = 0):
    """Retorna o histórico de verificações."""
    db = SessionLocal()
    try:
        verifications = (
            db.query(Verification)
            .order_by(Verification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            {
                "id": v.id,
                "input_type": v.input_type,
                "input_value": v.input_value[:100],
                "verdict": v.verdict,
                "confidence": v.confidence,
                "summary": v.summary,
                "checked_at": v.created_at.isoformat()
            }
            for v in verifications
        ]
    finally:
        db.close()


@app.get("/history/{verification_id}")
def get_verification(verification_id: int):
    """Retorna uma verificação específica com análise completa."""
    db = SessionLocal()
    try:
        v = db.query(Verification).filter(Verification.id == verification_id).first()
        if not v:
            raise HTTPException(status_code=404, detail="Verificação não encontrada.")
        return {
            "id": v.id,
            "input_type": v.input_type,
            "input_value": v.input_value,
            "verdict": v.verdict,
            "confidence": v.confidence,
            "summary": v.summary,
            "analysis": v.analysis,
            "sources_found": json.loads(v.sources_found or "[]"),
            "checked_at": v.created_at.isoformat()
        }
    finally:
        db.close()


@app.delete("/history/{verification_id}")
def delete_verification(verification_id: int):
    """Remove uma verificação do histórico."""
    db = SessionLocal()
    try:
        v = db.query(Verification).filter(Verification.id == verification_id).first()
        if not v:
            raise HTTPException(status_code=404, detail="Verificação não encontrada.")
        db.delete(v)
        db.commit()
        return {"message": "Verificação removida com sucesso."}
    finally:
        db.close()