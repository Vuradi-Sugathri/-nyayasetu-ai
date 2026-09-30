"""
NyayaSetu AI - Multilingual Legal Voice Engine
Synthesizes spoken legal guidance, emergency citizen rights briefings, and helpline announcements
across 8 Indian languages (Telugu, Hindi, English, Tamil, Marathi, Kannada, Odia, Assamese).
"""

import os
import io
import math
import wave
import struct
import hashlib
import base64
from pathlib import Path
from typing import Dict, Any

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = BASE_DIR / "data" / "audio_cache"

LANG_CONFIG = {
    "te": {"name": "Telugu", "native": "తెలుగు", "gtts": "te"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "gtts": "hi"},
    "en": {"name": "English", "native": "English", "gtts": "en"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "gtts": "ta"},
    "mr": {"name": "Marathi", "native": "मराठी", "gtts": "mr"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "gtts": "kn"},
    "or": {"name": "Odia", "native": "ଓଡ଼ିଆ", "gtts": "en"},
    "as": {"name": "Assamese", "native": "অসমীয়া", "gtts": "en"}
}

# Core Spoken Legal Advice Transcripts
LEGAL_SPEECH_CATALOG = {
    "cyber_fraud_advice": {
        "te": "సైబర్ మోసం జరిగిన వెంటనే జాతీయ హెల్ప్‌లైన్ 1930 కు కాల్ చేయండి. మీ బ్యాంక్ లావాదేవీ UTR నంబర్‌ను తెలియజేయడం ద్వారా దొంగిలించబడిన డబ్బును స్తంభింపజేయవచ్చు.",
        "hi": "साइबर धोखाधड़ी होते ही तुरंत राष्ट्रीय हेल्पलाइन 1930 पर कॉल करें। अपने बैंक लेनदेन का यूटीआर नंबर दर्ज कराकर आप अपने पैसे को ब्लॉक करवा सकते हैं।",
        "en": "In case of cyber financial fraud, immediately dial 1930 or visit cybercrime.gov.in within 2 hours to freeze the defrauded funds in the recipient bank account.",
        "ta": "சைபர் மோசடி நடந்தால் உடனடியாக 1930 என்ற உதவி எண்ணை அழைக்கவும். உங்கள் வங்கி பரிவர்த்தனை எண்ணை தெரிவித்து பணத்தை முடக்க முடியும்.",
        "mr": "सायबर फसवणूक झाल्यास ताबडतोब 1930 या हेल्पलाइनवर कॉल करा. बँक व्यवहार यूटीआर नंबर नोंदवून आपण फसवणुकीची रक्कम गोठवू शकता.",
        "kn": "ಸೈಬರ್ ವಂಚನೆ ಸಂಭವಿಸಿದ ತಕ್ಷಣ ರಾಷ್ಟ್ರೀಯ ಸಹಾಯವಾಣಿ 1930 ಗೆ ಕರೆ ಮಾಡಿ. ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ವಹಿವಾಟು ಸಂಖ್ಯೆಯನ್ನು ನೀಡಿ ಹಣವನ್ನು ತಡೆಹಿಡಿಯಿರಿ.",
        "or": "ସାଇବର ଠକେଇ ହେଲେ ତୁରନ୍ତ 1930 ହେଲ୍ପଲାଇନକୁ କଲ୍ କରନ୍ତୁ। ନିଜର ବ୍ୟାଙ୍କ ଟ୍ରାଞ୍ଜାକ୍ସନ ନମ୍ବର ଦେଇ ଟଙ୍କା ଫ୍ରିଜ୍ କରନ୍ତୁ।",
        "as": "চাইবাৰ প্ৰবঞ্চনা হ'লে তৎক্ষণাৎ ১৯৩০ নম্বৰত ফোন কৰক আৰু বেংক লেনদেনৰ নম্বৰ জনাই ধন ফ্ৰিজ কৰক।"
    },

    "arrest_rights_brief": {
        "te": "భారత రాజ్యాంగం ప్రకారం అరెస్ట్ అయిన వ్యక్తికి కారణాలు తెలుసుకునే హక్కు, బంధువులకు సమాచారం ఇచ్చే హక్కు మరియు ఉచిత వైద్య పరీక్ష చేయించుకునే హక్కు ఉన్నాయి.",
        "hi": "भारतीय कानून के अनुसार गिरफ्तार व्यक्ति को गिरफ्तारी का कारण जानने, परिजनों को सूचित करने और 24 घंटे के भीतर मजिस्ट्रेट के सामने पेश किए जाने का संवैधानिक अधिकार है।",
        "en": "Under Indian Law and Article 22 of the Constitution, you have the right to know the grounds of arrest, the right to consult an advocate, and mandatory production before a Magistrate within 24 hours.",
        "ta": "இந்திய சட்டத்தின்படி கைது செய்யப்பட்ட நபருக்கு காரணங்களை அறியும் உரிமை, வழக்கறிஞரை அணுகும் உரிமை மற்றும் 24 மணி நேரத்திற்குள் நீதிபதி முன் ஆஜர்படுத்தப்படும் உரிமை உண்டு.",
        "mr": "भारतीय कायद्यानुसार अटक केलेल्या व्यक्तीला अटकेचे कारण जाणून घेण्याचा, वकिलाचा सल्ला घेण्याचा आणि 24 तासांच्या आत न्यायाधीशांसमोर हजर राहण्याचा अधिकार आहे.",
        "kn": "ಭಾರತೀಯ ಕಾನೂನಿನ ಪ್ರಕಾರ ಬಂಧಿತ ವ್ಯಕ್ತಿಗೆ ಬಂಧನದ ಕಾರಣ ತಿಳಿಯುವ, ವಕೀಲರನ್ನು ಭೇಟಿ ಮಾಡುವ ಮತ್ತು 24 ಗಂಟೆಗಳಲ್ಲಿ ಮ್ಯಾಜಿಸ್ಟ್ರೇಟ್ ಮುಂದೆ ಹಾಜರುಪಡಿಸುವ ಹಕ್ಕಿದೆ.",
        "or": "ଭାରତୀୟ ସମ୍ବିଧାନ ଅନୁଯାୟୀ ଗିରଫ ବ୍ୟକ୍ତିଙ୍କୁ ଗିରଫର କାରଣ ଜାଣିବା ଏବଂ 24 ଘଣ୍ଟା ମଧ୍ୟରେ ମାଜିଷ୍ଟ୍ରେଟଙ୍କ ସମ୍ମୁଖରେ ହାଜର କରାଯିବାର ଅଧିକାର ଅଛି।",
        "as": "ভাৰতীয় আইন অনুসৰি গ্ৰেপ্তাৰ হোৱা ব্যক্তিৰ গ্ৰেপ্তাৰৰ কাৰণ জনা আৰু ২৪ ঘণ্টাৰ ভিতৰত দণ্ডাধীশৰ ওচৰত হাজিৰ কৰোৱাৰ সাংবিধানিক অধিকাৰ আছে।"
    },

    "tenancy_refund_advice": {
        "te": "ఇంటి యజమాని అద్దె డిపాజిట్ నిరాకరిస్తే, సెక్షన్ 126 భారతీయ న్యాయ సంహిత ప్రకారం నోటీసు జారీ చేసి లీగల్ నోటీసు ద్వారా 15 రోజుల్లో పూర్తి రికవరీ పొందవచ్చు.",
        "hi": "यदि मकान मालिक सुरक्षा जमा राशि वापस करने से मना करता है, तो आप 15 दिनों का कानूनी नोटिस भेजकर उपभोक्ता आयोग या रेंट ट्रिब्यूनल में शिकायत दर्ज कर सकते हैं।",
        "en": "If your landlord refuses to refund your security deposit, serve a formal 15-day statutory legal notice under the Model Tenancy Act before approaching the Rent Court.",
        "ta": "வாடகை முன்வைப்பு தொகையை திருப்பித் தர நில உரிமையாளர் மறுத்தால், 15 நாட்கள் அவகாசத்துடன் சட்டப்பூர்வ நோட்டீஸ் அனுப்பி தீர்வு பெறலாம்.",
        "mr": "घरमालकाने डिपॉझिट परत करण्यास नकार दिल्यास, 15 दिवसांची कायदेशीर नोटीस पाठवून रेंट ट्रिब्यूनलमध्ये तक्रार दाखल करता येते.",
        "kn": "ಮನೆ ಮಾಲೀಕರು ಠೇವಣಿ ಹಣ ಹಿಂದಿರುಗಿಸಲು ನಿರಾಕರಿಸಿದರೆ, 15 ದಿನಗಳ ಕಾನೂನು ನೋಟಿಸ್ ನೀಡಿ ನ್ಯಾಯಾಲಯದಲ್ಲಿ ದಾವೆ ಹೂಡಬಹುದು.",
        "or": "ଘର ମାଲିକ ସିକ୍ୟୁରିଟି ଡିପୋଜିଟ୍ ଫେରସ୍ତ ନକଲେ, 15 ଦିନର ଆଇନଗତ ନୋଟିସ୍ ପଠାଇ ନ୍ୟାୟାଳୟରେ ଅଭିଯୋଗ କରନ୍ତୁ।",
        "as": "ঘৰৰ মালিকে ছিকিউৰিটি ডিপ'জিট ঘূৰাই নিদিলে ১৫ দিনৰ আইনী জাননী প্ৰেৰণ কৰি ভাড়াতীয়া ন্যায়াধিকৰণত গোচৰ তৰক।"
    }
}

