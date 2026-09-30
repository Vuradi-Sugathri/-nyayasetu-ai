"""
NyayaSetu AI (న్యాయసేతు AI) - Universal 1-Click System Launcher
Dedicated Port: 8003
Features:
- BNS 2023 & BNSS 2023 Statutory Mapping
- Pre-Litigation Legal Demand Notice & Police FIR Drafter
- Void Contract & Non-Compete Analyzer (Sec 27 Contract Act)
- Constitutional Rights Safeguards & NALSA Legal Aid Guide
- 8 Indian Languages Localization & Spoken Legal Voice Guidance
- 100% Offline & Zero External Cloud Dependencies
"""

import sys
import os
from pathlib import Path

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def print_banner():
    banner = r"""
================================================================================
   ⚖️   NYAYASETU AI (న్యాయసేతు AI)   ⚖️
   AI-Powered Legal Tech & Citizen Justice Bridge for Indian Citizens
   Bharatiya Nyaya Sanhita (BNS 2023) | BNSS 2023 | Constitution of India
================================================================================
  * Port Allocation:        8003 (AgroPulse: 8000 | NetraShiksha: 8001 | SurakshaVision: 8002)
  * Default Location:       Telangana (Centroid Locked: 17.3850 N, 78.4867 E)
  * Primary Language:       Telugu (తెలుగు) + 7 Indian Languages (hi, en, ta, mr, kn, or, as)
  * Statutes Integrated:    BNS 2023, BNSS 2023, IPC 1860, Consumer Act 2019, IT Act 2000
  * External Dependencies:  0 (Runs 100% locally with zero cloud token cost)
================================================================================
  >>> ACCESS NYAYASETU AI PORTAL: http://127.0.0.1:8003
================================================================================
"""
    print(banner)

def main():
    print_banner()
    print("[1/3] Pre-warming legal inference engines...")
    try:
        from backend.engines.legal_triage_engine import LegalTriageEngine
        from backend.engines.document_drafting_engine import DocumentDraftingEngine
        from backend.engines.contract_simplifier import ContractSimplifierEngine
        from backend.engines.rights_safeguards_engine import RightsSafeguardsEngine
        from backend.engines.multilingual_legal_voice import MultilingualLegalVoiceEngine
        from backend.engines.document_verifier_engine import LegalDocumentVerifierEngine
        from backend.engines.law_search_engine import IndianLawSearchEngine
        
        triage = LegalTriageEngine()
        drafting = DocumentDraftingEngine()
        contract = ContractSimplifierEngine()
        safeguards = RightsSafeguardsEngine()
        voice = MultilingualLegalVoiceEngine()
        verifier = LegalDocumentVerifierEngine()
        law_search = IndianLawSearchEngine()
        print("  ✓ All 7 Legal Engines (Triage, Drafter, Verifier, Law Search, Contract, Rights, Voice) loaded successfully.")
    except Exception as e:
        print(f"  [!] Warning during engine pre-warming: {e}")

    print("[2/3] Checking audio cache directory...")
    audio_dir = PROJECT_ROOT / "data" / "audio_cache"
    audio_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Audio cache ready: {audio_dir}")

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8003"))
    print(f"[3/3] Starting NyayaSetu AI Web Server on http://{host}:{port} ...")
    import uvicorn
    uvicorn.run("backend.main:app", host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
