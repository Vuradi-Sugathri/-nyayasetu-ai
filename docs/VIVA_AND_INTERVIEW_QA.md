# NYAYASETU AI - COMPREHENSIVE VIVA & INTERVIEW QUESTION BANK
## 30+ In-Depth Technical, Statutory & Judicial Architecture Questions and Answers

---

### PART 1: LEGAL DOMAIN & STATUTORY FRAMEWORK

#### Q1: What are BNS and BNSS, and why does NyayaSetu AI map them?
**A:** In 2023, the Parliament of India repealed the colonial-era Indian Penal Code (IPC 1860) and Code of Criminal Procedure (CrPC 1973), replacing them with the **Bharatiya Nyaya Sanhita (BNS 2023)** and **Bharatiya Nagarik Suraksha Sanhita (BNSS 2023)**. 
Because police stations, courts, and citizens are currently transitioning between both systems, NyayaSetu AI features a **Dual-Statutory Cross-Referencing Engine**. For example, it maps classic cheating under Section 420 IPC directly to **Section 318(4) BNS 2023**, and theft under Section 379 IPC to **Section 303(2) BNS 2023**.

#### Q2: What is the significance of Section 173 of the BNSS 2023 in NyayaSetu AI's drafter?
**A:** Section 173 of the BNSS corresponds to Section 154 of the repealed CrPC. It governs the mandatory registration of information in cognizable cases (First Information Report / FIR). Under Section 173 BNSS, an aggrieved citizen can provide oral or written information to the police station. NyayaSetu AI's drafter formats the police complaint with exact Section 173 BNSS headings, jurisdictional particulars, and legal averments so the Station House Officer (SHO) cannot dismiss it as informal or vague.

#### Q3: How does the system handle "Zero FIR"?
**A:** A Zero FIR allows a citizen to register an FIR at *any* police station regardless of where the crime took place, as established by the Supreme Court of India in *Lalita Kumari v. Govt. of U.P. (2014)*. The police station must register the Zero FIR under Section 173 BNSS, assign it a serial number '0', and subsequently transfer it to the jurisdictional police station. NyayaSetu AI embeds this right in the Adhikar Guide and FIR drafter.

#### Q4: Why are non-compete clauses in employment letters flagged as void in India?
**A:** Under **Section 27 of the Indian Contract Act, 1872**, *"Every agreement by which anyone is restrained from exercising a lawful profession, trade or business of any kind, is to that extent void."* In the landmark case *Niranjan Shankar Golikari v. Century Spinning & Mfg. Co.* and later in *Percept D'Mark v. Zaheer Khan (2006)*, the Supreme Court held that the doctrine of restraint of trade applies to all post-employment covenants. While non-competes during active employment are valid, post-termination restrictions are strictly void ab initio. NyayaSetu AI's Contract Simplifier automatically identifies these clauses and advises employees accordingly.

#### Q5: Can a landlord arbitrarily forfeit a tenant's security deposit under Indian law?
**A:** No. Under **Sections 73 and 74 of the Indian Contract Act**, a party claiming liquidated damages for breach of contract can only recover reasonable compensation for *actual proved loss or damage*. A clause stating that the full deposit is automatically forfeited upon early vacation is treated as an unlawful penalty by civil courts. Furthermore, the Model Tenancy Act limits deposits to 2 months' rent and mandates refund within 30 days.

#### Q6: What is the "Golden Hour" in cyber fraud and how does NyayaSetu AI operationalize it?
**A:** When cybercriminals steal funds via fraudulent UPI or IMPS transfers, the money typically passes through multiple "mule" bank accounts before cash withdrawal at ATMs. The first 2 to 4 hours after the transaction are known as the **Golden Hour**. If reported within this window to National Helpline **1930** or the National Cybercrime Reporting Portal, the nodal liaison officers can place a temporary freeze on the recipient bank nodes under RBI guidelines. NyayaSetu AI alerts the user to this window with top priority.

---

### PART 2: SOFTWARE ARCHITECTURE & SYSTEM DESIGN