class MultilingualLegalVoiceEngine:
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def get_legal_speech(self, topic_key: str = "cyber_fraud_advice", lang_code: str = "te") -> Dict[str, Any]:
        """Returns spoken audio and transcript in selected Indian language."""
        if lang_code not in LANG_CONFIG:
            lang_code = "te" # Default to Telangana (Telugu)

        topic_data = LEGAL_SPEECH_CATALOG.get(topic_key, LEGAL_SPEECH_CATALOG["cyber_fraud_advice"])
        text = topic_data.get(lang_code, topic_data.get("en", "Legal guidance active."))

        cache_hash = hashlib.md5(f"{topic_key}_{lang_code}_{text}".encode("utf-8")).hexdigest()
        cache_file = CACHE_DIR / f"{cache_hash}.mp3"

        if not cache_file.exists():
            success = False
            if GTTS_AVAILABLE:
                try:
                    target_gtts = LANG_CONFIG[lang_code]["gtts"]
                    tts = gTTS(text=text, lang=target_gtts, tld="co.in", timeout=4.0)
                    tts.save(str(cache_file))
                    success = True
                except Exception:
                    success = False

            if not success:
                # Synthesize acoustic wave tone as reliable fallback
                wav_file = CACHE_DIR / f"{cache_hash}.wav"
                self._synthesize_acoustic_alert(wav_file)
                cache_file = wav_file

        with open(cache_file, "rb") as f:
            audio_bytes = f.read()

        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        mime_type = "audio/wav" if cache_file.suffix == ".wav" else "audio/mp3"

        return {
            "topic_key": topic_key,
            "lang": lang_code,
            "language": LANG_CONFIG[lang_code]["name"],
            "native_name": LANG_CONFIG[lang_code]["native"],
            "spoken_text": text,
            "audio_base64": f"data:{mime_type};base64,{b64_audio}",
            "audio_url": f"data:{mime_type};base64,{b64_audio}"
        }

    def _synthesize_acoustic_alert(self, output_wav: Path):
        """Generates clear notification chime waveform when offline."""
        sample_rate = 22050
        duration = 1.2
        num_samples = int(sample_rate * duration)

        with wave.open(str(output_wav), "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)

            for i in range(num_samples):
                t = i / sample_rate
                # Dual tone: 523Hz (C5) and 659Hz (E5)
                freq = 523.25 if t < 0.6 else 659.25
                sample = int(12000 * math.sin(2 * math.pi * freq * t) * math.exp(-2.0 * (t % 0.6)))
                wav.writeframes(struct.pack("<h", max(-32768, min(32767, sample))))
