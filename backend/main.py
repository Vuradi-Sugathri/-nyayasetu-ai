"""
NyayaSetu AI - Main FastAPI Application Server
AI-Powered Legal Tech & Citizen Justice Bridge for Indian Citizens
Runs on Port: 8003 | Zero External Cloud Dependencies
"""

import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from backend.engines.legal_triage_engine import LegalTriageEngine
from backend.engines.document_drafting_engine import DocumentDraftingEngine
from backend.engines.contract_simplifier import ContractSimplifierEngine
from backend.engines.rights_safeguards_engine import RightsSafeguardsEngine
from backend.engines.multilingual_legal_voice import MultilingualLegalVoiceEngine, LANG_CONFIG
from backend.engines.document_verifier_engine import LegalDocumentVerifierEngine
from backend.engines.law_search_engine import IndianLawSearchEngine

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
DATA_DIR = BASE_DIR / "data"

# Ensure data and audio cache directories exist prior to mounting
DATA_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "audio_cache").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="NyayaSetu AI API",
    description="AI-Powered Citizen Legal Bridge, BNS/IPC Mapping, and Document Drafting",
    version="1.0.0"
)

# Environment-aware CORS configuration
raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [orig.strip() for orig in raw_origins.split(",") if orig.strip()]
is_wildcard = "*" in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=not is_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# Engine Singletons
triage_engine = LegalTriageEngine()
drafting_engine = DocumentDraftingEngine()
contract_engine = ContractSimplifierEngine()
safeguards_engine = RightsSafeguardsEngine()
voice_engine = MultilingualLegalVoiceEngine()
verifier_engine = LegalDocumentVerifierEngine()
search_engine = IndianLawSearchEngine()

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB upload ceiling to mitigate DoS / Memory exhaustion

async def read_uploaded_file_safe(file: Optional[UploadFile]) -> str:
    """Reads uploaded file safely with size validation."""
    if not file:
        return ""
    content_bytes = await file.read(MAX_UPLOAD_SIZE + 1)
    if len(content_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Uploaded file exceeds the maximum permitted size of 5 MB."
        )
    try:
        return content_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""

class TriageRequest(BaseModel):
    grievance_text: str = Field(..., min_length=3, max_length=15000)
    location: Optional[str] = Field("Telangana", max_length=100)

class NoticeDraftRequest(BaseModel):
    sender_name: str = Field(..., min_length=1, max_length=200)
    sender_address: str = Field(..., min_length=1, max_length=500)
    recipient_name: str = Field(..., min_length=1, max_length=200)
    recipient_address: str = Field(..., min_length=1, max_length=500)
    dispute_type: str = Field(..., min_length=1, max_length=200)
    dispute_facts: str = Field(..., min_length=3, max_length=15000)
    demand_amount: Optional[str] = Field("50,000", max_length=50)
    notice_period_days: Optional[int] = Field(15, ge=1, le=180)
    location: Optional[str] = Field("Hyderabad", max_length=100)

class FIRDraftRequest(BaseModel):
    complainant_name: str = Field(..., min_length=1, max_length=200)
    complainant_phone: str = Field(..., min_length=1, max_length=50)
    complainant_address: str = Field(..., min_length=1, max_length=500)
    police_station_name: str = Field(..., min_length=1, max_length=300)
    incident_date: str = Field(..., min_length=1, max_length=50)
    incident_location: str = Field(..., min_length=1, max_length=200)
    accused_details: str = Field(..., min_length=1, max_length=500)
    incident_description: str = Field(..., min_length=3, max_length=15000)
    applicable_sections: Optional[str] = Field("Section 303, 318 BNS 2023", max_length=300)

class VoiceRequest(BaseModel):
    topic_key: str = Field("intro_welcome", max_length=100)
    lang: str = Field("te", max_length=10)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>NyayaSetu AI is running.</h1>")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": "NyayaSetu AI (न्यायसेतु AI)",
        "version": "1.0.0",
        "port": 8003,
        "supported_laws": [
            "Bharatiya Nyaya Sanhita, 2023 (BNS)",
            "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
            "Indian Penal Code, 1860 (Legacy IPC Cross-References)",
            "Consumer Protection Act, 2019",
            "Information Technology Act, 2000",
            "Industrial Disputes Act, 1947",
            "Model Tenancy Act / Rent Control Act",
            "Constitution of India (Articles 21, 22, 39A)"
        ],
        "supported_languages": LANG_CONFIG
    }

