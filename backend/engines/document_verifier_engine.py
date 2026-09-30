"""
NyayaSetu AI - Legal Document Verifier & Accuracy Audit Engine
Analyzes uploaded or pasted legal documents (Pre-Litigation Notices, Police FIR Complaints,
Tenancy Agreements, Employment Contracts, Affidavits, Consumer Petitions, Cheque Bounce Notices)
for legal validity, missing statutory elements, section accuracy under BNS/BNSS/IPC, and court readiness.
"""

import re
from typing import Dict, List, Any, Optional

class LegalDocumentVerifierEngine:
    def __init__(self):
        # Mandatory Element Rules per Document Type
        self.doc_type_rules = {
            "legal_notice": {
                "name": "Pre-Litigation Legal Demand Notice",
                "keywords": ["legal notice", "demand notice", "advocate", "undersigned", "hereby call upon you", "within 15 days", "within 30 days", "failing which"],
                "mandatory_elements": [
                    {
                        "id": "parties_identification",
                        "title": "Clear Identification of Parties & Addresses",
                        "pattern": r"(to\s*[:,\n].{5,100}from\s*[:,\n]|on behalf of my client|undersigned|residing at)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Missing clear Sender (Complainant) and Recipient (Opposite Party) names and verifiable physical addresses."
                    },
                    {
                        "id": "cause_of_action",
                        "title": "Specific Facts & Cause of Action with Dates",
                        "pattern": r"(facts|dated|entered into|transaction|agreement|on or about|on \d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Missing specific dates, transaction details, or chronological chain of events giving rise to the dispute."
                    },
                    {
                        "id": "statutory_cure_period",
                        "title": "Explicit Statutory Cure / Notice Window (e.g. 15 or 30 Days)",
                        "pattern": r"(\b(15|30|7|21)\s*days?\b|within\s+\d+\s+days)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Missing clear statutory time window (e.g. 'within 15 days from receipt of this notice') to rectify the grievance."
                    },
                    {
                        "id": "crystallized_demand",
                        "title": "Quantified Claim Amount / Specific Relief Sought",
                        "pattern": r"(rs\.?|inr|\u20b9|sum of|amount of|refund|possession|deliver)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "The relief or financial demand is vague. Specify exact principal sum, interest rate, and litigation costs."
                    },
                    {
                        "id": "consequence_warning",
                        "title": "Warning of Impending Civil / Criminal Litigation",
                        "pattern": r"(civil court|criminal proceedings|prosecute|appropriate forum|costs and consequences|without further reference)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Missing standard legal consequence clause notifying of impending civil litigation or criminal prosecution."
                    },
                    {
                        "id": "dispatch_mode",
                        "title": "Mode of Service (RPAD / Speed Post)",
                        "pattern": r"(rpad|registered post|speed post|acknowledgement due|electronic transmission|email)",
                        "importance": "MEDIUM",
                        "deduction": 10,
                        "failure_msg": "Recommended to specify service via 'Registered Post with Acknowledgement Due (RPAD)' to prove receipt in court."
                    }
                ]
            },
            "police_complaint": {
                "name": "Police Complaint / Application for FIR (Sec 173 BNSS / Sec 154 CrPC)",
                "keywords": ["station house officer", "sho", "police station", "complaint", "fir", "first information report", "bns", "ipc", "incident"],
                "mandatory_elements": [
                    {
                        "id": "jurisdiction_ps",
                        "title": "Jurisdiction & Police Station Addressee",
                        "pattern": r"(station house officer|sho|police station|cyber crime police|commissioner of police)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Must be formally addressed to the 'Station House Officer' of the relevant local or Cyber Crime Police Station."
                    },
                    {
                        "id": "incident_time_place",
                        "title": "Exact Date, Time & Place of Occurrence",
                        "pattern": r"(date|time|place|location|at about|occurred at|hyderabad|telangana|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Must specify the exact date, time, and physical/online location where the offence took place."
                    },
                    {
                        "id": "accused_details",
                        "title": "Accused Particulars (Known or Unknown)",
                        "pattern": r"(accused|suspect|perpetrator|person named|unknown person|mobile number|upi id|bank account)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Missing names, physical descriptions, phone numbers, or digital IDs (UPI/Bank) of the suspected accused."
                    },
                    {
                        "id": "statutory_provision",
                        "title": "Invocation of BNS 2023 or BNSS Provisions",
                        "pattern": r"(section\s+\d+|bns|bnss|it act|ipc|crpc|cognizable)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Recommend citing specific penal sections (e.g. Section 318 BNS for cheating, Section 173 BNSS for FIR registration)."
                    },
                    {
                        "id": "prayer_for_fir",
                        "title": "Formal Prayer Requesting Registration of FIR",
                        "pattern": r"(register fir|register an fir|take strict action|investigate|book the accused|appropriate legal action)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Missing the operative prayer requesting the SHO to 'Register an FIR under Section 173 BNSS and investigate'."
                    },
                    {
                        "id": "signature_verification",
                        "title": "Verification & Complainant Signature",
                        "pattern": r"(yours faithfully|sincerely|complainant|signature|phone|mobile|contact)",
                        "importance": "MEDIUM",
                        "deduction": 10,
                        "failure_msg": "Must contain complainant's full signature, verified contact number, and present residential address."
                    }
                ]
            },
            "tenancy_agreement": {
                "name": "Residential Tenancy / Lease Agreement",
                "keywords": ["tenancy agreement", "lease deed", "landlord", "tenant", "monthly rent", "security deposit", "premises", "11 months"],
                "mandatory_elements": [
                    {
                        "id": "property_description",
                        "title": "Detailed Description of Premises",
                        "pattern": r"(flat no|house no|plot|situated at|schedule|premises|bearing)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Property schedule must specify exact door number, floor, building name, boundaries, and fixtures."
                    },
                    {
                        "id": "deposit_and_rent",
                        "title": "Quantified Monthly Rent & Refundable Deposit Terms",
                        "pattern": r"(monthly rent|security deposit|advance|payable on or before|refundable)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Must specify monthly rent due date, payment mode, and refundable security deposit amount."
                    },
                    {
                        "id": "deposit_refund_timeline",
                        "title": "Deposit Refund Timeline (Model Tenancy Act Compliance)",
                        "pattern": r"(refunded within|refund of deposit|deduction for damages|30 days)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Must explicitly mandate refund of deposit within 30 days of vacating, subject only to verified damages."
                    },
                    {
                        "id": "notice_period",
                        "title": "Reciprocal Termination Notice Period",
                        "pattern": r"(\d+\s*months?\s*notice|\d+\s*days?\s*notice|prior notice)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Termination notice period must be reciprocal (e.g. 1 month on either side) to prevent unilateral eviction."
                    },
                    {
                        "id": "stamp_duty_witnesses",
                        "title": "Execution, Stamp Duty & Attestation by Witnesses",
                        "pattern": r"(in witness whereof|witness 1|witness 2|signed by lessor|signed by lessee)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Lease deeds require signatures of Lessor, Lessee, and two independent adult witnesses."
                    }
                ]
            },
            "employment_contract": {
                "name": "Employment Agreement / Offer Letter",
                "keywords": ["employment agreement", "appointment letter", "employer", "employee", "ctc", "salary", "probation", "designation"],
                "mandatory_elements": [
                    {
                        "id": "role_compensation",
                        "title": "Designation, Scope of Work & CTC Breakdown",
                        "pattern": r"(designation|role|salary|ctc|remuneration|probation|allowance)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Must state job title, working hours, probation period, and detailed salary components."
                    },
                    {
                        "id": "termination_clause",
                        "title": "Reciprocal Termination & Notice Period Clause",
                        "pattern": r"(notice period|termination|severance|pay in lieu of notice)",
                        "importance": "CRITICAL",
                        "deduction": 20,
                        "failure_msg": "Must provide reasonable, reciprocal notice period (e.g. 30 or 60 days) or salary in lieu of notice."
                    },
                    {
                        "id": "void_non_compete_check",
                        "title": "Check for Void Post-Employment Non-Compete (Sec 27 Contract Act)",
                        "pattern": r"(non[- ]compete|shall not work for any competitor|restraint of trade)",
                        "importance": "HIGH",
                        "deduction": 15,
                        "failure_msg": "Contains illegal post-termination non-compete clause, which is void ab initio under Section 27 of Indian Contract Act."
                    }
                ]
            }
        }

    def verify_document(self, doc_text: str, declared_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Performs a full statutory and structural verification audit of a legal document.
        Calculates accuracy score, highlights missing mandatory elements, and checks statutory citations.
        """
        if not doc_text or len(doc_text.strip()) < 20:
            return {
                "status": "error",
                "message": "Document text is too brief or empty. Please upload or paste a substantive legal document."
            }

        text_lower = doc_text.lower()

        # Step 1: Detect Document Type if not explicitly provided
        matched_type_key = declared_type if declared_type in self.doc_type_rules else None
        if not matched_type_key:
            max_kw_count = 0
            matched_type_key = "legal_notice" # default fallback
            for type_key, type_rule in self.doc_type_rules.items():
                count = sum(1 for kw in type_rule["keywords"] if kw in text_lower)
                if count > max_kw_count:
                    max_kw_count = count
                    matched_type_key = type_key

        rule_set = self.doc_type_rules[matched_type_key]

        # Step 2: Evaluate Mandatory Elements
        passed_elements = []
        missing_elements = []
        total_deductions = 0

        for elem in rule_set["mandatory_elements"]:
            has_match = bool(re.search(elem["pattern"], text_lower))
            
            # Special check for employment non-compete (it is bad if present!)
            if elem["id"] == "void_non_compete_check":
                if has_match:
                    total_deductions += elem["deduction"]
                    missing_elements.append({
                        "id": elem["id"],
                        "title": "ILLEGAL TRAP: Post-Employment Non-Compete Covenant Found",
                        "importance": "CRITICAL",
                        "issue": elem["failure_msg"],
                        "remedy": "Delete this covenant. In India, post-employment non-competes are void under Section 27 Contract Act."
                    })
                else:
                    passed_elements.append({
                        "id": elem["id"],
                        "title": "Clean of Illegal Post-Employment Non-Competes (Sec 27 Compliant)",
                        "status": "VERIFIED"
                    })
                continue

            if has_match:
                passed_elements.append({
                    "id": elem["id"],
                    "title": elem["title"],
                    "status": "VERIFIED"
                })
            else:
                total_deductions += elem["deduction"]
                missing_elements.append({
                    "id": elem["id"],
                    "title": elem["title"],
                    "importance": elem["importance"],
                    "issue": elem["failure_msg"],
                    "remedy": f"Insert formal clause covering: {elem['title']}."
                })

        # Step 3: Check Statutory Citation Accuracy (BNS 2023 vs IPC 1860)
        citations_found = []
        citation_warnings = []

        # Check for legacy IPC citations
        ipc_matches = re.findall(r'(section\s+\d+|sec\.?\s+\d+)\s*(of\s*)?(ipc|indian penal code)', text_lower)
        for m in ipc_matches:
            citations_found.append(f"{m[0].upper()} Indian Penal Code (Legacy 1860)")
            citation_warnings.append(
                f"Document cites legacy IPC ({m[0].upper()}). Recommended to update or co-cite Bharatiya Nyaya Sanhita (BNS 2023) for current filings."
            )

        # Check for BNS citations
        bns_matches = re.findall(r'(section\s+\d+|sec\.?\s+\d+)\s*(of\s*)?(bns|bharatiya nyaya sanhita)', text_lower)
        for m in bns_matches:
            citations_found.append(f"{m[0].upper()} Bharatiya Nyaya Sanhita, 2023")

        # Check for BNSS citations
        bnss_matches = re.findall(r'(section\s+\d+|sec\.?\s+\d+)\s*(of\s*)?(bnss|bharatiya nagarik suraksha)', text_lower)
        for m in bnss_matches:
            citations_found.append(f"{m[0].upper()} Bharatiya Nagarik Suraksha Sanhita, 2023")

        # Step 4: Calculate Overall Legal Accuracy & Court Readiness Score
        accuracy_score = max(15, min(100, 100 - total_deductions))

        if accuracy_score >= 85:
            court_readiness = "Court-Admissible / High Accuracy"
            badge_color = "green"
            verdict_text = "The document satisfies standard Indian court formatting and contains mandatory statutory ingredients."
        elif accuracy_score >= 60:
            court_readiness = "Needs Minor Fortification / Moderate Accuracy"
            badge_color = "gold"
            verdict_text = "The document has core facts but lacks critical statutory clauses (notice window, specific relief, or BNS citations)."
        else:
            court_readiness = "Defective / High Risk of Dismissal"
            badge_color = "red"
            verdict_text = "The document misses fundamental legal requirements. Opposite parties or courts may reject it on technical grounds."

        # Step 5: Generate Recommended Corrected Boilerplate Clauses
        recommendations = []
        for miss in missing_elements:
            recommendations.append(f"Add {miss['title']}: {miss['issue']}")

        return {
            "status": "success",
            "document_type": rule_set["name"],
            "type_key": matched_type_key,
            "accuracy_score": accuracy_score,
            "court_readiness": court_readiness,
            "badge_color": badge_color,
            "verdict_summary": verdict_text,
            "word_count": len(doc_text.split()),
            "passed_elements_count": len(passed_elements),
            "missing_elements_count": len(missing_elements),
            "passed_elements": passed_elements,
            "missing_elements": missing_elements,
            "statutory_citations_found": citations_found,
            "citation_warnings": citation_warnings,
            "actionable_corrections": recommendations
        }
