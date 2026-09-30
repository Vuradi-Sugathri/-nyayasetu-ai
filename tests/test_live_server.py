"""
NyayaSetu AI - Live Server Verification Suite
Validates all HTTP endpoints, BNS mapping, document drafting, contract analysis, and audio routes on Port 8003.
"""

import sys
import requests
import json
import time

# Ensure UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8003"

def wait_for_server(max_retries=10, delay=1.0):
    for i in range(max_retries):
        try:
            res = requests.get(f"{BASE_URL}/api/health", timeout=2)
            if res.status_code == 200:
                print(f"[OK] Server is UP and healthy on port 8003 (attempt {i+1})")
                return True
        except Exception:
            time.sleep(delay)
    return False

def test_endpoints():
    print("=" * 70)
    print("NYAYASETU AI - LIVE SERVER TEST SUITE (PORT 8003)")
    print("=" * 70)

    # 1. Health Endpoint
    print("\n[1] Testing GET /api/health ...")
    res = requests.get(f"{BASE_URL}/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    health = res.json()
    print(f"  App Name: {health['app_name']}")
    print(f"  Port: {health['port']}")
    print(f"  Supported Laws: {len(health['supported_laws'])} frameworks")
    assert health['port'] == 8003

    # 2. Index HTML
    print("\n[2] Testing GET / (Frontend Index) ...")
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    assert "న్యాయసేతు AI" in res.text
    print("  ✓ Frontend HTML serves successfully with judicial title & tags.")

    # 3. Legal Triage (Cybercrime)
    print("\n[3] Testing POST /api/legal/triage (Cybercrime Grievance) ...")
    payload = {
        "grievance_text": "I lost 45,000 rupees in a UPI phishing scam where a caller posed as my bank manager and then blocked me.",
        "location": "Telangana"
    }
    res = requests.post(f"{BASE_URL}/api/legal/triage", json=payload)
    assert res.status_code == 200
    triage = res.json()
    cat_name = triage.get('category_name') or triage.get('category')
    statutes = triage.get('applicable_statutes') or triage.get('applicable_sections')
    print(f"  Category: {cat_name}")
    print(f"  Urgency: {triage.get('urgency') or triage.get('severity')}")
    print(f"  Mapped Statutes: {[s['section'] for s in statutes]}")
    assert any("318" in s['section'] or "66D" in s['section'] for s in statutes)

    # 4. Document Drafter: Pre-Litigation Legal Notice
    print("\n[4] Testing POST /api/legal/draft-notice ...")
    notice_payload = {
        "sender_name": "Kavitha Reddy",
        "sender_address": "Plot 101, Kavuri Hills, Hyderabad, Telangana",
        "recipient_name": "ABC Real Estate Developers Pvt Ltd",
        "recipient_address": "Financial District, Gachibowli, Hyderabad",
        "dispute_type": "Rental Security Deposit Refund",
        "dispute_facts": "The recipient has failed to refund the security deposit of Rs 80,000 despite peaceful vacation of the premises.",
        "demand_amount": "80,000",
        "notice_period_days": 15,
        "location": "Hyderabad, Telangana"
    }
    res = requests.post(f"{BASE_URL}/api/legal/draft-notice", json=notice_payload)
    assert res.status_code == 200
    notice = res.json()
    doc_text = notice.get('document_text') or notice.get('formatted_text')
    print(f"  Notice Type: {notice['document_type']}")
    assert "FORMAL LEGAL DEMAND NOTICE" in doc_text
    assert "80,000" in doc_text

    # 5. Document Drafter: Police FIR under Sec 173 BNSS
    print("\n[5] Testing POST /api/legal/draft-fir ...")
    fir_payload = {
        "complainant_name": "Kavitha Reddy",
        "complainant_phone": "9876543210",
        "complainant_address": "Kavuri Hills, Hyderabad",
        "police_station_name": "Cyber Crime Police Station, Hyderabad Commissionerate",
        "incident_date": "2026-09-28",
        "incident_location": "Hyderabad, Telangana",
        "accused_details": "Unknown cyber fraudster posing as bank official",
        "incident_description": "Fraudulent withdrawal of funds via rogue UPI gateway",
        "applicable_sections": "Section 316, 318 BNS 2023 & Section 66D IT Act"
    }
    res = requests.post(f"{BASE_URL}/api/legal/draft-fir", json=fir_payload)
    assert res.status_code == 200
    fir = res.json()
    fir_text = fir.get('document_text') or fir.get('formatted_text')
    print(f"  Application Type: {fir['document_type']}")
    assert "SECTION 173 OF BHARATIYA NAGARIK SURAKSHA SANHITA" in fir_text

    # 6. Contract Simplifier: Unfair Non-Compete & Forfeiture
    print("\n[6] Testing POST /api/legal/simplify-contract ...")
    contract_text = (
        "1. The employee shall not work for any competitor for 3 years post separation. "
        "2. The employer reserves the right to terminate without any notice. "
        "3. Entire deposit shall be non-refundable if tenant leaves early."
    )
    res = requests.post(
        f"{BASE_URL}/api/legal/simplify-contract",
        data={"contract_text": contract_text, "contract_type": "employment_contract"}
    )
    assert res.status_code == 200
    contract = res.json()
    traps = contract.get('flagged_traps') or contract.get('unfair_clauses_identified')
    print(f"  Fairness Score: {contract['fairness_score']}/100")
    print(f"  Identified Unfair Clauses: {len(traps)}")
    for trap in traps:
        print(f"    - [{trap.get('statute') or trap.get('legal_statute')}] {trap.get('title') or trap.get('issue')}")
    assert contract['fairness_score'] < 60  # Flagged as high risk

    # 7. Constitutional Rights Safeguards
    print("\n[7] Testing GET /api/legal/safeguards ...")
    res = requests.get(f"{BASE_URL}/api/legal/safeguards")
    assert res.status_code == 200
    safeguards = res.json()
    print(f"  Safeguards Categories: {list(safeguards.keys())}")
    assert "arrest_safeguards" in safeguards
    assert "women_safeguards" in safeguards
    assert "free_legal_aid" in safeguards

    # 8. Multilingual Legal Voice Advice
    print("\n[8] Testing POST /api/legal/voice (Telugu Advice) ...")
    voice_payload = {
        "topic_key": "cyber_fraud_advice",
        "lang": "te"
    }
    res = requests.post(f"{BASE_URL}/api/legal/voice", json=voice_payload)
    assert res.status_code == 200
    voice = res.json()
    print(f"  Language: {voice['language']}")
    # 9. Legal Document Verifier & Accuracy Audit
    print("\n[9] Testing POST /api/legal/verify-document ...")
    test_notice = """
    LEGAL DEMAND NOTICE
    To: Global Tech Solutions, HITEC City, Hyderabad
    From: Amit Kumar, Software Engineer, Madhapur, Hyderabad
    Date: 28-09-2026
    Sir, You have terminated my contract without 30 days statutory notice and withheld my 2 months salary of Rs 1,50,000.
    Please pay within 15 days failing which legal civil recovery and criminal proceedings will be initiated.
    Yours faithfully,
    Amit Kumar
    """
    res = requests.post(f"{BASE_URL}/api/legal/verify-document", data={"doc_text": test_notice})
    assert res.status_code == 200
    v = res.json()
    print(f"  Document Type: {v['document_type']}")
    print(f"  Accuracy Score: {v['accuracy_score']}/100")
    print(f"  Court Readiness: {v['court_readiness']}")
    print(f"  Passed Elements: {v['passed_elements_count']}, Missing Elements: {v['missing_elements_count']}")
    assert v['accuracy_score'] >= 50

    # 10. Indian Law Search (NyayaSearch)
    print("\n[10] Testing GET /api/legal/search-laws?q=cheating&lang=en ...")
    res = requests.get(f"{BASE_URL}/api/legal/search-laws", params={"q": "cheating", "lang": "en"})
    assert res.status_code == 200
    s = res.json()
    print(f"  Total Matches for 'cheating': {s['total_matches']}")
    assert s['total_matches'] > 0
    top_result = s['results'][0]
    print(f"  Top Match: {top_result['title']} ({top_result['section']})")
    assert "318" in top_result['section']

    # 11. Citizen Legal Encyclopedia (All Laws)
    print("\n[11] Testing GET /api/legal/all-laws?lang=te ...")
    res = requests.get(f"{BASE_URL}/api/legal/all-laws", params={"lang": "te"})
    assert res.status_code == 200
    all_laws = res.json()
    print(f"  Total Indexed Indian Laws: {all_laws['total_matches']}")
    assert all_laws['total_matches'] >= 10

    print("\n" + "=" * 70)
    print("ALL 11 LIVE SERVER ENDPOINT TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    if not wait_for_server():
        print("[FAIL] Server failed to start on port 8003 within timeout.")
        sys.exit(1)
    test_endpoints()
