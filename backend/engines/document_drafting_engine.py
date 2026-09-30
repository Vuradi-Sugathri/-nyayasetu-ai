"""
NyayaSetu AI - Automated Legal Document & Notice Drafting Engine
Generates court-ready, formal legal notices, police complaints (FIR applications),
Consumer Forum petitions, and RTI applications with accurate Indian legal syntax.
"""

import datetime
from typing import Dict, Any, Optional

class DocumentDraftingEngine:
    def __init__(self):
        pass

    def generate_legal_notice(
        self,
        sender_name: str,
        sender_address: str,
        recipient_name: str,
        recipient_address: str,
        dispute_type: str,
        dispute_facts: str,
        demand_amount: str = "50,000",
        notice_period_days: int = 15,
        location: str = "Hyderabad"
    ) -> Dict[str, Any]:
        """Generates formal Pre-Litigation Legal Demand Notice."""
        now = datetime.datetime.now().strftime("%d-%m-%Y")

        notice_text = f"""================================================================================
                               FORMAL LEGAL DEMAND NOTICE
                 (ISSUED UNDER THE PROVISIONS OF INDIAN CIVIL & STATUTORY LAW)
================================================================================

Date: {now}
Place: {location}

VIA REGISTERED POST WITH ACKNOWLEDGEMENT DUE (RPAD) & ELECTRONIC TRANSMISSION

TO,
{recipient_name}
{recipient_address}

FROM,
{sender_name}
{sender_address}

SUBJECT: LEGAL NOTICE FOR {dispute_type.upper()} AND DEMAND FOR IMMEDIATE RESOLUTION / REFUND OF RS. {demand_amount}/- WITHIN {notice_period_days} DAYS.

Sir / Madam,

Under instructions and on behalf of my client / the undersigned, {sender_name}, residing at {sender_address}, I hereby serve upon you this formal Legal Notice setting forth the following facts:

1. That my client had entered into a legal and binding transaction / agreement with you regarding {dispute_type}.

2. That the material facts giving rise to this notice are as follows:
   "{dispute_facts}"

3. That despite repeated reminders, verbal requests, and written communications, you have willfully, deliberately, and with dishonest intent failed and neglected to fulfill your statutory and contractual obligations towards my client.

4. That your aforesaid failure constitutes a serious breach of contract, deficiency in service, and illegal withholding of my client's rightful funds, causing severe financial loss, mental harassment, and agony to my client.

5. That your conduct also attracts penal consequences under the provisions of the Bharatiya Nyaya Sanhita, 2023 (BNS) / Indian Penal Code, including Section 316 (Criminal Breach of Trust) and Section 318 (Cheating).

I, THEREFORE, HEREBY CALL UPON YOU BY WAY OF THIS NOTICE to:
a) Immediately pay / refund to my client the total sum of Rs. {demand_amount}/- (Rupees {demand_amount} Only) along with interest @ 18% per annum from the due date until realization;
b) Compensate my client to the tune of Rs. 25,000/- towards mental harassment and legal expenses;
c) Comply with the aforesaid demand within a period of {notice_period_days} (Fifteen) days from the date of receipt of this notice.

PLEASE TAKE NOTE that in the event of your failure to comply with the demands set forth above within the stipulated period of {notice_period_days} days, my client has given me strict instructions to initiate appropriate Civil, Consumer, and/or Criminal proceedings against you in the competent Court of Law having jurisdiction at {location}, holding you solely liable for all consequential costs and damages arising therefrom.

A copy of this Legal Notice is retained in our records for future judicial reference.

Yours faithfully,

_____________________________
{sender_name}
(Complainant / Aggrieved Citizen)
Contact: Through NyayaSetu Citizen Legal Portal
================================================================================
"""

        return {
            "document_type": "Pre-Litigation Legal Demand Notice",
            "statutory_period": f"{notice_period_days} Days",
            "governing_law": "Indian Contract Act 1872 & Relevant Statutory Laws",
            "jurisdiction": location,
            "generated_date": now,
            "document_text": notice_text
        }

    def generate_police_complaint_fir(
        self,
        complainant_name: str,
        complainant_phone: str,
        complainant_address: str,
        police_station_name: str,
        incident_date: str,
        incident_location: str,
        accused_details: str,
        incident_description: str,
        applicable_sections: str = "Section 303, 318 BNS 2023"
    ) -> Dict[str, Any]:
        """Generates formal Police Complaint for registration of FIR under Section 173 BNSS."""
        now = datetime.datetime.now().strftime("%d-%m-%Y")

        complaint_text = f"""================================================================================
                      FORMAL POLICE COMPLAINT / APPLICATION FOR FIR
            (UNDER SECTION 173 OF BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 - BNSS)
================================================================================

Date: {now}

TO,
The Station House Officer (SHO),
Police Station: {police_station_name}

SUBJECT: WRITTEN COMPLAINT REGARDING COGNIZABLE OFFENSE COMMITTED ON {incident_date} AT {incident_location} AND PRAYER FOR REGISTRATION OF FIR UNDER {applicable_sections}.

Respected Sir / Madam,

I, the undersigned complainant, {complainant_name}, residing at {complainant_address}, holding mobile number {complainant_phone}, do hereby lodge this formal written complaint regarding the commission of cognizable criminal offenses:

1. DETAILS OF THE COMPLAINANT:
   - Full Name: {complainant_name}
   - Contact Number: {complainant_phone}
   - Residential Address: {complainant_address}

2. DETAILS OF ACCUSED / SUSPECT PERSON(S):
   - Name / Identification: {accused_details}

3. INCIDENT PARTICULARS:
   - Date & Time of Occurrence: {incident_date}
   - Place of Occurrence: {incident_location} (Within the territorial limits of this Police Station)

4. CHRONOLOGY OF FACTS & CIRCUMSTANCES:
   "{incident_description}"

5. OFFENSES COMMITTED:
   The acts committed by the accused person(s) constitute clear cognizable and non-bailable offenses under the Bharatiya Nyaya Sanhita, 2023 (BNS), including but not limited to:
   - {applicable_sections}
   - And other relevant penal provisions.

PRAYER:
In view of the above-stated facts and circumstances, it is most respectfully prayed that this Hon'ble Police Authority may be pleased to:
a) Treat this written complaint as an information disclosing cognizable offense under Section 173 of BNSS, 2023;
b) Immediately register a First Information Report (FIR) against the accused person(s);
c) Provide a certified copy of the FIR free of cost to the complainant as mandated by law;
d) Investigate the matter and take stern legal action in accordance with law.

I hereby affirm that the statements made hereinabove are true and correct to the best of my knowledge, information, and belief.

LIST OF ENCLOSURES / EVIDENCE ATTACHED:
1. Proof of Identity of Complainant (Aadhaar / Voter ID).
2. Relevant screenshots, call records, financial transaction receipts, and chat logs.

Yours sincerely,

_____________________________
{complainant_name}
(Complainant / Informant)
================================================================================
"""

        return {
            "document_type": "Formal Police Complaint (FIR Application)",
            "governing_section": "Section 173 BNSS, 2023 (Mandatory FIR Registration)",
            "police_station": police_station_name,
            "generated_date": now,
            "document_text": complaint_text
        }

    def generate_consumer_complaint(
        self,
        consumer_name: str,
        consumer_address: str,
        opposite_party_name: str,
        opposite_party_address: str,
        product_service_name: str,
        purchase_date: str,
        amount_paid: str,
        compensation_demanded: str = "25,000",
        grievance_summary: str = "",
        district_name: str = "Hyderabad"
    ) -> Dict[str, Any]:
        """Generates formal Consumer Complaint under Section 35 of Consumer Protection Act 2019."""
        now = datetime.datetime.now().strftime("%d-%m-%Y")

        consumer_text = f"""================================================================================
             BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
                              AT {district_name.upper()}
================================================================================

CONSUMER COMPLAINT NO. _________ OF {datetime.datetime.now().year}
(COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019)

IN THE MATTER OF:

{consumer_name}
{consumer_address}
... COMPLAINANT

VERSUS

{opposite_party_name}
{opposite_party_address}
... OPPOSITE PARTY / RESPONDENT

MEMO OF COMPLAINT ON BEHALF OF THE COMPLAINANT:

1. That the Complainant is a bonafide 'Consumer' within the meaning of Section 2(7) of the Consumer Protection Act, 2019, having purchased {product_service_name} on {purchase_date} from the Opposite Party against valid consideration of Rs. {amount_paid}/-.

2. That the Opposite Party is a commercial enterprise engaged in the business of selling goods and providing services to consumers for consideration.

3. BRIEF STATEMENT OF FACTS:
   "{grievance_summary}"

4. CAUSE OF ACTION & DEFICIENCY IN SERVICE:
   That the conduct of the Opposite Party amounts to 'Deficiency in Service' as defined under Section 2(11) and 'Unfair Trade Practice' under Section 2(47) of the Act. The Complainant was subjected to severe financial prejudice, harassment, and mental distress.

5. TERRITORIAL & PECUNIARY JURISDICTION:
   That the Complainant resides within the jurisdiction of this Hon'ble District Commission, and the total value of goods and compensation claimed is well within the pecuniary limit of Rs. 50,00,000/- (Fifty Lakhs) as prescribed under Section 34 of the Act.

PRAYER:
It is therefore most respectfully prayed that this Hon'ble District Commission may be graciously pleased to:
a) Direct the Opposite Party to refund the full purchase consideration of Rs. {amount_paid}/- along with interest @ 12% p.a. from the date of payment;
b) Award compensation of Rs. {compensation_demanded}/- towards mental agony, harassment, and punitive damages;
c) Award Rs. 10,000/- towards litigation expenses incurred by the Complainant;
d) Pass such further order(s) as this Hon'ble Commission may deem fit in the interest of justice.

Place: {district_name}
Date: {now}

VERIFICATION:
I, {consumer_name}, the Complainant above-named, do hereby verify that the contents of paragraphs 1 to 5 are true to my personal knowledge and belief. Verified at {district_name} on this {now}.

_____________________________
{consumer_name}
(Complainant in Person)
================================================================================
"""

        return {
            "document_type": "Consumer Forum Complaint Petition (Form-A)",
            "governing_section": "Section 35 Consumer Protection Act, 2019",
            "forum": f"District Consumer Commission ({district_name})",
            "generated_date": now,
            "document_text": consumer_text
        }
