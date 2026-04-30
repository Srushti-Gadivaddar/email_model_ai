from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from scipy.sparse import hstack
from fastapi.middleware.cors import CORSMiddleware
import os

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

    is_money_request = has_payment and has_rupee and not has_stipend
    has_safe_money = has_rupee and has_stipend and has_no_fee

    has_refund_trap = any(word in text_lower for word in [
        'refundable','security deposit','will be returned','adjusted in stipend'
    ])

    # ----------- ADVANCED FEATURES -----------
    has_scam_words = any(word in text_lower for word in [
        'upi','otp','click','link','verify','account blocked','login now','bank'
    ])

    import re
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

    # ----------- FINAL DECISION LOGIC -----------

    # Rule overrides FIRST
    if is_money_request and has_whatsapp:
        final_pred = "fake"

    elif has_refund_trap:
        final_pred = "suspicious"

    elif has_stipend and has_no_fee and not is_money_request:
        final_pred = "real"

    # Then ML confidence
    elif max_prob < 0.6:
        final_pred = "suspicious"

    else:
        final_pred = pred

    reasons = []

    if is_money_request:
        reasons.append("Requests money (likely scam pattern)")
    if has_urgency:
        reasons.append("Uses urgency words")
    if has_whatsapp:
        reasons.append("Asks to contact on WhatsApp/Telegram")
    if has_refund_trap:
        reasons.append("Mentions refundable/security deposit")
    if has_scam_words:
        reasons.append("Contains scam keywords (OTP/UPI/etc)")
    if has_url:
        reasons.append("Contains URL link")
    if has_short_link:
        reasons.append("Uses shortened link")
    if has_fake_domain:
        reasons.append("Looks like fake domain")
    if has_stipend and has_no_fee:
        reasons.append("Mentions stipend with no fee")

    # Remove duplicates
    reasons = list(set(reasons))

    # Fallback reason
    if not reasons:
        if final_pred == "real":
            reasons.append("Looks like a legitimate informational email")
        elif final_pred == "fake":
            reasons.append("Likely scam based on patterns")
        else:
            reasons.append("Model uncertain - requires manual verification")

    return {
        "prediction": final_pred,
        "confidence": float(max_prob),
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


