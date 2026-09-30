/**
 * NyayaSetu AI - Core Frontend Application Controller
 * Handles 8 Indian Languages Localization, Telangana Centroid Geolocation,
 * Legal Grievance Triage, 1-Click Document Drafting, Document Accuracy Verification,
 * Indian Law Search Encyclopedia (NyayaSearch), and Contract Analysis.
 */

// Application State
const State = {
  lang: 'te',             // Default language set initially (switches cleanly to 'en', 'hi', etc.)
  location: 'Telangana',  // Default location
  activeTab: 'triage',
  triageData: null,
  verificationData: null,
  currentDocText: '',
  allLawsData: [],
  selectedLawCategory: 'all'
};

// Geolocation Centroids for Indian States
const STATE_CENTROIDS = {
  'Telangana': { lat: 17.3850, lon: 78.4867, defaultLang: 'te' },
  'Andhra Pradesh': { lat: 15.9129, lon: 79.7400, defaultLang: 'te' },
  'Maharashtra': { lat: 19.7515, lon: 75.7139, defaultLang: 'mr' },
  'Karnataka': { lat: 15.3173, lon: 75.7139, defaultLang: 'kn' },
  'Tamil Nadu': { lat: 11.1271, lon: 78.6569, defaultLang: 'ta' },
  'Odisha': { lat: 20.9517, lon: 85.0985, defaultLang: 'or' },
  'Assam': { lat: 26.2006, lon: 92.9376, defaultLang: 'as' },
  'Delhi / North India': { lat: 28.6139, lon: 77.2090, defaultLang: 'hi' }
};

// Sample Grievances for Quick Testing
const SAMPLE_GRIEVANCES = {
  cyber: {
    en: "I transferred Rs 45,000 via GooglePay after receiving a phishing call from someone pretending to be my bank manager. The fraudster's mobile number is 9876543210 and UPI ID is fraud@okaxis. He has now blocked my calls.",
    te: "బ్యాంక్ మేనేజర్ అని చెప్పుకుని ఫోన్ చేసిన గుర్తుతెలియని వ్యక్తికి నేను UPI ద్వారా రూ. 45,000 బదిలీ చేశాను. ఆ తర్వాత అతను నా ఫోన్ నంబర్ బ్లాక్ చేశాడు.",
    hi: "बैंक मैनेजर बनकर कॉल करने वाले अज्ञात व्यक्ति को मैंने गूगल पे से 45,000 रुपये ट्रांसफर कर दिए। इसके बाद उसने मेरा नंबर ब्लॉक कर दिया है।"
  },
  rent: {
    en: "My landlord at Madhapur Hyderabad is refusing to refund my security deposit of Rs 75,000 despite vacating the flat 30 days ago with prior written notice. He is giving false excuses about painting charges.",
    te: "హైదరాబాద్‌లోని మా ఇంటి యజమాని నేను ముందుగా సమాచారం ఇచ్చి ఇల్లు ఖాళీ చేసినప్పటికీ రూ. 75,000 సెక్యూరిటీ డిపాజిట్ తిరిగి ఇవ్వడానికి నిరాకరిస్తున్నాడు.",
    hi: "मकान खाली करने और 30 दिन पहले नोटिस देने के बावजूद मेरे मकान मालिक ने 75,000 रुपये की सुरक्षा जमा राशि वापस करने से मना कर दिया है।"
  },
  job: {
    en: "My software company in HITEC City abruptly terminated my employment without mandatory 30-day notice and withheld my 2 months pending salary of Rs 1,40,000 and PF dues.",
    te: "నా కంపెనీ ఎటువంటి ముందస్తు నోటీసు ఇవ్వకుండా ఉద్యోగం నుంచి తొలగించి, 2 నెలల జీతం బకాయిలు రూ. 1,40,000 చెల్లించకుండా ఆపివేసింది.",
    hi: "मेरी कंपनी ने बिना किसी 30 दिन के कानूनी नोटिस के मुझे नौकरी से निकाल दिया और पिछले 2 महीने का वेतन 1,40,000 रुपये रोक लिया है।"
  },
  harassment: {
    en: "A neighbor named Ramesh is constantly stalking, verbally abusing, and threatening me with physical violence outside my apartment gate. I feel unsafe.",
    te: "మా అపార్ట్‌మెంట్ వద్ద రమేష్ అనే వ్యక్తి నన్ను వెంబడిస్తూ, అసభ్య పదజాలంతో దూషిస్తూ, చంపేస్తానని తీవ్రంగా బెదిరిస్తున్నాడు.",
    hi: "पड़ोस में रहने वाला एक व्यक्ति मुझे लगातार परेशान कर रहा है, गाली-गलौज कर रहा है और जान से मारने की धमकी दे रहा है।"
  }
};

// Sample Contracts
const SAMPLE_CONTRACTS = {
  unfair_rent: `TENANCY AGREEMENT
1. The Tenant shall deposit a refundable security deposit of Rs 1,00,000.
2. In the event of early termination before the completion of 11 months, the Landlord reserves the absolute right to forfeit the entire security deposit without accounting for repairs.
3. The Landlord reserves unilateral authority to increase the monthly rent by 25% at any time without prior written consent.
4. The Tenant waives all rights to approach civil court or the Rent Control Authority for any dispute arising out of this agreement.`,

  unfair_employment: `EMPLOYMENT COVENANT & TERMS
1. Non-Compete Clause: The Employee agrees that for a period of 24 months post termination of employment for any reason, the Employee shall not work for, consult, or assist any competing business or IT company anywhere in India.
2. Salary Retention: The Employer shall retain 3 months of Employee's salary as a security bond for 1 year.
3. Unilateral Termination: The Employer may terminate employment immediately without notice or severance pay, while the Employee must serve a mandatory 90-day notice period.`
};