#### Q7: Why does NyayaSetu AI run on Port 8003?
**A:** To avoid socket collision across our multi-project ecosystem:
- Port **8000**: AgroPulse AI (Smart Agriculture)
- Port **8001**: NetraShiksha AI (Assistive Education)
- Port **8002**: SurakshaVision AI (Women's Safety & Surveillance)
- Port **8003**: **NyayaSetu AI** (Legal Tech & Citizen Justice Bridge)
Each service operates in an independent process environment, enabling side-by-side execution on any developer machine or production server.

#### Q8: Why did you build an offline-first architecture with zero external LLM API dependencies?
**A:** Three critical reasons:
1. **Confidentiality and Legal Privilege:** Legal grievances involve sensitive personal data (bank account numbers, domestic abuse allegations, salary figures, home addresses). Sending this data to commercial third-party LLMs introduces severe privacy violations.
2. **Deterministic Statutory Accuracy:** Generative LLMs frequently hallucinate legal sections or cite repealed IPC numbers incorrectly. A rule-and-knowledge-based statutory mapping engine produces 100% deterministic, verifiable legal citations every single time.
3. **Zero Operational Cost & High Availability:** Legal aid tools must remain accessible to low-income citizens and legal aid clinics without incurring API token charges or failing during internet outages.

#### Q9: How does the Telangana centroid geolocation lock work?
**A:** The frontend queries `navigator.geolocation` for latitude and longitude. It computes the Euclidean / spherical distance to pre-mapped centroids of major Indian states:
- Telangana Centroid: $(17.3850^\circ\text{ N}, 78.4867^\circ\text{ E})$
If the user's distance is within $4.5^\circ$ (covering Greater Hyderabad, Warangal, Karimnagar, Nizamabad, Khammam), it locks to **Telangana** and automatically activates **Telugu (`te`)** localization. If geolocation is denied or errors, it safely defaults to Telangana. An instant dropdown selector allows the user to override this to any state.

#### Q10: How does the Contract Simplifier calculate the Fairness Score?
**A:** The engine inspects contract text using regular expression pattern graphs for 5 high-frequency trap categories:
- Critical Traps (e.g. Unlawful deposit forfeiture, Ouster of jurisdiction): Deduct **25 points**.
- High Traps (e.g. Post-employment non-compete, Unilateral termination): Deduct **15 points**.
- Medium Traps (e.g. Usurious interest >24%): Deduct **8 points**.
Starting from a base score of 100, the final score is clamped between 20 and 100:
$$\text{Fairness Score} = \max(20, \min(100, 100 - \text{Total Deductions}))$$
A score $\ge 80$ indicates a Fair & Balanced contract, $55–79$ indicates Moderate Risk, and $<55$ indicates High Risk / Trap Clauses Detected.

#### Q11: How does the Multilingual Legal Voice Engine operate when offline?
**A:** The engine implements a dual-mode fallback strategy. If online, it uses `gTTS` to generate natural language speech in the target language (Telugu, Hindi, etc.) and caches the resulting MP3 on disk using an MD5 hash of `topic_key + lang`. If the host is completely offline and the file is not yet cached, it uses Python's native `wave` and `struct` modules to generate an in-memory dual-tone acoustic alert chime (523 Hz and 659 Hz) and returns it as a Base64-encoded Data URI. This guarantees that the audio endpoint never raises an unhandled exception or breaks the UI.

#### Q12: How are generated legal documents formatted for court admissibility?
**A:** Documents are drafted in compliance with standard Indian High Court notice formats:
- Sender and Recipient identification with full addresses.
- Subject line with statutory act references.
- Numbered averments detailing facts chronologically.
- Formal demand clause specifying the liquidated amount and 15-day rectification window.
- Warning of impending civil litigation or criminal prosecution under specific BNS/BNSS provisions.
- Reservation of rights to claim legal fees and 18% annual interest.
The frontend includes a `@media print` stylesheet that strips navigation bars, headers, and UI controls, leaving an A4-compliant document ready for printing and signature.

---

### PART 3: VIVA QUICK-FIRE SUMMARY

| Question | Short Answer |
|---|---|
| **What is the penalty under Sec 318(4) BNS?** | Imprisonment up to 7 years with fine for cheating. |
| **What is the NALSA Free Legal Aid helpline?** | **15100** (Toll-Free, 24/7 across India). |
| **What article guarantees free legal aid?** | **Article 39A** of the Constitution of India. |
| **Can police arrest a woman at 10:00 PM?** | No, prohibited under **Sec 43(5) BNSS** without prior written judicial magistrate permission. |
| **Within how many hours must an arrested person see a magistrate?** | **24 hours** excluding travel time (Article 22(2) & Sec 57 CrPC / Sec 58 BNSS). |
| **What is the maximum response time for a Legal Demand Notice?** | Standard practice is **15 days** from the date of receipt. |
