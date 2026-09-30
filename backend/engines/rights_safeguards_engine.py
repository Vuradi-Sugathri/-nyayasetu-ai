"""
NyayaSetu AI - Citizen Rights & Statutory Safeguards Engine (Adhikar Guide)
Comprehensive knowledge of Indian Constitutional rights, arrest safeguards under BNSS/CrPC,
women's procedural protections, bail categories, and Free Legal Aid under Article 39A / NALSA.
"""

from typing import Dict, List, Any

class RightsSafeguardsEngine:
    def __init__(self):
        self.safeguard_modules = {
            "arrest_safeguards": {
                "title": "Citizen Rights during Police Detention & Arrest",
                "constitutional_basis": "Article 21 & 22 of the Constitution of India",
                "rules": [
                    {
                        "right": "Right to Know Grounds of Arrest",
                        "statute": "Section 47 BNSS 2023 / Section 50 CrPC",
                        "description": "Police officer MUST immediately inform the arrested person of the full particulars of the offense and specific grounds for arrest."
                    },
                    {
                        "right": "Right to Inform a Relative or Friend Immediately",
                        "statute": "Section 48 BNSS 2023 / Section 50A CrPC & D.K. Basu Guidelines",
                        "description": "The police station is legally bound to inform a family member, nominated friend, or advocate immediately upon detention."
                    },
                    {
                        "right": "Right to Free Government Medical Examination",
                        "statute": "Section 53 BNSS 2023 / Section 54 CrPC",
                        "description": "Arrested individual has the statutory right to be medically examined by a registered medical practitioner to document physical condition and record any custodial injuries."
                    },
                    {
                        "right": "Mandatory Production before Magistrate within 24 Hours",
                        "statute": "Article 22(2) Constitution & Section 58 BNSS / Section 57 CrPC",
                        "description": "No person can be detained in police custody beyond 24 hours without the express judicial authorization of a Magistrate."
                    },
                    {
                        "right": "Right to Consult a Lawyer during Interrogation",
                        "statute": "Section 38 BNSS 2023 / Section 41D CrPC",
                        "description": "An accused is entitled to meet an advocate of their choice throughout interrogation, though not throughout the entire interrogation."
                    }
                ]
            },

            "women_safeguards": {
                "title": "Special Procedural Protections for Women under Indian Law",
                "constitutional_basis": "Article 15(3) of Constitution of India",
                "rules": [
                    {
                        "right": "Prohibition of Arrest between Sunset and Sunrise",
                        "statute": "Section 43(5) BNSS 2023 / Section 46(4) CrPC",
                        "description": "No woman can be arrested after sunset and before sunrise except under exceptional circumstances with prior written permission from a Judicial Magistrate First Class."
                    },
                    {
                        "right": "Search and Physical Arrest by Female Officers Only",
                        "statute": "Section 43(1) BNSS 2023 / Section 46(1) CrPC",
                        "description": "A woman can only be arrested and searched by a female police officer with strict regard to decency."
                    },
                    {
                        "right": "Universal Zero FIR Filing",
                        "statute": "Ministry of Home Affairs Advisory & Section 173 BNSS",
                        "description": "A woman can register a Zero FIR at ANY police station regardless of where the incident occurred. Police cannot cite jurisdictional excuse."
                    },
                    {
                        "right": "Confidential In-Camera Statement Recording",
                        "statute": "Section 183 BNSS 2023 / Section 164(5A) CrPC",
                        "description": "Statements of sexual assault or harassment survivors must be recorded by a woman Magistrate in private chambers."
                    }
                ]
            },

            "free_legal_aid": {
                "title": "Constitutional Right to 100% Free Legal Aid (NALSA)",
                "constitutional_basis": "Article 39A (Equal Justice & Free Legal Aid)",
                "rules": [
                    {
                        "right": "Free Court Advocate & Court Fee Exemption",
                        "statute": "Legal Services Authorities Act, 1987",
                        "description": "The State provides a qualified legal aid advocate free of cost. Beneficiaries include all women, children, SC/ST citizens, industrial workmen, and citizens with annual income below statutory ceiling (Rs. 3 Lakh in Telangana)."
                    },
                    {
                        "right": "National Legal Aid Toll-Free Helpline: 15100",
                        "statute": "NALSA 24x7 Citizen Legal Hotline",
                        "description": "Any citizen can dial 15100 to connect with duty legal aid counsels at District Courts and High Courts."
                    }
                ]
            }
        }

    def get_all_safeguards(self) -> Dict[str, Any]:
        """Returns complete directory of constitutional and statutory citizen safeguards."""
        return self.safeguard_modules

    def get_safeguards_by_topic(self, topic_key: str) -> Dict[str, Any]:
        """Returns specific rights module."""
        return self.safeguard_modules.get(topic_key, self.safeguard_modules["arrest_safeguards"])