// Sample Audits for Document Verification
const SAMPLE_AUDIT_DOCS = {
  notice: `LEGAL NOTICE
Date: 15-09-2026
To: ABC Tech Solutions Pvt Ltd, HITEC City, Hyderabad
From: Suresh Varma, Software Engineer, Kondapur, Hyderabad

Sir/Madam,
You have illegally terminated my services and withheld my pending salary of Rs 1,20,000 for July and August 2026. 
You are hereby called upon to release my full salary within 15 days from receipt of this notice, failing which I will initiate appropriate civil recovery proceedings and file complaint before the Labor Commissioner.
Yours faithfully,
Suresh Varma`,

  defective_lease: `RENTAL NOTE
I have rented my room to Mahesh. He paid 50,000 advance. 
If he leaves before 1 year, deposit will not be returned. No court cases allowed.
Signed: Landlord`
};

// Initialize Application on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initLocation();
  initEventListeners();
  applyLanguage(State.lang);
  loadSafeguardsData();
  loadAllLaws();
  triggerAudioForTopic('intro_welcome');
});

/**
 * Geolocation Detection with Telangana Centroid Lock
 */
function initLocation() {
  const locSelect = document.getElementById('locationSelect');
  if (locSelect) {
    locSelect.value = State.location;
    locSelect.addEventListener('change', (e) => {
      State.location = e.target.value;
      updateLocationBadge(State.location);
    });
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        const nearestState = findNearestState(latitude, longitude);
        if (nearestState) {
          State.location = nearestState;
          if (locSelect) locSelect.value = nearestState;
          updateLocationBadge(nearestState);
        }
      },
      (err) => {
        State.location = 'Telangana';
        updateLocationBadge('Telangana (Centroid Locked)');
      },
      { timeout: 3500 }
    );
  } else {
    State.location = 'Telangana';
    updateLocationBadge('Telangana (Centroid Locked)');
  }
}

function findNearestState(lat, lon) {
  const dTelangana = Math.hypot(lat - 17.3850, lon - 78.4867);
  if (dTelangana < 4.5) return 'Telangana';

  let minDistance = Infinity;
  let closest = 'Telangana';
  for (const [state, coords] of Object.entries(STATE_CENTROIDS)) {
    const d = Math.hypot(lat - coords.lat, lon - coords.lon);
    if (d < minDistance) {
      minDistance = d;
      closest = state;
    }
  }
  return closest;
}

function updateLocationBadge(stateName) {
  const badge = document.getElementById('detectedLocationBadge');
  if (badge) {
    badge.innerHTML = `📍 <strong>${stateName}</strong> (BNS Active)`;
  }
}

/**
 * Event Listeners Registration
 */
function initEventListeners() {
  // Navigation Tabs
  document.querySelectorAll('.view-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Language Selector
  const langSelect = document.getElementById('languageSelect');
  if (langSelect) {
    langSelect.value = State.lang;
    langSelect.addEventListener('change', (e) => {
      setLanguage(e.target.value);
    });
  }

  // Accessibility Toggles
  const contrastBtn = document.getElementById('contrastToggleBtn');
  if (contrastBtn) {
    contrastBtn.addEventListener('click', () => {
      document.body.classList.toggle('high-contrast');
    });
  }

  const dayModeBtn = document.getElementById('dayModeToggleBtn');
  if (dayModeBtn) {
    dayModeBtn.addEventListener('click', () => {
      document.body.classList.toggle('day-mode');
    });
  }

  // Triage Action Buttons
  const btnTriage = document.getElementById('btnRunTriage');
  if (btnTriage) btnTriage.addEventListener('click', runLegalTriage);

  document.querySelectorAll('.sample-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const type = chip.getAttribute('data-sample');
      fillSampleGrievance(type);
    });
  });

  // Drafter Action Buttons
  const btnGenNotice = document.getElementById('btnGenLegalNotice');
  if (btnGenNotice) btnGenNotice.addEventListener('click', draftNotice);

  const btnGenFIR = document.getElementById('btnGenFIR');
  if (btnGenFIR) btnGenFIR.addEventListener('click', draftFIR);

  const btnGenConsumer = document.getElementById('btnGenConsumer');
  if (btnGenConsumer) btnGenConsumer.addEventListener('click', draftConsumerComplaint);

  const btnPrintDoc = document.getElementById('btnPrintDoc');
  if (btnPrintDoc) btnPrintDoc.addEventListener('click', () => window.print());

  const btnCopyDoc = document.getElementById('btnCopyDoc');
  if (btnCopyDoc) btnCopyDoc.addEventListener('click', copyDocumentToClipboard);

  // Document Verifier Buttons (NEW)
  const btnVerify = document.getElementById('btnRunVerification');
  if (btnVerify) btnVerify.addEventListener('click', verifyDocumentAccuracy);

  const btnSampleNotice = document.getElementById('btnLoadSampleNoticeAudit');
  if (btnSampleNotice) {
    btnSampleNotice.addEventListener('click', () => {
      const box = document.getElementById('verifierTextInput');
      if (box) box.value = SAMPLE_AUDIT_DOCS.notice;
    });
  }

  const btnSampleLease = document.getElementById('btnLoadSampleLeaseAudit');
  if (btnSampleLease) {
    btnSampleLease.addEventListener('click', () => {
      const box = document.getElementById('verifierTextInput');
      if (box) box.value = SAMPLE_AUDIT_DOCS.defective_lease;
    });
  }

  // Indian Law Search (NyayaSearch)
  const btnSearch = document.getElementById('btnExecuteLawSearch');
  if (btnSearch) btnSearch.addEventListener('click', executeLawSearch);

  const searchInput = document.getElementById('lawSearchInput');
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') executeLawSearch();
    });
  }

  document.querySelectorAll('.law-filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.law-filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      State.selectedLawCategory = chip.getAttribute('data-cat');
      executeLawSearch();
    });
  });

  // Contract Simplifier Buttons
  const btnRunContract = document.getElementById('btnRunContract');
  if (btnRunContract) btnRunContract.addEventListener('click', simplifyContract);

  document.querySelectorAll('.sample-contract-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const cType = chip.getAttribute('data-contract');
      const box = document.getElementById('contractTextInput');
      if (box && SAMPLE_CONTRACTS[cType]) {
        box.value = SAMPLE_CONTRACTS[cType];
      }
    });
  });

  // Audio Playback
  const btnVoicePlay = document.getElementById('btnVoicePlay');
  if (btnVoicePlay) {
    btnVoicePlay.addEventListener('click', () => {
      const topic = btnVoicePlay.getAttribute('data-topic') || 'intro_welcome';
      triggerAudioForTopic(topic);
    });
  }
}

