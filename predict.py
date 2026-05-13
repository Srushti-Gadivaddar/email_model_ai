from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from scipy.sparse import hstack
from fastapi.middleware.cors import CORSMiddleware
import os
import re



app = FastAPI()

port = int(os.environ.get("PORT", 10000))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and vectorizer
model = joblib.load("email_model_final.pkl")
print("Model loaded successfully")
tfidf = joblib.load("tfidf_vectorizer_final.pkl")
print("Vectorizer loaded successfully") 


def predict_email(text):

    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    text_lower = text.lower()
    
    # ----------- BASIC FEATURES -----------
    has_payment = (
        any(word in text_lower for word in [
            'pay','fee','amount','charge','payment','deposit'
        ])
        and not any(word in text_lower for word in [
            'no fee','no payment','no charges'
        ])
    )

    has_rupee = any(sym in text_lower for sym in ['₹','rs','inr'])

    has_urgency = any(word in text_lower for word in [
        'urgent','hurry','limited','24 hours','deadline','act fast'
    ])

    has_whatsapp = any(word in text_lower for word in [
        'whatsapp','telegram','dm','contact hr'
    ])

    has_stipend = any(word in text_lower for word in [
        'stipend','salary','per month','lpa','ctc'
    ])

    has_no_fee = any(word in text_lower for word in [
        'no fee','no payment','free','no charges'
    ])
    
    has_professional_language = any(word in text_lower for word in [
        'regards',
        'hr manager',
        'selection process',
        'internship program',
        'department',
        'hybrid',
        'location'
    ])

    has_official_structure = (
        'position:' in text_lower
        or 'department:' in text_lower
        or 'location:' in text_lower
    )

    has_legit_company_words = any(word in text_lower for word in [
        'technologies',
        'solutions',
        'private limited',
        'official'
    ])

    is_money_request = has_payment and has_rupee and not has_stipend
    has_safe_money = has_rupee and has_stipend and has_no_fee

    has_refund_trap = any(word in text_lower for word in [
        'refundable','security deposit','will be returned','adjusted in stipend'
    ])

    # ----------- ADVANCED FEATURES -----------
    has_scam_words = any(word in text_lower for word in [
        'upi','otp','click','link','verify','account blocked','login now','bank'
    ])

    has_url = bool(re.search(r'http[s]?://|www\.', text_lower))

    has_short_link = any(link in text_lower for link in [
        'bit.ly','tinyurl','goo.gl','t.co'
    ])

    has_fake_domain = any(word in text_lower for word in [
        'g00gle','micr0soft','amaz0n'
    ])

    # ----------- FEATURE VECTOR -----------
    extra = [[
        int(is_money_request),
        int(has_urgency),
        int(has_whatsapp),
        int(has_stipend and has_no_fee),
        int(any(word in text_lower for word in [
            'google','microsoft','amazon','tcs','infosys','wipro','mnc'
        ])),
        int(has_no_fee),
        int(has_safe_money),
        int(has_refund_trap),
        int(has_scam_words),
        int(has_url),
        int(has_short_link),
        int(has_fake_domain)
    ]]

    from scipy.sparse import hstack
    text_vec = tfidf.transform([text])
    final = hstack([text_vec, extra])

    pred = model.predict(final)[0]
    prob = model.predict_proba(final)[0]
    max_prob = max(prob)
    
        # Rule overrides FIRST
    if is_money_request and has_whatsapp:
        final_pred = "fake"

    elif has_refund_trap:
        final_pred = "suspicious"

    elif (
        has_stipend
        and not is_money_request
        and not has_whatsapp
        and not has_short_link
        and has_professional_language
        and has_official_structure
    ):
        final_pred = "real"

    # Then ML confidence
    elif max_prob < 0.6:
        final_pred = "suspicious"

    else:
        final_pred = pred

    reasons = []

    if is_money_request:
        reasons.append({
            "title": "Payment Request",
            "description": "This email asks for money, registration fee, or payment.",
            "severity": "high"
    })

    if has_urgency:
        reasons.append({
            "title": "Urgency / Pressure",
            "description": "The message creates urgency to force quick action.",
            "severity": "medium"
    })

    if has_whatsapp:
        reasons.append({
            "title": "External Contact Request",
            "description": "The sender asks to continue communication on WhatsApp or Telegram.",
            "severity": "medium"
    })

    if has_refund_trap:
        reasons.append({
            "title": "Refundable Deposit Trap",
            "description": "Mentions refundable or security deposit patterns often used in scams.",
            "severity": "high"
    })

    if has_scam_words:
        reasons.append({
            "title": "Scam Keywords Detected",
            "description": "Contains suspicious terms like OTP, UPI, verify, or login request.",
            "severity": "medium"
    })

    if has_url:
        reasons.append({
            "title": "Contains External Link",
            "description": "Email includes external URLs which may redirect users.",
            "severity": "low"
    })

    if has_short_link:
        reasons.append({
            "title": "Shortened URL Detected",
            "description": "Uses shortened links that may hide phishing websites.",
            "severity": "high"
    })

    if has_fake_domain:
        reasons.append({
            "title": "Suspicious Domain",
            "description": "Possible fake or impersonated company domain detected.",
            "severity": "high"
    })

    if has_stipend and has_no_fee:
        reasons.append({
            "title": "No Payment Required",
            "description": "Mentions stipend/salary and clearly states no payment required.",
            "severity": "safe"
    })
        
    if has_professional_language:
        reasons.append({
            "title": "Professional Email Structure",
            "description": "The email uses formal internship and company communication patterns.",
            "severity": "safe"
    })
        
    if has_official_structure:
        reasons.append({
            "title": "Official Internship Details",
            "description": "Contains structured internship information like department and location.",
            "severity": "safe"
    })    
    
    if has_legit_company_words:
        reasons.append({
            "title": "Recognized Company Indicators",
            "description": "Contains company naming patterns commonly seen in legitimate organizations.",
            "severity": "safe"
    })        
        
    #threat score calculation
    if final_pred == "real":
        threat_score = int((1 - max_prob) * 40)
    elif final_pred == "suspicious":
        threat_score = int(max_prob * 70)
    else:
        threat_score = int(max_prob * 100)    
        
    if is_money_request:
        threat_score += 15

    if has_short_link:
        threat_score += 10

    if has_fake_domain:
        threat_score += 15

    if has_whatsapp:
        threat_score += 10

    threat_score = min(threat_score, 100)    

    # Fallback reason
    if not reasons:

        if final_pred == "real":
            reasons.append({
                "title": "Looks Legitimate",
                "description": "No major scam indicators detected.",
                "severity": "safe"
            })

        elif final_pred == "fake":
            reasons.append({
                "title": "Suspicious Pattern Detected",
                "description": "The email matches multiple scam-related behavioral patterns.",
                "severity": "high"
            })

        else:
            reasons.append({
                "title": "Needs Manual Verification",
                "description": "The model confidence is uncertain for this email.",
                "severity": "medium"
            })

    return {
        "prediction": final_pred,
        "confidence": round(float(max_prob), 2),
        "threat_score": threat_score,
        "reasons": reasons
    }


class EmailRequest(BaseModel):
    text: str
    
@app.post("/predict")
def predict(req: EmailRequest | dict):
    if isinstance(req, dict):
        text = req.get("text")
    else:
        text = req.text

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    return predict_email(text)


