"""
NyayaSetu AI - Legal Grievance Triage & BNS / IPC Section Mapping Engine
Analyzes citizen legal disputes, maps relevant statutory provisions under Bharatiya Nyaya Sanhita (BNS 2023),
legacy IPC, Consumer Protection Act 2019, IT Act 2000, and Labor Laws, and outputs actionable legal relief paths.
"""

import re
from typing import Dict, List, Any, Optional

class LegalTriageEngine:
    def __init__(self):
        # Comprehensive Indian Legal Taxonomy & Precedent Knowledge
        self.legal_categories = {
            "cyber_crime": {
                "name": "Cybercrime & Financial Fraud",
                "keywords": ["upi", "bank", "scam", "phishing", "otp", "hacked", "stolen", "online", "fraud", "cyber", "telegram", "crypto", "sim swap", "blackmail"],
                "statutes": [
                    {
                        "act": "Information Technology Act, 2000",
                        "section": "Section 66D",
                        "title": "Cheating by Personation using Computer Resource",
                        "penalty": "Imprisonment up to 3 years and fine up to Rs. 1 Lakh."
                    },
                    {
                        "act": "Information Technology Act, 2000",
                        "section": "Section 43 & 66",
                        "title": "Hacking & Unauthorized Data Access",
                        "penalty": "Compensation to victim and imprisonment up to 3 years."
                    },
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 318(4)",
                        "legacy_ipc": "Section 420 IPC",
                        "title": "Cheating and dishonestly inducing delivery of property",
                        "penalty": "Imprisonment up to 7 years with fine."
                    }
                ],
                "authority": "National Cybercrime Reporting Portal (cybercrime.gov.in) & Local Cyber Crime Cell",
                "helpline": "1930 (Cyber Financial Fraud Helpline)",
                "urgency": "CRITICAL",
                "golden_hour_window": "Report within 2 to 4 hours to freeze disputed funds in recipient bank accounts.",
                "evidence_checklist": [
                    "Bank transaction statement with UTR / Reference ID",
                    "Screenshot of fraudulent payment gateway or SMS debit alerts",
                    "WhatsApp / Telegram chat transcripts with fraudster",
                    "Mobile number and UPI ID of recipient"
                ]
            },

            "consumer_dispute": {
                "name": "Consumer Rights & Defective Goods/Services",
                "keywords": ["defective", "refund", "warranty", "seller", "amazon", "flipkart", "damaged", "repair", "shopkeeper", "product", "e-commerce", "service deficiency", "replacement"],
                "statutes": [
                    {
                        "act": "Consumer Protection Act, 2019",
                        "section": "Section 2(11) & 2(47)",
                        "title": "Deficiency in Service & Unfair Trade Practice",
                        "penalty": "Direct refund with interest, punitive damages, and replacement of goods."
                    },
                    {
                        "act": "Consumer Protection Act, 2019",
                        "section": "Section 35",
                        "title": "Institution of Complaint before District Consumer Commission",
                        "penalty": "Jurisdiction up to Rs. 50 Lakhs at district level."
                    },
                    {
                        "act": "Consumer Protection Act, 2019",
                        "section": "Section 84 - 86",
                        "title": "Product Liability of Manufacturer / Seller",
                        "penalty": "Compensation for harm, defect, or financial injury caused."
                    }
                ],
                "authority": "District Consumer Disputes Redressal Commission (DCDRC) & e-Daakhil Portal",
                "helpline": "1915 (National Consumer Helpline - NCH)",
                "urgency": "MEDIUM",
                "golden_hour_window": "Serve formal 15-day statutory legal notice prior to initiating District Consumer Forum litigation.",
                "evidence_checklist": [
                    "Tax Invoice / Purchase receipt with GST number",
                    "Warranty card and service technician job sheets",
                    "Email communications and customer support ticket numbers",
                    "Photographs / video proof of product defect or non-functionality"
                ]
            },

            "tenancy_dispute": {
                "name": "Landlord-Tenant & Real Estate Disputes",
                "keywords": ["landlord", "tenant", "rent", "deposit", "security deposit", "eviction", "room", "flat", "lease", "owner", "lock", "water cutoff", "electricity cutoff"],
                "statutes": [
                    {
                        "act": "Model Tenancy Act / State Rent Control Act",
                        "section": "Security Deposit Refund Clause",
                        "title": "Mandatory Refund of Security Deposit upon Vacating Premises",
                        "penalty": "Interest penalty on delayed refund and prohibition of arbitrary deductions."
                    },
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 329(1)",
                        "legacy_ipc": "Section 441 & 448 IPC",
                        "title": "Criminal Trespass & Illegal Dispossession",
                        "penalty": "Imprisonment up to 1 year and fine. Landlord cannot lock premises without due process."
                    },
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 126",
                        "legacy_ipc": "Section 339 & 341 IPC",
                        "title": "Wrongful Restraint (Disconnecting Essential Utilities)",
                        "penalty": "Imprisonment up to 1 month and fine. Cutting water/power is an actionable offense."
                    }
                ],
                "authority": "Rent Court / Rent Tribunal & Local Civil Court / Police Station",
                "helpline": "112 (Emergency Assistance if physically locked out)",
                "urgency": "HIGH",
                "golden_hour_window": "Issue formal Legal Demand Notice demanding immediate return of deposit within 15 days.",
                "evidence_checklist": [
                    "Registered Rental Agreement / Lease Deed",
                    "Bank transfer records for monthly rent and initial security deposit",
                    "WhatsApp / Email notice given for vacating premises",
                    "Handover inspection photos confirming property was returned undamaged"
                ]
            },

            "labor_dispute": {
                "name": "Labor Law, Unlawful Termination & Salary Withholding",
                "keywords": ["salary", "fired", "terminated", "severance", "employer", "company", "boss", "notice period", "resignation", "wages", "overtime", "pf", "provident fund", "gratuity"],
                "statutes": [
                    {
                        "act": "Industrial Disputes Act, 1947",
                        "section": "Section 25F",
                        "title": "Conditions Precedent to Retrenchment of Workmen",
                        "penalty": "Mandatory 1 month notice or wages in lieu thereof + 15 days severance compensation per year."
                    },
                    {
                        "act": "Payment of Wages Act, 1936",
                        "section": "Section 15",
                        "title": "Claims arising out of deductions from wages or delay in payment",
                        "penalty": "Direction to pay unpaid wages plus compensation up to 10 times the amount deducted."
                    },
                    {
                        "act": "Payment of Gratuity Act, 1972",
                        "section": "Section 4 & 7",
                        "title": "Payment of Gratuity to Employee with 5+ Years Service",
                        "penalty": "Compound interest on delayed payment + penal imprisonment for defaulting employer."
                    }
                ],
                "authority": "Office of the Labor Commissioner & Industrial Tribunal / Samadhan Portal",
                "helpline": "1800-180-1111 (Ministry of Labour & Employment)",
                "urgency": "HIGH",
                "golden_hour_window": "Submit formal conciliation petition before Deputy Labor Commissioner within 90 days.",
                "evidence_checklist": [
                    "Employment Offer Letter and Employment Agreement",
                    "Monthly salary slips and bank account statements showing credit history",
                    "Termination letter or email communication",
                    "PF UAN number and Form 16 / Tax deduction records"
                ]
            },

            "criminal_harassment": {
                "name": "Criminal Harassment, Assault, Theft & Domestic Disputes",
                "keywords": ["theft", "stolen", "assault", "beat", "hit", "threat", "harass", "abusive", "blackmail", "domestic violence", "husband", "in-laws", "fight", "police", "fir"],
                "statutes": [
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 303(2)",
                        "legacy_ipc": "Section 379 IPC",
                        "title": "Punishment for Theft",
                        "penalty": "Imprisonment up to 3 years, or fine, or both. Cognizable and Non-Bailable."
                    },
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 351",
                        "legacy_ipc": "Section 506 IPC",
                        "title": "Criminal Intimidation",
                        "penalty": "Imprisonment up to 2 years, or fine, or both. If threat is grievous harm, up to 7 years."
                    },
                    {
                        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
                        "section": "Section 115(2)",
                        "legacy_ipc": "Section 323 IPC",
                        "title": "Voluntarily Causing Hurt",
                        "penalty": "Imprisonment up to 1 year, or fine up to Rs. 10,000, or both."
                    },
                    {
                        "act": "Protection of Women from Domestic Violence Act, 2005",
                        "section": "Section 12, 18, 19",
                        "title": "Protection Orders, Right to Reside & Maintenance",
                        "penalty": "Prohibits abuser from committing acts of domestic violence, guarantees residence rights."
                    }
                ],
                "authority": "Local Police Station (Jurisdictional SHO) & Judicial Magistrate First Class (JMFC)",
                "helpline": "112 (National Emergency), 1091 (Women's Helpline), 181 (Domestic Abuse)",
                "urgency": "CRITICAL",
                "golden_hour_window": "File immediate Zero FIR at nearest police station. Mandatory registration under Sec 173 BNSS.",
                "evidence_checklist": [
                    "Medical MLC (Medico-Legal Certificate) from government hospital if injured",
                    "Audio recordings, CCTV footage, or call records of threats",
                    "Names and contact details of eyewitnesses",
                    "Photographs of property damage or physical injuries"
                ]
            }
        }

    def analyze_grievance(self, citizen_text: str, user_location: str = "Telangana") -> Dict[str, Any]:
        """
        Parses a plain-language citizen grievance, matches legal categories,
        extracts statutory sections, and builds an actionable relief roadmap.
        """
        text_lower = citizen_text.lower()
        matched_cat_key = "consumer_dispute" # Default fallback
        max_matches = 0

        # Score matching keywords
        for cat_key, cat_data in self.legal_categories.items():
            matches = sum(1 for kw in cat_data["keywords"] if re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
            if matches > max_matches:
                max_matches = matches
                matched_cat_key = cat_key

        cat = self.legal_categories[matched_cat_key]

        # Generate custom citizen guidance roadmap
        action_plan = self._generate_action_plan(matched_cat_key, citizen_text, user_location)

        return {
            "status": "success",
            "category_key": matched_cat_key,
            "category_name": cat["name"],
            "urgency": cat["urgency"],
            "primary_authority": cat["authority"],
            "helpline": cat["helpline"],
            "golden_hour_window": cat["golden_hour_window"],
            "applicable_statutes": cat["statutes"],
            "evidence_checklist": cat["evidence_checklist"],
            "action_plan": action_plan,
            "legal_aid_eligibility": {
                "eligible": True,
                "scheme": "Legal Services Authorities Act, 1987 (NALSA / TALSA)",
                "provision": "Article 39A of Constitution of India (Free Legal Aid)",
                "contact": "Telangana State Legal Services Authority (Nyaya Seva Sadan, Hyderabad) / Toll Free 15100"
            }
        }

    def _generate_action_plan(self, cat_key: str, text: str, location: str) -> List[Dict[str, str]]:
        if cat_key == "cyber_crime":
            return [
                {
                    "step": "Step 1: Immediate Financial Freeze (Within 2 Hours)",
                    "action": "Call national helpline 1930 immediately or log in to cybercrime.gov.in. Provide your bank account number, UTR number, and recipient UPI ID. The nodal officer will freeze the recipient wallet/account under RBI guidelines."
                },
                {
                    "step": "Step 2: Bank Fraud Dispute Notice",
                    "action": "Submit formal unauthorized transaction dispute form to your home bank branch within 72 hours under RBI Circular on Zero Customer Liability (RBI/2017-18/15)."
                },
                {
                    "step": "Step 3: Formal Police FIR Registration",
                    "action": "File formal complaint at your local Cyber Crime Police Station under Section 66D IT Act and Section 318(4) BNS 2023."
                }
            ]
        elif cat_key == "tenancy_dispute":
            return [
                {
                    "step": "Step 1: Formal Statutory Legal Notice (15-Day Demand)",
                    "action": "Send a formal written Legal Demand Notice via Registered Post AD and WhatsApp demanding full refund of security deposit within 15 days."
                },
                {
                    "step": "Step 2: Police Intervention for Lockout or Threat",
                    "action": "If landlord has locked your belongings or disconnected power/water, call 112 immediately. Inform SHO that wrongful restraint under Section 126 BNS and criminal trespass under Section 329 BNS has occurred."
                },
                {
                    "step": "Step 3: Rent Tribunal / Civil Summary Suit",
                    "action": "If deposit is not refunded, file an application before the Rent Controller / Civil Court under Order 37 CPC for summary recovery of money with interest."
                }
            ]
        elif cat_key == "consumer_dispute":
            return [
                {
                    "step": "Step 1: Formal Grievance to NCH & Company Nodal Officer",
                    "action": "Register grievance on National Consumer Helpline (NCH App / Portal or call 1915). Quote order ID, invoice, and defect photos."
                },
                {
                    "step": "Step 2: Issue 15-Day Pre-Litigation Legal Notice",
                    "action": "Serve a formal legal notice demanding replacement or full refund with compensation for mental agony within 15 days under Consumer Protection Act 2019."
                },
                {
                    "step": "Step 3: Online e-Daakhil Consumer Court Filing",
                    "action": "File an online consumer complaint on edaakhil.nic.in before your District Consumer Disputes Redressal Commission without needing an expensive advocate."
                }
            ]
        elif cat_key == "labor_dispute":
            return [
                {
                    "step": "Step 1: Written Demand to HR / Management",
                    "action": "Send formal email to Managing Director and HR stating non-payment of salary and illegal termination under Section 25F of Industrial Disputes Act."
                },
                {
                    "step": "Step 2: Conciliation Petition to Labor Commissioner",
                    "action": f"File a formal dispute petition before the Deputy Labor Commissioner / Conciliation Officer in {location} under the Industrial Disputes Act 1947."
                },
                {
                    "step": "Step 3: Recovery Citation via Revenue Department",
                    "action": "If conciliation fails, obtain an official Recovery Certificate from the Labor Court to attach company bank accounts."
                }
            ]
        else: # criminal_harassment
            return [
                {
                    "step": "Step 1: Immediate Safety & 112 Dispatch",
                    "action": "Call 112 emergency services immediately if under active physical threat. Women can call 1091 for priority emergency patrol response."
                },
                {
                    "step": "Step 2: Medical Examination (MLC)",
                    "action": "If physical assault occurred, report to government hospital casualty for mandatory Medico-Legal Examination (MLC) prior to police filing."
                },
                {
                    "step": "Step 3: Zero FIR Registration",
                    "action": "Lodge an FIR under Section 173 BNSS (Bharatiya Nagarik Suraksha Sanhita). Under Indian law, police CANNOT refuse to register a Zero FIR regardless of territorial jurisdiction."
                }
            ]