/**
 * Tab Switching Logic
 */
function switchTab(tabId) {
  State.activeTab = tabId;
  document.querySelectorAll('.view-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
  });

  document.querySelectorAll('.tab-content-panel').forEach(panel => {
    panel.style.display = (panel.id === `panel-${tabId}`) ? 'block' : 'none';
  });
}

/**
 * Multilingual Translation Application (Fixes English Toggle Completely)
 */
function setLanguage(langCode) {
  if (!I18N[langCode]) langCode = 'en';
  State.lang = langCode;
  
  const langSelect = document.getElementById('languageSelect');
  if (langSelect) langSelect.value = langCode;

  applyLanguage(langCode);

  // Re-render active dynamic content to eliminate any lingering regional text
  if (State.triageData) renderTriageResults(State.triageData);
  if (State.verificationData) renderVerificationResults(State.verificationData);
  executeLawSearch();
  loadSafeguardsData();
}

function applyLanguage(langCode) {
  const dict = I18N[langCode] || I18N['en'];

  // Apply to text elements with data-i18n attributes
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Apply to placeholders
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Update Voice Banner
  const voiceNotice = document.getElementById('voiceNoticeBanner');
  if (voiceNotice && dict.audioNotice) {
    voiceNotice.textContent = dict.audioNotice;
  }
}

/**
 * Fill Sample Grievance
 */
function fillSampleGrievance(type) {
  const input = document.getElementById('triageGrievanceInput');
  if (!input) return;

  const sampleSet = SAMPLE_GRIEVANCES[type];
  if (sampleSet) {
    input.value = sampleSet[State.lang] || sampleSet['en'] || sampleSet['te'];
  }
}

/**
 * 1. Legal Grievance Triage & BNS Mapping
 */
async function runLegalTriage() {
  const input = document.getElementById('triageGrievanceInput');
  const resultsContainer = document.getElementById('triageResultsContainer');
  const loader = document.getElementById('triageLoader');

  if (!input || !input.value.trim()) {
    const msg = State.lang === 'en' ? "Please describe your legal grievance." : 
                (State.lang === 'hi' ? "कृपया अपनी कानूनी समस्या का विवरण दें।" : "దయచేసి మీ సమస్యను వివరించండి.");
    alert(msg);
    return;
  }

  if (loader) loader.style.display = 'block';
  if (resultsContainer) resultsContainer.innerHTML = '';

  try {
    const res = await fetch('/api/legal/triage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        grievance_text: input.value.trim(),
        location: State.location
      })
    });

    if (!res.ok) throw new Error("Server error during triage analysis.");
    const data = await res.json();
    State.triageData = data;
    renderTriageResults(data);

    // Audio guidance trigger
    const cat = data.category_key || '';
    if (cat.includes('cyber')) triggerAudioForTopic('cyber_fraud_advice');
    else if (cat.includes('rent')) triggerAudioForTopic('tenancy_deposit_advice');
    else if (cat.includes('labor') || cat.includes('salary')) triggerAudioForTopic('salary_recovery_advice');
    else triggerAudioForTopic('fir_lodging_advice');

  } catch (err) {
    console.error(err);
    if (resultsContainer) {
      resultsContainer.innerHTML = `<div class="result-card" style="border-color: var(--accent-red);">
        <p style="color: var(--accent-red); font-weight: bold;">Error during analysis: ${err.message}</p>
      </div>`;
    }
  } finally {
    if (loader) loader.style.display = 'none';
  }
}