@app.post("/api/legal/triage")
async def legal_triage(req: TriageRequest):
    """Analyzes citizen legal grievance and maps BNS/IPC sections."""
    if not req.grievance_text.strip():
        raise HTTPException(status_code=400, detail="Grievance text cannot be empty.")
    return triage_engine.analyze_grievance(req.grievance_text, req.location or "Telangana")

@app.post("/api/legal/draft-notice")
async def draft_legal_notice(req: NoticeDraftRequest):
    """Generates formal Pre-Litigation Legal Demand Notice."""
    return drafting_engine.generate_legal_notice(
        sender_name=req.sender_name,
        sender_address=req.sender_address,
        recipient_name=req.recipient_name,
        recipient_address=req.recipient_address,
        dispute_type=req.dispute_type,
        dispute_facts=req.dispute_facts,
        demand_amount=req.demand_amount or "50,000",
        notice_period_days=req.notice_period_days or 15,
        location=req.location or "Hyderabad"
    )

@app.post("/api/legal/draft-fir")
async def draft_police_complaint(req: FIRDraftRequest):
    """Generates formal Police Complaint / FIR Application under Section 173 BNSS."""
    return drafting_engine.generate_police_complaint_fir(
        complainant_name=req.complainant_name,
        complainant_phone=req.complainant_phone,
        complainant_address=req.complainant_address,
        police_station_name=req.police_station_name,
        incident_date=req.incident_date,
        incident_location=req.incident_location,
        accused_details=req.accused_details,
        incident_description=req.incident_description,
        applicable_sections=req.applicable_sections or "Section 303, 318 BNS 2023"
    )

@app.post("/api/legal/simplify-contract")
async def simplify_contract(
    contract_text: Optional[str] = Form(None),
    contract_type: Optional[str] = Form("rental_agreement"),
    file: Optional[UploadFile] = File(None)
):
    """Simplifies contracts, identifies illegal non-competes, and scores fairness."""
    text_to_analyze = contract_text or ""
    if file:
        uploaded_content = await read_uploaded_file_safe(file)
        if uploaded_content:
            text_to_analyze += "\n" + uploaded_content

    if not text_to_analyze.strip():
        # Fallback sample contract
        text_to_analyze = "The Tenant shall forfeit the entire deposit if vacated before 11 months. The employee agrees to non-compete for 2 years."

    return contract_engine.simplify_contract(text_to_analyze, contract_type or "agreement")

@app.get("/api/legal/safeguards")
async def get_safeguards():
    """Returns directory of constitutional rights & arrest safeguards."""
    return safeguards_engine.get_all_safeguards()

@app.post("/api/legal/voice")
async def get_legal_voice(req: VoiceRequest):
    """Synthesizes spoken legal audio in native Indian language."""
    return voice_engine.get_legal_speech(req.topic_key, req.lang or "te")

@app.post("/api/legal/verify-document")
async def verify_legal_document(
    doc_text: Optional[str] = Form(None),
    declared_type: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Audits legal document for statutory compliance, court readiness & missing elements."""
    text_to_audit = doc_text or ""
    if file:
        uploaded_content = await read_uploaded_file_safe(file)
        if uploaded_content:
            text_to_audit += "\n" + uploaded_content

    if not text_to_audit.strip():
        raise HTTPException(status_code=400, detail="Please provide document text or upload a valid file.")

    return verifier_engine.verify_document(text_to_audit, declared_type)

@app.get("/api/legal/search-laws")
async def search_laws(
    q: str = "",
    category: Optional[str] = None,
    lang: str = "en"
):
    """Searches comprehensive Indian law repository by keyword, section, or everyday scenario."""
    return search_engine.search_laws(query=q, category=category, lang=lang)

@app.get("/api/legal/all-laws")
async def get_all_laws(lang: str = "en"):
    """Returns all indexed Indian laws for the citizen legal encyclopedia."""
    return search_engine.search_laws(query="", category=None, lang=lang)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8003"))
    reload = os.getenv("ENVIRONMENT", "development").lower() == "development"
    uvicorn.run("backend.main:app", host=host, port=port, reload=reload)
