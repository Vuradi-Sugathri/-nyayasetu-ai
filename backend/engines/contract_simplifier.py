"""
NyayaSetu AI - Legal Contract & Agreement Simplifier Engine
Deconstructs complex legalese in rental agreements, employment letters, loan terms, and service agreements.
Identifies hidden "red flag" clauses, unfair forfeiture conditions, and calculates a Contract Fairness Index.
"""

import re
from typing import Dict, List, Any

class ContractSimplifierEngine:
    def __init__(self):
        # Known Unfair / Restrictive Contract Traps under Indian Jurisprudence
        self.trap_rules = [
            {
                "id": "non_compete_restraint",
                "pattern": r"(non[- ]compete|shall not work for any competitor|restraint of trade|shall not join any rival|restrictive covenant)",
                "category": "Void Restraint of Trade Clause",
                "severity": "HIGH",
                "legal_statute": "Section 27, Indian Contract Act, 1872",
                "verdict": "UNENFORCEABLE IN INDIA: Under Indian law, post-employment non-compete agreements are strictly void and unconstitutional under Article 19(1)(g) (Niranjan Shankar Golikari v. Century Spg & Mfg Co).",
                "advice": "Employer cannot legally block you from joining another company after resignation."
            },
            {
                "id": "arbitrary_deposit_forfeiture",
                "pattern": r"(forfeit the entire deposit|deposit shall be non[- ]refundable|landlord shall retain full advance|no refund of advance|without any claim)",
                "category": "Arbitrary Deposit Forfeiture Clause",
                "severity": "CRITICAL",
                "legal_statute": "Section 73 & 74, Indian Contract Act, 1872 & Model Tenancy Act",
                "verdict": "UNLAWFUL FORFEITURE: Landlord or counter-party cannot arbitrarily forfeit full security deposit without proving actual damages or unpaid arrears.",
                "advice": "Demand clause modification to state: 'Deposit refundable within 7 days of vacating subject only to electricity/water arrears and verified physical damage'."
            },
            {
                "id": "unilateral_termination",
                "pattern": r"(terminate without any notice|terminate at sole discretion|without assigning any reason|without any severance)",
                "category": "Unilateral Termination without Cause",
                "severity": "HIGH",
                "legal_statute": "Principles of Natural Justice & Industrial Disputes Act Sec 25F",
                "verdict": "UNFAIR CONTRACT TERM: A clause giving one party unilateral right to terminate without notice or compensation is prima facie unconscionable.",
                "advice": "Insist on reciprocal notice period (e.g., minimum 30 or 60 days on either side)."
            },
            {
                "id": "usurious_penalty_interest",
                "pattern": r"(interest at 24%|interest at 36%|penalty of 2% per day|exorbitant interest|compound penalty)",
                "category": "Usurious / Punitive Interest Penalty",
                "severity": "MEDIUM",
                "legal_statute": "Section 74 Indian Contract Act & Usurious Loans Act",
                "verdict": "PUNITIVE DAMAGES VOID: Courts do not enforce penalty interest exceeding reasonable commercial rates (usually 12% to 18% p.a.).",
                "advice": "Request penalty rate to be capped at prevailing SBI MCLR + 2%."
            },
            {
                "id": "waiver_of_legal_recourse",
                "pattern": r"(waive any right to file complaint|shall not approach consumer court|jurisdiction exclusively outside india|give up right to sue)",
                "category": "Ouster of Legal Jurisdiction & Consumer Rights",
                "severity": "CRITICAL",
                "legal_statute": "Section 28, Indian Contract Act, 1872",
                "verdict": "STRICTLY VOID: Any agreement restricting a citizen from enforcing their rights in court or consumer commission is void ab initio.",
                "advice": "You cannot be stopped from approaching Consumer Commission or Civil Court regardless of this clause."
            }
        ]

    def simplify_contract(self, contract_text: str, contract_type: str = "rental_agreement") -> Dict[str, Any]:
        """Analyzes agreement text, flags hidden risks, and generates a structured plain-language summary."""
        text_lower = contract_text.lower()
        flagged_traps = []

        for rule in self.trap_rules:
            if re.search(rule["pattern"], text_lower):
                flagged_traps.append({
                    "id": rule["id"],
                    "title": rule["category"],
                    "severity": rule["severity"],
                    "statute": rule["legal_statute"],
                    "legal_verdict": rule["verdict"],
                    "citizen_advice": rule["advice"]
                })

        # Calculate Contract Fairness Score
        deductions = sum(25 if t["severity"] == "CRITICAL" else (15 if t["severity"] == "HIGH" else 8) for t in flagged_traps)
        fairness_score = max(20, min(100, 100 - deductions))

        # Extract Key Financial & Term Clauses
        notice_match = re.search(r'(\d+)\s*(days?|months?)\s*notice', text_lower)
        notice_period = notice_match.group(0) if notice_match else "30 days (Standard Default)"

        deposit_match = re.search(r'(deposit|advance)\s*(of\s*)?(rs\.?|inr)?\s*([0-9,]+)', text_lower)
        deposit_term = deposit_match.group(0) if deposit_match else "Specified in Schedule"

        plain_language_summary = [
            f"Notice Period: Required notice to terminate is {notice_period}.",
            f"Financial Commitment: Advance / security deposit recorded as {deposit_term}.",
            f"Hidden Risk Traps Detected: {len(flagged_traps)} clause(s) found that require scrutiny or modification.",
            "Legal Validity: All terms remain subject to mandatory statutory consumer, tenancy, and constitutional safeguards."
        ]

        return {
            "status": "success",
            "contract_type": contract_type,
            "fairness_score": fairness_score,
            "fairness_rating": "Fair & Balanced" if fairness_score >= 80 else ("Moderate Risk" if fairness_score >= 55 else "High Risk / Trap Clauses Detected"),
            "flagged_traps_count": len(flagged_traps),
            "flagged_traps": flagged_traps,
            "plain_language_summary": plain_language_summary,
            "recommended_amendments": [
                "Remove or strike out non-refundable deposit terms.",
                "Ensure reciprocal equal notice periods for both parties.",
                "Verify dispute resolution jurisdiction is within your home city / district."
            ]
        }