function renderTriageResults(data) {
  const container = document.getElementById('triageResultsContainer');
  if (!container) return;

  const isEn = State.lang === 'en';
  const isHi = State.lang === 'hi';

  const categoryName = data.category_name || data.category || "Legal Grievance";
  const urgency = data.urgency || data.severity || "STANDARD RECOURSE";
  const statutes = data.applicable_statutes || data.applicable_sections || [];
  const actionPlan = data.action_plan || (data.actionable_roadmap && data.actionable_roadmap.immediate_steps) || [];
  const evidenceList = data.evidence_checklist || data.evidentiary_checklist || [];
  const legalAid = data.legal_aid_eligibility || data.free_legal_aid_eligibility || {};

  // Statutes HTML
  let sectionsHtml = '';
  statutes.forEach(sec => {
    const sName = sec.section || sec.act || "Statutory Law";
    const legacy = sec.legacy_ipc || sec.legacy_ipc_crpc || "Direct Statutory Provision";
    const title = sec.title || sec.description || "";
    const penalty = sec.penalty || sec.punishment || "As determined by court";

    sectionsHtml += `
      <div class="statute-tag">
        <div class="statute-title">${sName} - ${sec.act || 'BNS 2023'}</div>
        <div style="font-size: 0.8rem; color: var(--accent-blue); margin-bottom: 3px;">
          ⚖️ ${isEn ? 'Legacy Reference' : (isHi ? 'पूर्व धारा (Legacy)' : 'పూర్వ చట్టం')}: <strong>${legacy}</strong>
        </div>
        <div style="font-size: 0.82rem; margin-bottom: 4px;">${title}</div>
        <div style="font-size: 0.78rem; color: var(--accent-gold-light);">
          ⛓️ ${isEn ? 'Remedy / Punishment' : (isHi ? 'सजा व प्रावधान' : 'శిక్ష / పరిహారం')}: <strong>${penalty}</strong>
        </div>
      </div>
    `;
  });

  // Action Steps HTML
  let stepsHtml = '';
  if (Array.isArray(actionPlan)) {
    actionPlan.forEach((item, idx) => {
      if (typeof item === 'object' && item.step) {
        stepsHtml += `<li style="margin-bottom: 0.45rem;"><strong>${item.step}:</strong> ${item.action}</li>`;
      } else {
        stepsHtml += `<li style="margin-bottom: 0.45rem;"><strong>${isEn ? 'Step' : (isHi ? 'चरण' : 'దశ')} ${idx + 1}:</strong> ${item}</li>`;
      }
    });
  }

  // Evidence Checklist HTML
  let evidenceHtml = '';
  evidenceList.forEach(item => {
    evidenceHtml += `
      <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; font-size: 0.83rem;">
        <input type="checkbox" checked onclick="return false;">
        <span>${item}</span>
      </div>
    `;
  });

  const goldenHourHtml = data.golden_hour_window ? `
    <div style="background: rgba(239, 68, 68, 0.12); border-left: 4px solid var(--accent-red); padding: 0.65rem 0.85rem; margin-bottom: 1rem; border-radius: 0 8px 8px 0; font-size: 0.83rem;">
      <strong style="color: var(--accent-red);">⏱️ ${isEn ? 'Golden Hour Window' : (isHi ? 'गोल्डन ऑवर समय सीमा' : 'గోల్డెన్ అవర్ పరిమితి')}:</strong> ${data.golden_hour_window}
    </div>
  ` : '';

  container.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <div>
          <span class="brand-tag">${categoryName}</span>
          ${data.primary_authority ? `<span style="font-size: 0.78rem; color: var(--text-muted); margin-left: 0.5rem;">${data.primary_authority}</span>` : ''}
        </div>
        <div style="font-size: 0.82rem; font-weight: 700; color: ${urgency.includes('CRITICAL') ? 'var(--accent-red)' : 'var(--accent-gold)'};">
          🚨 ${urgency}
        </div>
      </div>

      ${goldenHourHtml}

      <div style="margin-bottom: 1rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-gold); margin-bottom: 0.6rem;">
          📜 ${isEn ? 'Applicable Statutes & Sections (BNS 2023 & IPC)' : (isHi ? 'लागू कानून एवं धाराएं (BNS 2023 एवं IPC)' : 'వర్తించే చట్టాలు & సెక్షన్లు (BNS 2023 & IPC)')}:
        </h4>
        ${sectionsHtml}
      </div>

      <div style="margin-bottom: 1rem; background: var(--bg-secondary); padding: 0.85rem; border-radius: 8px;">
        <h4 style="font-size: 0.9rem; color: var(--accent-green); margin-bottom: 0.5rem;">
          🗺️ ${isEn ? 'Immediate Action Roadmap' : (isHi ? 'तत्काल कार्रवाई योजना' : 'తక్షణ కార్యాచరణ ప్రణాళిక')}:
        </h4>
        <ol style="padding-left: 1.25rem; font-size: 0.85rem; color: var(--text-main);">
          ${stepsHtml}
        </ol>
      </div>

      <div style="margin-bottom: 1rem;">
        <h4 style="font-size: 0.9rem; color: var(--accent-blue); margin-bottom: 0.5rem;">
          📋 ${isEn ? 'Evidentiary Checklist for Court / Police' : (isHi ? 'जरूरी सबूतों की सूची' : 'సమర్పించాల్సిన ఆధారాల జాబితా')}:
        </h4>
        ${evidenceHtml}
      </div>

      <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); padding: 0.75rem; border-radius: 8px; font-size: 0.82rem; margin-bottom: 1rem;">
        <div style="font-weight: 700; color: var(--accent-green);">
          🏛️ ${isEn ? 'NALSA Free Legal Aid (Article 39A)' : (isHi ? 'NALSA मुफ्त कानूनी सहायता (अनुच्छेद 39A)' : 'NALSA ఉచిత న్యాయ సహాయం (ఆర్టికల్ 39A)')}:
        </div>
        <div style="color: var(--text-main); margin-top: 0.25rem;">
          ${legalAid.scheme || 'Legal Services Authorities Act, 1987'} | 
          <strong>${isEn ? 'Toll-Free Helpline' : 'ఉచిత హెల్ప్‌లైన్'}: 15100</strong>
        </div>
      </div>

      <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <button class="btn btn-primary" onclick="transferTriageToDrafter('notice')">
          📄 ${isEn ? 'Draft Pre-Litigation Legal Demand Notice' : 'ఈ సమస్యపై లీగల్ డిమాండ్ నోటీసు రూపొందించండి'}
        </button>
        <button class="btn btn-secondary" onclick="transferTriageToDrafter('fir')">
          🚓 ${isEn ? 'Draft Police FIR Application (Sec 173 BNSS)' : 'పోలీస్ FIR ఫిర్యాదు తయారుచేయండి'}
        </button>
      </div>
    </div>
  `;
}

/**
 * Transfer Triage Data to Drafter
 */
function transferTriageToDrafter(docType) {
  switchTab('drafter');
  const factsBox = document.getElementById('draftFacts');
  const disputeType = document.getElementById('draftDisputeType');
  const triageInput = document.getElementById('triageGrievanceInput');

  if (factsBox && triageInput) factsBox.value = triageInput.value;

  if (State.triageData && disputeType) {
    const cat = State.triageData.category_name || State.triageData.category || '';
    if (cat.includes('Rent')) disputeType.value = 'Rental Security Deposit Refund';
    else if (cat.includes('Labor') || cat.includes('Salary')) disputeType.value = 'Unpaid Salary & Wrongful Termination';
    else if (cat.includes('Consumer')) disputeType.value = 'Consumer Deficiency in Service';
    else disputeType.value = 'Financial Fraud & Breach of Trust';
  }

  if (docType === 'fir') draftFIR();
  else draftNotice();
}

/**
 * 2. Document Drafter: Legal Notice
 */
async function draftNotice() {
  const senderName = document.getElementById('draftSenderName')?.value || "Complainant Citizen";
  const senderAddress = document.getElementById('draftSenderAddress')?.value || "H.No. 4-12, Madhapur, Hyderabad, Telangana";
  const recipientName = document.getElementById('draftRecipientName')?.value || "Opposite Party / Landlord / Employer";
  const recipientAddress = document.getElementById('draftRecipientAddress')?.value || "Plot 88, Jubilee Hills, Hyderabad";
  const disputeType = document.getElementById('draftDisputeType')?.value || "Non-Refund of Security Deposit & Breach of Contract";
  const disputeFacts = document.getElementById('draftFacts')?.value || "The recipient has withheld the legitimate amount without lawful justification.";
  const amount = document.getElementById('draftAmount')?.value || "75,000";
  const period = parseInt(document.getElementById('draftNoticePeriod')?.value || "15");

  const previewBox = document.getElementById('docPreviewBox');
  if (previewBox) previewBox.textContent = State.lang === 'en' ? "⏳ Synthesizing formal Pre-Litigation Legal Notice..." : "⏳ అధికారిక లీగల్ నోటీసు రూపకల్పన జరుగుతోంది...";

  try {
    const res = await fetch('/api/legal/draft-notice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sender_name: senderName,
        sender_address: senderAddress,
        recipient_name: recipientName,
        recipient_address: recipientAddress,
        dispute_type: disputeType,
        dispute_facts: disputeFacts,
        demand_amount: amount,
        notice_period_days: period,
        location: State.location
      })
    });

    if (!res.ok) throw new Error("Failed to generate legal notice.");
    const data = await res.json();
    State.currentDocText = data.document_text || data.formatted_text || "";
    if (previewBox) previewBox.textContent = State.currentDocText;

  } catch (err) {
    if (previewBox) previewBox.textContent = `Error: ${err.message}`;
  }
}

/**
 * 2. Document Drafter: Police FIR Application
 */
async function draftFIR() {
  const senderName = document.getElementById('draftSenderName')?.value || "Complainant Citizen";
  const senderAddress = document.getElementById('draftSenderAddress')?.value || "Hyderabad, Telangana";
  const facts = document.getElementById('draftFacts')?.value || "Incident of cheating, breach of trust and unauthorized withholding of funds.";
  
  const applicableSecs = State.triageData ? 
    (State.triageData.applicable_statutes || State.triageData.applicable_sections || []).map(s => s.section).join(', ') : 
    "Section 316, 318 BNS 2023";

  const previewBox = document.getElementById('docPreviewBox');
  if (previewBox) previewBox.textContent = State.lang === 'en' ? "⏳ Drafting Police FIR Application under Section 173 BNSS..." : "⏳ పోలీస్ స్టేషన్ FIR దరఖాస్తు రూపకల్పన జరుగుతోంది (Sec 173 BNSS)...";

  try {
    const res = await fetch('/api/legal/draft-fir', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        complainant_name: senderName,
        complainant_phone: "9876543210",
        complainant_address: senderAddress,
        police_station_name: "Station House Officer, Cyber Crime Police Station / Local PS, Hyderabad",
        incident_date: new Date().toISOString().split('T')[0],
        incident_location: State.location,
        accused_details: document.getElementById('draftRecipientName')?.value || "Unknown Cyber Fraudster / Accused",
        incident_description: facts,
        applicable_sections: applicableSecs
      })
    });

    if (!res.ok) throw new Error("Failed to generate FIR draft.");
    const data = await res.json();
    State.currentDocText = data.document_text || data.formatted_text || "";
    if (previewBox) previewBox.textContent = State.currentDocText;

  } catch (err) {
    if (previewBox) previewBox.textContent = `Error: ${err.message}`;
  }
}

/**
 * 2. Document Drafter: Consumer Complaint
 */
function draftConsumerComplaint() {
  const senderName = document.getElementById('draftSenderName')?.value || "Aggrieved Consumer";
  const recipientName = document.getElementById('draftRecipientName')?.value || "Opposite Party Service Provider";
  const facts = document.getElementById('draftFacts')?.value || "Deficiency of service and unfair trade practice.";
  const amount = document.getElementById('draftAmount')?.value || "50,000";

  const template = `BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION AT HYDERABAD
COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

IN THE MATTER OF:
${senderName}
... Complainant

VERSUS

${recipientName}
... Opposite Party

MOST RESPECTFULLY SHOWETH:
1. That the Complainant is a bonafide consumer as defined under Section 2(7) of the Consumer Protection Act, 2019.
2. BRIEF FACTS OF THE CASE:
   ${facts}
3. DEFICIENCY IN SERVICE:
   The Opposite Party has failed to render due service and engaged in Unfair Trade Practice under Section 2(47) of the Act.
4. PRAYER:
   It is most respectfully prayed that this Hon'ble Commission may be pleased to:
   a) Direct the Opposite Party to refund the disputed sum of Rs. ${amount}/- along with interest @ 18% p.a.
   b) Award compensation of Rs. 25,000/- towards mental agony, harassment and litigation costs.
   c) Pass such other order(s) as this Hon'ble Commission deems fit in the interest of justice.

Place: Hyderabad, Telangana
Date: ${new Date().toLocaleDateString('en-IN')}
(Complainant Sign)`;

  State.currentDocText = template;
  const previewBox = document.getElementById('docPreviewBox');
  if (previewBox) previewBox.textContent = template;
}

function copyDocumentToClipboard() {
  if (!State.currentDocText) {
    alert("No document text to copy.");
    return;
  }
  navigator.clipboard.writeText(State.currentDocText).then(() => {
    alert("Document text successfully copied to clipboard!");
  });
}

/**
 * 3. Document Verifier & Accuracy Audit (NEW FEATURE)
 */
async function verifyDocumentAccuracy() {
  const fileInput = document.getElementById('verifierFileInput');
  const textInput = document.getElementById('verifierTextInput');
  const container = document.getElementById('verifierResultsContainer');
  const loader = document.getElementById('verifierLoader');

  const textVal = textInput ? textInput.value.trim() : "";
  const hasFile = fileInput && fileInput.files && fileInput.files.length > 0;

  if (!textVal && !hasFile) {
    alert("Please upload a file or paste legal document text to verify.");
    return;
  }

  if (loader) loader.style.display = 'block';
  if (container) container.innerHTML = '';

  const formData = new FormData();
  if (textVal) formData.append('doc_text', textVal);
  if (hasFile) formData.append('file', fileInput.files[0]);

  try {
    const res = await fetch('/api/legal/verify-document', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error("Document audit failed.");
    const data = await res.json();
    State.verificationData = data;
    renderVerificationResults(data);

  } catch (err) {
    if (container) {
      container.innerHTML = `<div class="result-card" style="border-color: var(--accent-red);">
        <p style="color: var(--accent-red); font-weight: bold;">Audit Error: ${err.message}</p>
      </div>`;
    }
  } finally {
    if (loader) loader.style.display = 'none';
  }
}

function renderVerificationResults(data) {
  const container = document.getElementById('verifierResultsContainer');
  if (!container) return;

  const isEn = State.lang === 'en';
  const score = data.accuracy_score || 0;
  const scoreColor = score >= 80 ? 'var(--accent-green)' : (score >= 55 ? 'var(--accent-gold)' : 'var(--accent-red)');

  // Passed Elements HTML
  let passedHtml = '';
  data.passed_elements.forEach(item => {
    passedHtml += `
      <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem; font-size: 0.83rem;">
        <span style="color: var(--accent-green); font-weight: bold;">✓</span>
        <span>${item.title}</span>
      </div>
    `;
  });

  // Missing / Defective Elements HTML
  let missingHtml = '';
  if (data.missing_elements.length === 0) {
    missingHtml = `<p style="color: var(--accent-green); font-size: 0.85rem;">All critical statutory elements verified. Ready for filing.</p>`;
  } else {
    data.missing_elements.forEach(item => {
      missingHtml += `
        <div class="trap-card" style="margin-bottom: 0.6rem;">
          <div style="font-weight: 700; color: var(--accent-red); margin-bottom: 2px;">
            ⚠️ ${item.title} (${item.importance})
          </div>
          <div style="font-size: 0.82rem; color: var(--text-main); margin-bottom: 3px;">
            ${item.issue}
          </div>
          <div style="font-size: 0.78rem; color: var(--accent-gold-light);">
            💡 <strong>Recommended Fix:</strong> ${item.remedy}
          </div>
        </div>
      `;
    });
  }

  // Citation Warnings HTML
  let warningsHtml = '';
  if (data.citation_warnings && data.citation_warnings.length > 0) {
    warningsHtml = `
      <div style="background: rgba(234, 179, 8, 0.12); border-left: 4px solid var(--accent-gold); padding: 0.65rem 0.85rem; margin-bottom: 1rem; border-radius: 0 8px 8px 0; font-size: 0.82rem;">
        <strong style="color: var(--accent-gold);">📜 Statutory Citations Notice:</strong>
        <ul style="padding-left: 1.25rem; margin-top: 4px;">
          ${data.citation_warnings.map(w => `<li>${w}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <div>
          <span class="brand-tag">${data.document_type}</span>
          <span style="font-size: 0.78rem; color: var(--text-muted); margin-left: 0.5rem;">${data.word_count} words analyzed</span>
        </div>
        <div style="font-size: 1.6rem; font-weight: 800; color: ${scoreColor};">
          ${score}/100
        </div>
      </div>

      <div style="margin-bottom: 0.85rem;">
        <div style="font-size: 0.95rem; font-weight: 700; color: ${scoreColor};">
          Verdict: ${data.court_readiness}
        </div>
        <div style="font-size: 0.83rem; color: var(--text-muted); margin-top: 2px;">
          ${data.verdict_summary}
        </div>
      </div>

      ${warningsHtml}

      <div style="margin-bottom: 1rem;">
        <h4 style="font-size: 0.9rem; color: var(--accent-green); margin-bottom: 0.5rem;">
          ✓ Verified Statutory Elements (${data.passed_elements_count}):
        </h4>
        <div style="background: var(--bg-secondary); padding: 0.75rem; border-radius: 8px;">
          ${passedHtml}
        </div>
      </div>

      <div style="margin-bottom: 1rem;">
        <h4 style="font-size: 0.9rem; color: var(--accent-red); margin-bottom: 0.5rem;">
          ⚠️ Missing Mandatory Ingredients & Risks (${data.missing_elements_count}):
        </h4>
        ${missingHtml}
      </div>

      <button class="btn btn-primary" onclick="switchTab('drafter')">
        ✍️ Auto-Correct & Re-Draft in Court Format
      </button>
    </div>
  `;
}

/**
 * 4. Indian Law Search & Citizen Encyclopedia (NyayaSearch)
 */
async function loadAllLaws() {
  try {
    const res = await fetch(`/api/legal/all-laws?lang=${State.lang}`);
    if (!res.ok) return;
    const data = await res.json();
    State.allLawsData = data.results || [];
    renderLawSearchResults(State.allLawsData);
  } catch (e) {
    console.error("Failed to load initial laws:", e);
  }
}

async function executeLawSearch() {
  const input = document.getElementById('lawSearchInput');
  const container = document.getElementById('lawSearchResultsContainer');
  const query = input ? input.value.trim() : "";
  const category = State.selectedLawCategory === 'all' ? '' : State.selectedLawCategory;

  if (container) container.innerHTML = '<div style="text-align:center; padding: 2rem; color: var(--accent-gold);">⏳ Searching Indian Law Encyclopedia...</div>';

  try {
    const res = await fetch(`/api/legal/search-laws?q=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}&lang=${State.lang}`);
    if (!res.ok) throw new Error("Search failed.");
    const data = await res.json();
    renderLawSearchResults(data.results || []);
  } catch (err) {
    if (container) container.innerHTML = `<p style="color: var(--accent-red);">Search Error: ${err.message}</p>`;
  }
}

function renderLawSearchResults(laws) {
  const container = document.getElementById('lawSearchResultsContainer');
  if (!container) return;

  if (!laws || laws.length === 0) {
    container.innerHTML = `
      <div class="result-card" style="text-align: center; padding: 2rem; color: var(--text-muted);">
        <h3>No matching statutes found</h3>
        <p style="font-size: 0.85rem;">Try searching everyday terms like "rent", "cheating", "traffic", "dowry", "cyber", or section numbers like "318", "420".</p>
      </div>
    `;
    return;
  }

  let html = `<div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">Showing <strong>${laws.length}</strong> matching Indian laws:</div>`;

  laws.forEach(law => {
    let stepsHtml = '';
    law.enforcement_steps.forEach(step => {
      stepsHtml += `<li style="margin-bottom: 0.25rem;">${step}</li>`;
    });

    html += `
      <div class="result-card" style="margin-bottom: 1rem;">
        <div class="result-card-header">
          <div>
            <h3 style="font-size: 1.05rem; color: var(--accent-gold); margin-bottom: 2px;">
              ${law.title}
            </h3>
            <span class="brand-tag">${law.category}</span>
          </div>
          <div style="font-size: 0.78rem; color: var(--accent-blue); font-family: var(--font-mono);">
            ${law.nature}
          </div>
        </div>

        <div style="background: var(--bg-secondary); padding: 0.65rem 0.85rem; border-radius: 6px; margin-bottom: 0.6rem; font-size: 0.85rem;">
          <div>📜 <strong>Current Statute:</strong> <span style="color: var(--accent-gold-light); font-weight: bold;">${law.section}</span></div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">⚖️ <strong>Legacy Reference:</strong> ${law.legacy}</div>
        </div>

        <div style="font-size: 0.88rem; line-height: 1.5; color: var(--text-main); margin-bottom: 0.6rem;">
          ${law.explanation}
        </div>

        <div style="font-size: 0.82rem; color: var(--accent-red); margin-bottom: 0.6rem;">
          ⛓️ <strong>Punishment / Legal Remedy:</strong> ${law.punishment}
        </div>

        <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid var(--accent-blue); padding: 0.6rem 0.85rem; border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
          <strong style="color: var(--accent-blue); font-size: 0.82rem;">🛡️ How to Enforce Your Rights:</strong>
          <ul style="padding-left: 1.25rem; font-size: 0.82rem; margin-top: 3px; color: var(--text-main);">
            ${stepsHtml}
          </ul>
        </div>

        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.4rem 0.8rem;" onclick="loadLawIntoDrafter('${law.title}')">
            ✍️ Draft Notice for This Law
          </button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function loadLawIntoDrafter(lawTitle) {
  switchTab('drafter');
  const disputeType = document.getElementById('draftDisputeType');
  if (disputeType) disputeType.value = lawTitle;
  draftNotice();
}

/**
 * 5. Contract & Agreement Simplifier
 */
async function simplifyContract() {
  const input = document.getElementById('contractTextInput');
  const typeSelect = document.getElementById('contractTypeSelect');
  const resultsContainer = document.getElementById('contractResultsContainer');
  const loader = document.getElementById('contractLoader');

  if (!input || !input.value.trim()) {
    alert("Please paste contract terms to analyze.");
    return;
  }

  if (loader) loader.style.display = 'block';
  if (resultsContainer) resultsContainer.innerHTML = '';

  const formData = new FormData();
  formData.append('contract_text', input.value.trim());
  formData.append('contract_type', typeSelect ? typeSelect.value : 'rental_agreement');

  try {
    const res = await fetch('/api/legal/simplify-contract', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error("Contract analysis failed.");
    const data = await res.json();
    renderContractResults(data);

  } catch (err) {
    if (resultsContainer) {
      resultsContainer.innerHTML = `<p style="color: var(--accent-red);">Error: ${err.message}</p>`;
    }
  } finally {
    if (loader) loader.style.display = 'none';
  }
}

function renderContractResults(data) {
  const container = document.getElementById('contractResultsContainer');
  if (!container) return;

  const traps = data.flagged_traps || data.unfair_clauses_identified || [];
  const summaryPoints = data.plain_language_summary || data.plain_english_summary || [];

  let trapsHtml = '';
  if (traps.length === 0) {
    trapsHtml = `<p style="color: var(--accent-green); font-size: 0.85rem;">No hazardous or void clauses detected in this agreement.</p>`;
  } else {
    traps.forEach(trap => {
      const issue = trap.title || trap.issue || "Hazardous Clause";
      const status = trap.legal_verdict || trap.legal_status || "Unenforceable";
      const advice = trap.citizen_advice || trap.action_recommended || "Insist on clause amendment";
      const statute = trap.statute || "Indian Contract Act";

      trapsHtml += `
        <div class="trap-card">
          <div style="font-weight: 700; color: var(--accent-red); margin-bottom: 2px;">
            ⚠️ ${issue}
          </div>
          <div style="font-size: 0.8rem; color: var(--accent-blue); font-family: var(--font-mono); margin-bottom: 4px;">
            Statute: <strong>${statute}</strong>
          </div>
          <div style="font-size: 0.82rem; margin-bottom: 4px; color: var(--text-main);">
            ${status}
          </div>
          <div style="font-size: 0.8rem; color: var(--accent-gold-light);">
            💡 Advice: <strong>${advice}</strong>
          </div>
        </div>
      `;
    });
  }

  let summaryHtml = '';
  summaryPoints.forEach(point => {
    summaryHtml += `<li style="margin-bottom: 0.4rem;">${point}</li>`;
  });

  const scoreColor = data.fairness_score >= 70 ? 'var(--accent-green)' : (data.fairness_score >= 45 ? 'var(--accent-gold)' : 'var(--accent-red)');

  container.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <div>
          <h3 style="font-size: 1.1rem; color: var(--text-main);">Contract Fairness Score</h3>
          <span style="font-size: 0.8rem; color: var(--text-muted);">${data.contract_type}</span>
        </div>
        <div style="font-size: 1.7rem; font-weight: 800; color: ${scoreColor};">
          ${data.fairness_score}/100
        </div>
      </div>

      <div style="margin-bottom: 1.25rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-red); margin-bottom: 0.6rem;">
          🚨 Flagged Unfair / Void Clauses:
        </h4>
        ${trapsHtml}
      </div>

      <div style="background: var(--bg-secondary); padding: 0.85rem; border-radius: 8px;">
        <h4 style="font-size: 0.9rem; color: var(--accent-gold); margin-bottom: 0.5rem;">
          📑 Plain Language Summary:
        </h4>
        <ul style="padding-left: 1.25rem; font-size: 0.85rem;">
          ${summaryHtml}
        </ul>
      </div>
    </div>
  `;
}

/**
 * 6. Rights & Safeguards Directory
 */
async function loadSafeguardsData() {
  const container = document.getElementById('rightsCardsContainer');
  if (!container) return;

  try {
    const res = await fetch('/api/legal/safeguards');
    if (!res.ok) return;
    const data = await res.json();

    let cardsHtml = '';
    for (const [key, category] of Object.entries(data)) {
      let rulesHtml = '';
      category.rules.forEach(rule => {
        rulesHtml += `
          <div class="right-rule-item">
            <div class="right-rule-name">${rule.rule}</div>
            <div class="right-rule-statute">${rule.statute}</div>
            <div style="color: var(--text-muted); font-size: 0.82rem;">${rule.summary}</div>
          </div>
        `;
      });

      cardsHtml += `
        <div class="right-card">
          <div class="right-card-title">
            <span>🛡️</span> ${category.title}
          </div>
          ${rulesHtml}
        </div>
      `;
    }

    container.innerHTML = cardsHtml;
  } catch (e) {
    console.error("Safeguards load error:", e);
  }
}

/**
 * Audio Synthesis & Guidance Playback
 */
async function triggerAudioForTopic(topicKey) {
  const audioPlayer = document.getElementById('legalAudioPlayer');
  const noticeBox = document.getElementById('voiceNoticeBanner');

  try {
    const res = await fetch('/api/legal/voice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic_key: topicKey,
        lang: State.lang
      })
    });

    if (!res.ok) return;
    const data = await res.json();

    if (noticeBox) {
      noticeBox.innerHTML = `🔊 <strong>${data.language.toUpperCase()}:</strong> ${data.spoken_text || data.text || ''}`;
    }

    if (audioPlayer && data.audio_url) {
      audioPlayer.src = data.audio_url;
      audioPlayer.play().catch(e => {
        console.log("Audio autoplay restricted by browser.");
      });
    }

  } catch (err) {
    console.error("Voice synthesis request error:", err);
  }
}
