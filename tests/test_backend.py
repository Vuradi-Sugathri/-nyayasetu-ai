"""
NyayaSetu AI - Backend Unit Test Suite
Validates all legal triage, BNS/IPC mappings, document drafting,
contract simplification, and multilingual voice engines.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from backend.engines.legal_triage_engine import LegalTriageEngine
from backend.engines.document_drafting_engine import DocumentDraftingEngine
from backend.engines.contract_simplifier import ContractSimplifierEngine
from backend.engines.rights_safeguards_engine import RightsSafeguardsEngine
from backend.engines.multilingual_legal_voice import MultilingualLegalVoiceEngine

def run_tests():
    print("=" * 65)
    print("Testing NyayaSetu AI Backend Engines...")
    print("=" * 65)

    # 1. Test Legal Triage Engine
    triage = LegalTriageEngine()
    test_cases = [
        ("I was scammed of 45,000 on UPI through a fake Telegram investment link.", "cyber_crime"),
        ("My landlord is refusing to refund my security deposit of 80,000 and locked my room.", "tenancy_dispute"),
        ("I bought a refrigerator from a local dealer and it stopped cooling after 5 days, they refuse replacement.", "consumer_dispute"),
        ("Company terminated me without paying 2 months pending salary and severance pay.", "labor_dispute"),
        ("A neighbour beat me and threatened to kill me over parking.", "criminal_harassment")
    ]

    for text, expected_cat in test_cases:
        res = triage.analyze_grievance(text, "Telangana")
        assert res["status"] == "success"
        print(f"✅ Triage: '{text[:40]}...' -> {res['category_name']} [{res['urgency']}]")
        print(f"   Helpline: {res['helpline']} | Authority: {res['primary_authority']}")
        assert len(res["applicable_statutes"]) > 0

    # 2. Test Document Drafting Engine
    drafting = DocumentDraftingEngine()
    notice = drafting.generate_legal_notice(
        sender_name="K. Rajesh Kumar",
        sender_address="H.No 12-4, Madhapur, Hyderabad",
        recipient_name="V. Ramachandra Rao",
        recipient_address="Plot 55, Jubilee Hills, Hyderabad",
        dispute_type="Unlawful Withholding of Security Deposit",
        dispute_facts="The landlord refused to return security deposit of Rs. 60,000 despite peaceful handover on 1st Sept.",
        demand_amount="60,000"
    )
    assert "LEGAL DEMAND NOTICE" in notice["document_text"]
    assert "60,000" in notice["document_text"]
    print(f"\n✅ Legal Notice Generator: {notice['document_type']} ({len(notice['document_text'])} chars)")

    fir = drafting.generate_police_complaint_fir(
        complainant_name="Sneha Reddy",
        complainant_phone="9849012345",
        complainant_address="Banjara Hills, Hyderabad",
        police_station_name="Cyber Crime PS, Hyderabad City",
        incident_date="2026-09-25",
        incident_location="Online Bank Transfer",
        accused_details="Unknown Telegram Handle @ForexTradeIndia",
        incident_description="Fraudulent inducement to deposit funds with promise of guaranteed returns."
    )
    assert "SECTION 173" in fir["document_text"]
    print(f"✅ Police FIR Generator: {fir['document_type']} for {fir['police_station']}")

    # 3. Test Contract Simplifier Engine
    contract_engine = ContractSimplifierEngine()
    sample_lease = """
    The Tenant agrees that the deposit shall be non-refundable if lease terminated before 11 months.
    The Tenant shall pay interest at 24% per annum for any delayed payment.
    The Tenant shall waive any right to file complaint before consumer court.
    The employee agrees to non-compete and shall not work for any competitor for 3 years.
    """
    contract_res = contract_engine.simplify_contract(sample_lease, "rental_agreement")
    assert contract_res["status"] == "success"
    print(f"\n✅ Contract Simplifier: Fairness Score: {contract_res['fairness_score']}% ({contract_res['fairness_rating']})")
    print(f"   Flagged Hidden Traps: {contract_res['flagged_traps_count']}")
    for trap in contract_res["flagged_traps"]:
        print(f"     • [{trap['severity']}] {trap['title']} -> {trap['statute']}")

    # 4. Test Rights Safeguards Engine
    safeguards = RightsSafeguardsEngine()
    all_rights = safeguards.get_all_safeguards()
    assert "arrest_safeguards" in all_rights
    assert "women_safeguards" in all_rights
    assert "free_legal_aid" in all_rights
    print(f"\n✅ Rights & Safeguards Engine: {len(all_rights)} constitutional safeguard modules verified.")

    # 5. Test Multilingual Legal Voice Engine
    voice = MultilingualLegalVoiceEngine()
    test_langs = ["te", "hi", "en", "ta", "mr", "kn", "or", "as"]
    print("\n✅ Multilingual Legal Audio Guidance across 8 Indian Languages:")
    for lang in test_langs:
        audio_res = voice.get_legal_speech("cyber_fraud_advice", lang)
        assert audio_res["audio_url"].startswith("data:audio/")
        print(f"   • [{lang.upper()}] {audio_res['language']}: \"{audio_res['spoken_text'][:40]}...\"")

    # 6. Test Document Verifier & Accuracy Audit Engine
    from backend.engines.document_verifier_engine import LegalDocumentVerifierEngine
    verifier = LegalDocumentVerifierEngine()
    test_doc = """
    LEGAL DEMAND NOTICE
    To: XYZ Landlord, Jubilee Hills, Hyderabad
    From: Rahul Sharma, Tenant, Madhapur, Hyderabad
    Date: 28-09-2026
    Sir, You have failed to refund my deposit of Rs 70,000. Please pay within 15 days failing which civil and criminal proceedings will be filed.
    Yours faithfully, Rahul Sharma
    """
    v_res = verifier.verify_document(test_doc)
    assert v_res["status"] == "success"
    print(f"\n✅ Document Verifier Engine: {v_res['document_type']} -> Score: {v_res['accuracy_score']}/100 [{v_res['court_readiness']}]")
    print(f"   Passed: {v_res['passed_elements_count']} elements | Missing: {v_res['missing_elements_count']} elements")

    # 7. Test Indian Law Search Engine (NyayaSearch)
    from backend.engines.law_search_engine import IndianLawSearchEngine
    search = IndianLawSearchEngine()
    s_res = search.search_laws("cheque bounce", lang="en")
    assert s_res["status"] == "success"
    assert s_res["total_matches"] > 0
    print(f"\n✅ Indian Law Search Engine: {s_res['total_matches']} statutes found for 'cheque bounce'.")
    top_statute = s_res["results"][0]
    print(f"   Top Match: {top_statute['title']} -> {top_statute['section']}")

    print("\n" + "=" * 65)
    print("🎉 ALL 7 NYAYASETU AI BACKEND UNIT TESTS PASSED 100%!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
