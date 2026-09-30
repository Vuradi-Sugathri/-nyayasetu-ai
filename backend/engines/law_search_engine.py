"""
NyayaSetu AI - Indian Law Search & Citizen Legal Encyclopedia Engine (NyayaSearch)
Provides instant search and plain-language explanation of Indian Statutes across:
Bharatiya Nyaya Sanhita (BNS 2023), Bharatiya Nagarik Suraksha Sanhita (BNSS 2023),
Legacy Indian Penal Code (IPC 1860), Code of Criminal Procedure (CrPC 1973),
IT Act 2000, Consumer Protection Act 2019, Motor Vehicles Act 2019, Negotiable Instruments Act 1881,
Industrial Disputes Act 1947, Indian Contract Act 1872, and Constitution of India.
"""

import re
from typing import Dict, List, Any, Optional

class IndianLawSearchEngine:
    def __init__(self):
        # Comprehensive Citizen-Facing Indian Law Corpus
        self.laws_corpus = [
            {
                "id": "bns_318_cheating",
                "title": "Cheating & Financial Fraud",
                "section": "Section 318(4) Bharatiya Nyaya Sanhita, 2023 (BNS)",
                "legacy": "Section 420 Indian Penal Code (IPC 1860)",
                "act": "Bharatiya Nyaya Sanhita, 2023",
                "category": "Financial Crime & Cheating",
                "nature": "Cognizable, Non-Bailable, Triable by Magistrate",
                "punishment": "Imprisonment up to 7 years with fine",
                "plain_english": "Applies when someone dishonestly deceives you and induces you to deliver money, property, or valuable security (such as bank transfers, investments, or forged sales).",
                "plain_telugu": "ఎవరైనా మిమ్మల్ని మోసగించి, తప్పుడు సమాచారం ఇచ్చి మీ వద్ద నుండి డబ్బు, ఆస్తి లేదా విలువైన సెక్యూరిటీని బదిలీ చేసుకున్నప్పుడు ఈ సెక్షన్ వర్తిస్తుంది.",
                "plain_hindi": "जब कोई व्यक्ति आपको धोखा देकर आपसे धन, संपत्ति या मूल्यवान वस्तु प्राप्त करता है, तो यह धारा लागू होती है। 7 साल तक की जेल और जुर्माना।",
                "enforcement_steps": [
                    "Preserve all transaction receipts, bank statements, and chat transcripts.",
                    "If online fraud, dial 1930 immediately to freeze recipient bank account.",
                    "File police complaint under Section 173 BNSS citing Section 318(4) BNS."
                ],
                "keywords": ["cheating", "fraud", "420", "318", "money scam", "scam", "investment fraud", "deceit", "fake promise", "dhokhadhadi", "mosam"]
            },
            {
                "id": "it_act_66d_upi_cyber",
                "title": "Cybercrime, Phishing & UPI Impersonation Fraud",
                "section": "Section 66D Information Technology Act, 2000",
                "legacy": "Section 66D IT Act (Co-read with Sec 420 IPC / Sec 318 BNS)",
                "act": "Information Technology Act, 2000",
                "category": "Cybercrime & Online Fraud",
                "nature": "Cognizable, Bailable / Compoundable with court consent",
                "punishment": "Imprisonment up to 3 years and fine up to ₹1,00,000",
                "plain_english": "Applies when someone cheats by impersonating another person (e.g. pretending to be your bank manager, lottery official, or government officer) using computers, phones, or the internet.",
                "plain_telugu": "కంప్యూటర్, మొబైల్ లేదా ఇంటర్నెట్ ద్వారా బ్యాంక్ అధికారి లేదా ఇతర వ్యక్తిగా నటించి ఆన్‌లైన్ లేదా UPI మోసం చేసినప్పుడు ఈ సెక్షన్ కింద చర్యలు తీసుకుంటారు.",
                "plain_hindi": "कंप्यूटर, मोबाइल या इंटरनेट के जरिए किसी अन्य व्यक्ति या बैंक अधिकारी का भेष बनाकर ऑनलाइन या UPI धोखाधड़ी करने पर यह धारा लगती है।",
                "enforcement_steps": [
                    "Call National Cybercrime Helpline 1930 within the 'Golden Hour' (2-4 hours).",
                    "Lodge formal digital complaint at cybercrime.gov.in.",
                    "Submit transaction UTR ID to your home bank branch within 3 days for zero liability."
                ],
                "keywords": ["cyber", "upi", "online fraud", "phishing", "otp", "googlepay", "phonepe", "paytm", "sim swap", "66d", "it act", "hacked"]
            },
            {
                "id": "bns_303_theft",
                "title": "Theft & Stolen Movable Property",
                "section": "Section 303(2) Bharatiya Nyaya Sanhita, 2023 (BNS)",
                "legacy": "Section 379 Indian Penal Code (IPC 1860)",
                "act": "Bharatiya Nyaya Sanhita, 2023",
                "category": "Property Offences",
                "nature": "Cognizable, Non-Bailable",
                "punishment": "Imprisonment up to 3 years, or fine, or both",
                "plain_english": "Applies when someone dishonestly takes any movable property (laptop, mobile phone, vehicle, jewelry, cash) out of your possession without your consent.",
                "plain_telugu": "మీ అనుమతి లేకుండా మీ స్వాధీనంలో ఉన్న చరాస్తిని (ఫోన్, ల్యాప్‌టాప్, నగలు, నగదు, వాహనం) ఎవరైనా దొంగిలించినప్పుడు ఈ సెక్షన్ వర్తిస్తుంది.",
                "plain_hindi": "आपकी सहमति के बिना आपके कब्जे से कोई चल संपत्ति (मोबाइल, वाहन, आभूषण, नकदी) बेईमानी से ले जाने पर यह धारा लागू होती है।",
                "enforcement_steps": [
                    "Report immediately to nearest police station or file online Zero FIR under Sec 173 BNSS.",
                    "Provide IMEI number of phone or RC book copy of stolen vehicle.",
                    "Obtain signed FIR copy free of cost under Section 173(2) BNSS."
                ],
                "keywords": ["theft", "stolen", "379", "303", "robbery", "chori", "dongathanam", "mobile theft", "bike theft"]
            },
            {
                "id": "ni_act_138_cheque_bounce",
                "title": "Cheque Bounce (Dishonour for Insufficient Funds)",
                "section": "Section 138 Negotiable Instruments Act, 1881",
                "legacy": "Section 138 NI Act",
                "act": "Negotiable Instruments Act, 1881",
                "category": "Commercial & Banking Disputes",
                "nature": "Non-Cognizable, Bailable, Compoundable",
                "punishment": "Imprisonment up to 2 years, or fine up to TWICE the cheque amount, or both",
                "plain_english": "If a cheque issued towards a legally enforceable debt bounces due to insufficient funds, the payee must issue a statutory Demand Notice within 30 days giving 15 days to pay.",
                "plain_telugu": "చట్టబద్ధమైన బాకీ కోసం ఇచ్చిన చెక్ నిధులు లేక బౌన్స్ అయినప్పుడు, 30 రోజులలోపు 15 రోజుల గడువుతో లీగల్ నోటీసు పంపాలి. చెల్లించకపోతే రెట్టింపు జరిమానా, 2 ఏళ్ల జైలు శిక్ష విధించబడుతుంది.",
                "plain_hindi": "पर्याप्त धनराशि न होने के कारण चेक बाउंस होने पर 30 दिनों के भीतर 15 दिन का कानूनी नोटिस भेजना अनिवार्य है। 2 वर्ष की जेल या चेक राशि का दोगुना जुर्माना।",
                "enforcement_steps": [
                    "Collect original Cheque Return Memo from your bank.",
                    "Serve formal Section 138 Statutory Legal Demand Notice within 30 days via RPAD.",
                    "If payment not made in 15 days, file criminal complaint before Judicial Magistrate within 30 days."
                ],
                "keywords": ["cheque bounce", "check bounce", "138", "ni act", "insufficient funds", "dishonour", "bank memo"]
            },
            {
                "id": "contract_act_27_non_compete",
                "title": "Unlawful Employment Non-Compete Clauses (Restraint of Trade)",
                "section": "Section 27 Indian Contract Act, 1872",
                "legacy": "Section 27 Indian Contract Act (Niranjan Shankar Golikari Precedent)",
                "act": "Indian Contract Act, 1872",
                "category": "Employment & Labor Rights",
                "nature": "Civil Law — Void Ab Initio (Unenforceable in India)",
                "punishment": "Clause is legally invalid; Courts will not enforce it against employee",
                "plain_english": "Any agreement restraining a person from exercising a lawful profession, trade, or business is 100% void in India. An employer cannot legally prevent you from joining a competitor post-resignation.",
                "plain_telugu": "భారత కాంట్రాక్ట్ చట్టం ప్రకారం రాజీనామా తర్వాత ఉద్యోగి పోటీ సంస్థలో చేరకుండా నిరోధించే ఎటువంటి నాన్-కాంపీట్ నిబంధన అయినా పూర్తిగా చట్టవిరుద్ధం మరియు చెల్లదు.",
                "plain_hindi": "भारतीय कानून के तहत नौकरी छोड़ने के बाद कर्मचारी को किसी अन्य प्रतिस्पर्धी कंपनी में काम करने से रोकने वाली कोई भी शर्त पूर्णतः अवैध और शून्य (Void) है।",
                "enforcement_steps": [
                    "Employees cannot be sued for joining competitors in normal commercial IT/corporate roles.",
                    "If company withholds experience letter or salary, send formal Legal Notice citing Section 27.",
                    "Approach Labor Commissioner or civil court for recovery of withheld dues."
                ],
                "keywords": ["non compete", "non-compete", "job bond", "employment contract", "service agreement", "resignation", "section 27", "restraint of trade"]
            },
            {
                "id": "consumer_act_35_deficiency",
                "title": "Consumer Rights, Deficiency in Service & E-Commerce Frauds",
                "section": "Section 2(11), 2(47) & Section 35 Consumer Protection Act, 2019",
                "legacy": "Consumer Protection Act 1986",
                "act": "Consumer Protection Act, 2019",
                "category": "Consumer Protection",
                "nature": "Civil / Statutory Redressal Commission",
                "punishment": "Full refund with 9-18% interest, punitive damages for mental agony, and replacement",
                "plain_english": "Protects buyers against defective products, unfair trade practices, false advertising, non-refunds, and service deficiencies by sellers, airlines, builders, hospitals, or e-commerce apps.",
                "plain_telugu": "లోపభూయిష్ట వస్తువులు, నాసిరకం సేవలు, రిఫండ్ ఇవ్వకపోవడం లేదా తప్పుడు ప్రకటనలపై వినియోగదారుల ఫోరంలో నేరుగా పరిహారం మరియు రీఫండ్ కోసం ఫిర్యాదు చేయవచ్చు.",
                "plain_hindi": "दोषपूर्ण सामान, अनुचित सेवा, रिफंड न देने या झूठे विज्ञापनों के खिलाफ उपभोक्ता फोरम में पूरा रिफंड और मानसिक प्रताड़ना का मुआवजा मिलता है।",
                "enforcement_steps": [
                    "Send formal Pre-Litigation Legal Notice to seller/company giving 15 days to refund.",
                    "If unresolved, file e-Daakhil consumer complaint online (edaakhil.nic.in).",
                    "Claim full refund + interest + litigation costs before District Consumer Commission."
                ],
                "keywords": ["consumer", "defective", "refund", "flipkart", "amazon", "e-commerce", "deficiency", "warranty", "consumer court", "edaakhil"]
            },
            {
                "id": "tenancy_deposit_forfeiture",
                "title": "Rental Security Deposit Non-Refund & Illegal Eviction",
                "section": "Section 73 & 74 Indian Contract Act & Model Tenancy Act",
                "legacy": "Sections 73/74 Contract Act & Sec 126 BNS (Wrongful Restraint / Sec 341 IPC)",
                "act": "Indian Contract Act & State Rent Control Acts",
                "category": "Housing & Tenancy Rights",
                "nature": "Civil Recovery & Criminal Trespass if locked out",
                "punishment": "Full refund of deposit with statutory interest; damages for harassment",
                "plain_english": "Landlords cannot arbitrarily forfeit your full security deposit. Deductions are only permissible for verified physical damages or unpaid utility bills. Deposit must be refunded within 30 days.",
                "plain_telugu": "ఇంటి యజమానులు అద్దె డిపాజిట్‌ను అకారణంగా జప్తు చేయడం చట్టవిరుద్ధం. కేవలం వాస్తవ నష్టాలు లేదా కరెంట్ బిల్లులకే మినహాయింపులు ఉంటాయి. 30 రోజులలోపు డిపాజిట్ తిరిగి ఇవ్వాలి.",
                "plain_hindi": "मकान मालिक आपकी सुरक्षा जमा राशि को मनमाने ढंग से जब्त नहीं कर सकता। वास्तविक टूट-फूट के अलावा पूरी राशि 30 दिनों के भीतर वापस करनी होती है।",
                "enforcement_steps": [
                    "Provide 30 days prior written notice of vacating via email/WhatsApp.",
                    "Take photos/video walkthrough of flat condition upon peaceful handover.",
                    "Serve formal 15-day Legal Demand Notice demanding deposit refund with 18% interest."
                ],
                "keywords": ["rent", "tenant", "landlord", "security deposit", "deposit refund", "eviction", "kiraya", "badige", "flat deposit", "house rent"]
            },
            {
                "id": "bnss_43_women_arrest",
                "title": "Prohibition of Arrest of Women After Sunset (Female Safeguard)",
                "section": "Section 43(5) Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
                "legacy": "Section 46(4) Code of Criminal Procedure (CrPC 1973)",
                "act": "Bharatiya Nagarik Suraksha Sanhita, 2023",
                "category": "Arrest Safeguards & Women Rights",
                "nature": "Mandatory Statutory Injunction on Police",
                "punishment": "Disciplinary action and contempt against offending police officer",
                "plain_english": "No woman can be arrested after sunset and before sunrise except in extraordinary circumstances, and ONLY with prior written permission of a Judicial Magistrate First Class.",
                "plain_telugu": "సూర్యాస్తమయం తర్వాత మరియు సూర్యోదయానికి ముందు ఎట్టి పరిస్థితుల్లోనూ మహిళలను అరెస్ట్ చేయడానికి వీల్లేదు. అత్యవసరమైతే జ్యుడీషియల్ మేజిస్ట్రేట్ ముందస్తు లిఖితపూర్వక అనుమతి తప్పనిసరి.",
                "plain_hindi": "सूर्यास्त के बाद और सूर्योदय से पहले किसी भी महिला को गिरफ्तार नहीं किया जा सकता, सिवाय असाधारण परिस्थितियों में और न्यायिक मजिस्ट्रेट की पूर्व लिखित अनुमति से।",
                "enforcement_steps": [
                    "A woman can only be arrested by a female police officer.",
                    "If detained at night without magistrate warrant, immediately dial 112 or Women Helpline 1091.",
                    "Inform legal counsel to file habeas corpus petition before High Court."
                ],
                "keywords": ["women arrest", "sunset", "female rights", "mahila", "arrest at night", "section 43", "46(4)", "lady arrest"]
            },
            {
                "id": "const_39a_free_legal_aid",
                "title": "Article 39A — Right to Free Legal Aid & Government Advocate",
                "section": "Article 39A Constitution of India & Legal Services Authorities Act, 1987",
                "legacy": "Article 39A Constitution of India",
                "act": "Constitution of India",
                "category": "Constitutional Rights & Justice",
                "nature": "Constitutional Fundamental Directive",
                "punishment": "State must provide advocate free of charge to eligible citizens",
                "plain_english": "Guarantees free legal representation to economically weaker citizens, women, children, SC/ST, custody undertrials, and disaster victims through NALSA, TALSA, and DLSA.",
                "plain_telugu": "ఆర్థికంగా వెనుకబడిన పౌరులు, మహిళలు, ఎస్సీ/ఎస్టీ మరియు బాధితులకు NALSA/TALSA ద్వారా ప్రభుత్వం పూర్తి ఉచితంగా న్యాయవాదిని సమకూర్చుతుంది. ఉచిత హెల్ప్‌లైన్: 15100.",
                "plain_hindi": "आर्थिक रूप से कमजोर नागरिकों, महिलाओं, बच्चों और पीड़ितों को सरकार की तरफ से निःशुल्क वकील और कानूनी सहायता प्रदान की जाती है। टोल-फ्री हेल्पलाइन: 15100.",
                "enforcement_steps": [
                    "Dial National Free Legal Aid Helpline 15100 (24x7 Toll-Free).",
                    "Visit District Legal Services Authority (DLSA) at your local court complex.",
                    "Submit application form for free panel advocate appointment."
                ],
                "keywords": ["free legal aid", "nalsa", "talsa", "dlsa", "article 39a", "free lawyer", "uchitha nyaya sahayam", "15100", "poor justice"]
            },
            {
                "id": "traffic_185_drunk_driving",
                "title": "Motor Vehicles Act — Drunk Driving & Traffic Fines",
                "section": "Section 185 Motor Vehicles (Amendment) Act, 2019",
                "legacy": "Motor Vehicles Act 1988",
                "act": "Motor Vehicles Act, 2019",
                "category": "Traffic & Road Safety",
                "nature": "Cognizable, Bailable",
                "punishment": "First offence: Fine up to ₹10,000 or 6 months jail; Second offence: ₹15,000 fine or 2 yrs jail",
                "plain_english": "Driving with blood alcohol concentration (BAC) exceeding 30 mg per 100 ml detected by breathalyzer. Police can seize vehicle keys and impound vehicle if driver is intoxicated.",
                "plain_telugu": "మద్యం సేవించి వాహనం నడిపితే బ్రీత్ ఎనలైజర్ పరీక్షలో 100 ml రక్తంలో 30 mg మించితే మొదటిసారి ₹10,000 జరిమానా లేదా 6 నెలల జైలు శిక్ష విధించబడుతుంది.",
                "plain_hindi": "शराब पीकर वाहन चलाने पर पहली बार ₹10,000 तक जुर्माना या 6 महीने की जेल का प्रावधान है। वाहन जब्त किया जा सकता है।",
                "enforcement_steps": [
                    "You have the right to demand a clean, sealed disposable straw for breath analyzer test.",
                    "If contested, police must take you to government hospital for blood test within 2 hours.",
                    "Fine must be paid via official e-Challan receipt, never cash to individual constables."
                ],
                "keywords": ["drunk driving", "traffic fine", "challan", "185", "motor vehicle", "driving license", "helmet fine", "police checking", "alcohol test"]
            },
            {
                "id": "rti_act_2005",
                "title": "Right to Information (RTI) — 30-Day Mandatory Disclosure",
                "section": "Section 6 & 7 Right to Information Act, 2005",
                "legacy": "RTI Act 2005",
                "act": "Right to Information Act, 2005",
                "category": "Citizen Empowerment & Governance",
                "nature": "Statutory Citizen Inquest Right",
                "punishment": "Penalty of ₹250 per day (up to ₹25,000) on Public Information Officer for delay",
                "plain_english": "Any citizen can file an RTI application to obtain copies of government files, tender records, road budget allocations, exam answer keys, or pension status within 30 days.",
                "plain_telugu": "ఏ పౌరుడైనా ప్రభుత్వ ఫైళ్లు, రోడ్ల బడ్జెట్, టెండర్లు, పెన్షన్ వివరాలను తెలుసుకోవడానికి RTI దరఖాస్తు చేయవచ్చు. 30 రోజులలోపు సమాచారం ఇవ్వడం అధికారుల తప్పనిసరి విధి.",
                "plain_hindi": "कोई भी नागरिक सरकारी फाइलों, बजट, विकास कार्यों और पेंशन की जानकारी 30 दिनों के भीतर प्राप्त करने के लिए RTI आवेदन कर सकता है।",
                "enforcement_steps": [
                    "Draft simple RTI application stating the specific information required.",
                    "Affix ₹10 court fee stamp or postal order (free for BPL card holders).",
                    "Submit to Public Information Officer (PIO) or file online at rtionline.gov.in."
                ],
                "keywords": ["rti", "right to information", "government records", "samachara hakku", "tender records", "road budget", "30 days"]
            },
            {
                "id": "bns_351_criminal_intimidation",
                "title": "Criminal Intimidation, Verbal Abuse & Death Threats",
                "section": "Section 351(2) & 352 Bharatiya Nyaya Sanhita, 2023 (BNS)",
                "legacy": "Section 506 & 504 Indian Penal Code (IPC 1860)",
                "act": "Bharatiya Nyaya Sanhita, 2023",
                "category": "Personal Safety & Criminal Law",
                "nature": "Non-Bailable if threat is of death or grievous hurt",
                "punishment": "Imprisonment up to 2 years, or fine; if threat is of death or grievous hurt, up to 7 years",
                "plain_english": "Applies when someone threatens you with injury to your person, reputation, or property, or intentionally insults you to provoke a breach of peace.",
                "plain_telugu": "ఎవరైనా మీ ప్రాణానికి, ఆస్తికి లేదా పరువుకు హాని కలిగిస్తామని బెదిరించినప్పుడు లేదా తీవ్రంగా దూషించినప్పుడు ఈ సెక్షన్ కింద 7 ఏళ్ల వరకు జైలు శిక్ష విధించవచ్చు.",
                "plain_hindi": "किसी को जान से मारने, शारीरिक चोट पहुंचाने या संपत्ति को नुकसान पहुंचाने की धमकी देने पर 7 साल तक की जेल हो सकती है।",
                "enforcement_steps": [
                    "Record phone calls, WhatsApp messages, or collect CCTV footage as proof.",
                    "File police complaint under Section 173 BNSS citing Section 351(2) BNS.",
                    "If threat is imminent, dial 112 immediately for emergency police dispatch."
                ],
                "keywords": ["threat", "threats", "abuse", "intimidation", "506", "351", "death threat", "bedirimpulu", "gaali", "stalking", "harassment"]
            }
        ]

    def search_laws(self, query: str, category: Optional[str] = None, lang: str = "en") -> Dict[str, Any]:
        """
        Searches the Indian statutory corpus by keyword, section, title, or everyday citizen situation.
        Returns matched statutes with explanations in the specified language.
        """
        q = query.strip().lower()
        results = []

        for law in self.laws_corpus:
            # Filter by category if specified
            if category and category.lower() not in law["category"].lower():
                continue

            score = 0
            # Exact keyword match
            for kw in law["keywords"]:
                if kw in q:
                    score += 15
                elif q in kw:
                    score += 8

            # Title & section match
            if q in law["title"].lower():
                score += 20
            if q in law["section"].lower() or q in law["legacy"].lower():
                score += 25
            if q in law["category"].lower():
                score += 10

            # Text content match
            if q in law["plain_english"].lower():
                score += 5

            if score > 0 or not q:  # If query is empty, return all
                explanation = law["plain_english"]
                if lang == "te" and law.get("plain_telugu"):
                    explanation = law["plain_telugu"]
                elif lang == "hi" and law.get("plain_hindi"):
                    explanation = law["plain_hindi"]

                results.append({
                    "id": law["id"],
                    "title": law["title"],
                    "section": law["section"],
                    "legacy": law["legacy"],
                    "act": law["act"],
                    "category": law["category"],
                    "nature": law["nature"],
                    "punishment": law["punishment"],
                    "explanation": explanation,
                    "enforcement_steps": law["enforcement_steps"],
                    "match_score": score
                })

        # Sort results by match score descending
        results.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "status": "success",
            "query": query,
            "category_filter": category or "All Categories",
            "language": lang,
            "total_matches": len(results),
            "results": results
        }

    def get_all_categories(self) -> List[str]:
        """Returns unique categories available in the legal encyclopedia."""
        return sorted(list(set(l["category"] for l in self.laws_corpus)))
