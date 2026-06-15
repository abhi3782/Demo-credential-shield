import streamlit as st
import time
import google.generativeai as genai

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DHL CredentialShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── DHL Brand CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  :root {
    --dhl-red:    #D40511;
    --dhl-yellow: #FFCC00;
    --dhl-dark:   #1A1A1A;
    --dhl-grey:   #F5F5F5;
    --dhl-mid:    #6B6B6B;
  }

  #MainMenu, footer, header { visibility: hidden; }

  .top-banner {
    background: var(--dhl-red);
    color: white;
    padding: 14px 28px;
    border-radius: 10px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .top-banner .logo { font-size: 2rem; font-weight: 700; color: var(--dhl-yellow); letter-spacing: -1px; }
  .top-banner .title { font-size: 1.15rem; font-weight: 500; }
  .top-banner .badge {
    margin-left: auto;
    background: var(--dhl-yellow);
    color: var(--dhl-dark);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  .section-card {
    background: white;
    border: 1px solid #E8E8E8;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  .section-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--dhl-mid);
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  .risk-critical { background:#FFEAEA; color:#C0000C; border:1px solid #F5AAAA; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .risk-high     { background:#FFF3E0; color:#E65100; border:1px solid #FFCC80; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .risk-medium   { background:#FFFDE7; color:#827717; border:1px solid #FFF176; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .risk-low      { background:#E8F5E9; color:#1B5E20; border:1px solid #A5D6A7; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }

  .email-preview {
    background: #FAFAFA;
    border: 1px solid #DCDCDC;
    border-radius: 10px;
    padding: 22px 26px;
    font-size: 0.88rem;
    line-height: 1.75;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
    color: #2A2A2A;
  }
  .email-subject {
    background: var(--dhl-yellow);
    color: var(--dhl-dark);
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.82rem;
    display: inline-block;
    margin-bottom: 14px;
  }

  .metric-row { display:flex; gap:14px; margin-bottom:20px; flex-wrap:wrap; }
  .metric-tile {
    flex:1; min-width:120px;
    background: white;
    border: 1px solid #E8E8E8;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .metric-value { font-size:1.6rem; font-weight:700; color: var(--dhl-red); }
  .metric-label { font-size:0.72rem; color: var(--dhl-mid); font-weight:500; margin-top:2px; }

  .stButton > button {
    background: var(--dhl-red) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 0.9rem !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.88 !important; }

  .disclaimer {
    background: #FFF8E1;
    border-left: 4px solid var(--dhl-yellow);
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 0.78rem;
    color: #5A4A00;
    margin-bottom: 20px;
  }

  .compare-label {
    font-size: 0.72rem; font-weight:700; letter-spacing:1px;
    text-transform:uppercase; margin-bottom:8px;
  }
  .before-label { color: #888; }
  .after-label  { color: var(--dhl-red); }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
  <span class="logo">DHL</span>
  <div>
    <div class="title">CredentialShield AI &nbsp;🛡️</div>
    <div style="font-size:0.75rem;opacity:0.8">Dark Web Breach Response · Powered by Gemini AI</div>
  </div>
  <div class="badge">⚠️ DEMO — SIMULATED DATA ONLY</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="disclaimer">🔒 <strong>Demo Notice:</strong> All customer profiles below are entirely fictitious and generated for demonstration purposes. No real DHL customer data is used or stored in this application.</div>', unsafe_allow_html=True)

# ── Simulated breach data ───────────────────────────────────────────────────────
MOCK_CUSTOMERS = [
    {
        "id": "C-001",
        "name": "Müller GmbH",
        "email": "logistics@mueller-gmbh.de",
        "type": "Business — Pharmaceutical Shipper",
        "country": "Germany",
        "account_tier": "Premium",
        "mfa_enabled": False,
        "last_login": "2 days ago",
        "shipments_/month": 340,
        "breach_source": "SteelerDB leak (June 2026)",
        "risk": "Critical",
    },
    {
        "id": "C-002",
        "name": "Sarah Chen",
        "email": "sarah.chen@email.sg",
        "type": "Personal — Frequent Shopper",
        "country": "Singapore",
        "account_tier": "Standard",
        "mfa_enabled": True,
        "last_login": "12 hours ago",
        "shipments_/month": 8,
        "breach_source": "ComboList_Asia_2026",
        "risk": "Medium",
    },
    {
        "id": "C-003",
        "name": "Patel Exports Ltd",
        "email": "admin@patelexports.in",
        "type": "Business — SME Exporter",
        "country": "India",
        "account_tier": "Business",
        "mfa_enabled": False,
        "last_login": "45 days ago",
        "shipments_/month": 120,
        "breach_source": "RaidForums repost (old breach)",
        "risk": "High",
    },
    {
        "id": "C-004",
        "name": "Carlos Rivera",
        "email": "c.rivera@correo.mx",
        "type": "Personal — Occasional User",
        "country": "Mexico",
        "account_tier": "Standard",
        "mfa_enabled": False,
        "last_login": "6 months ago",
        "shipments_/month": 1,
        "breach_source": "SteelerDB leak (June 2026)",
        "risk": "Low",
    },
]

RISK_COLORS = {
    "Critical": "risk-critical",
    "High": "risk-high",
    "Medium": "risk-medium",
    "Low": "risk-low",
}

# ── Layout ──────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔑 Google Gemini API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="AIzaSy...", label_visibility="collapsed")
    if not api_key:
        st.caption("Get your free key → aistudio.google.com")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-row">
      <div class="metric-tile"><div class="metric-value">4</div><div class="metric-label">Accounts at Risk</div></div>
      <div class="metric-tile"><div class="metric-value">2</div><div class="metric-label">Critical / High</div></div>
      <div class="metric-tile"><div class="metric-value">3</div><div class="metric-label">No MFA Enabled</div></div>
      <div class="metric-tile"><div class="metric-value">220+</div><div class="metric-label">Countries Covered</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Select Affected Customer</div>', unsafe_allow_html=True)

    selected_name = st.selectbox(
        "",
        [f"{c['id']} · {c['name']} ({c['country']})" for c in MOCK_CUSTOMERS],
        label_visibility="collapsed",
    )
    selected = MOCK_CUSTOMERS[[c['id'] for c in MOCK_CUSTOMERS].index(selected_name.split(" · ")[0])]

    risk_cls = RISK_COLORS[selected["risk"]]
    st.markdown(f"""
    <div style="background:#F9F9F9;border-radius:8px;padding:14px 16px;margin-top:10px;font-size:0.83rem;line-height:2">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <strong style="font-size:1rem">{selected['name']}</strong>
        <span class="{risk_cls}">{selected['risk']} Risk</span>
      </div>
      <div>📧 {selected['email']}</div>
      <div>🌏 {selected['country']} &nbsp;·&nbsp; {selected['type']}</div>
      <div>🏷️ {selected['account_tier']} account &nbsp;·&nbsp; Last login: {selected['last_login']}</div>
      <div>📦 {selected['shipments_/month']} shipments/mo &nbsp;·&nbsp; MFA: {'✅ On' if selected['mfa_enabled'] else '❌ Off'}</div>
      <div>🔍 Breach source: <em>{selected['breach_source']}</em></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌐 Email Language</div>', unsafe_allow_html=True)
    language = st.selectbox("", ["English", "German", "Spanish", "Hindi", "French", "Mandarin Chinese"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎚️ Tone</div>', unsafe_allow_html=True)
    tone = st.radio("", ["Urgent & Direct", "Professional & Calm", "Friendly & Reassuring"], label_visibility="collapsed", horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    generate_btn = st.button("⚡ Generate AI Security Alert", use_container_width=True)

with col_right:

    if not generate_btn:
        st.markdown("""
        <div class="section-card" style="text-align:center;padding:60px 30px;color:#AAA;">
          <div style="font-size:2.5rem;margin-bottom:12px">🛡️</div>
          <div style="font-size:1rem;font-weight:600;color:#555">Select a customer and click Generate</div>
          <div style="font-size:0.82rem;margin-top:8px">AI will produce a personalised security alert email<br>tailored to their account profile, region, and risk level.</div>
        </div>
        """, unsafe_allow_html=True)

    elif not api_key:
        st.error("Please enter your Google Gemini API key in the left panel.")

    else:
        prompt = f"""You are a senior cybersecurity communications specialist at DHL Express, responsible for customer data protection across 220+ countries.

A dark web credential monitoring system has detected that the following DHL customer's credentials appear in a breach database. Write a personalised security alert email to this customer.

CUSTOMER PROFILE:
- Name: {selected['name']}
- Email: {selected['email']}
- Account Type: {selected['type']}
- Country/Region: {selected['country']}
- Account Tier: {selected['account_tier']}
- MFA Enabled: {selected['mfa_enabled']}
- Last Login: {selected['last_login']}
- Monthly Shipments: {selected['shipments_/month']}
- Breach Source: {selected['breach_source']}
- Risk Level: {selected['risk']}

REQUIREMENTS:
1. Write in {language}
2. Tone: {tone}
3. Personalise based on account type (business vs personal) and risk level
4. If MFA is NOT enabled, make enabling it the #1 call to action
5. If it IS enabled, reassure them their account has an extra layer of protection
6. For business/premium accounts, acknowledge the business impact (shipment continuity)
7. For dormant accounts (last login > 30 days), use gentler urgency
8. Include 3-5 concrete best practice tips relevant to their profile
9. End with a clear, single primary action button placeholder: [RESET PASSWORD NOW]
10. Sign off as "DHL Express Security Team"

ALSO PROVIDE (after the email, separated by ---ANALYSIS---):
A 3-bullet AI analysis explaining:
• Why this email is personalised differently from a generic blast
• What risk factors drove the tone and content choices
• What the human reviewer should verify before sending

Keep the email professional, on-brand for DHL, and avoid alarmist language that could cause panic."""

        with st.spinner("🤖 Gemini AI is crafting your personalised security alert..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                t0 = time.time()
                response = model.generate_content(prompt)
                elapsed = round(time.time() - t0, 1)
                full_text = response.text

                parts = full_text.split("---ANALYSIS---")
                email_body = parts[0].strip()
                analysis = parts[1].strip() if len(parts) > 1 else ""

                subject_line = "Urgent: Action Required — Your DHL Account Security"
                lines = email_body.split("\n")
                for i, line in enumerate(lines):
                    if line.lower().startswith("subject:"):
                        subject_line = line.replace("Subject:", "").replace("subject:", "").strip()
                        email_body = "\n".join(lines[i+1:]).strip()
                        break

                tab1, tab2 = st.tabs(["📧 Generated Email", "⚡ Before / After Comparison"])

                with tab1:
                    st.markdown(f"""
                    <div class="section-card">
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
                        <div class="section-title" style="margin-bottom:0">AI-Generated Security Alert</div>
                        <div style="font-size:0.75rem;color:#888">Generated in {elapsed}s · {language} · {tone}</div>
                      </div>
                      <div class="email-subject">📨 Subject: {subject_line}</div>
                      <div class="email-preview">{email_body}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if analysis:
                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">🧠 AI Personalisation Analysis</div>', unsafe_allow_html=True)
                        for line in analysis.split("\n"):
                            if line.strip().startswith("•"):
                                st.markdown(f"<div style='padding:6px 0;font-size:0.85rem;border-bottom:1px solid #F0F0F0'>{line.strip()}</div>", unsafe_allow_html=True)
                        st.markdown("""
                        <div style="background:#FFF3CD;border-radius:8px;padding:12px 16px;margin-top:14px;font-size:0.8rem">
                          ⚠️ <strong>Human-in-the-Loop:</strong> This email requires review and approval before sending.
                          AI drafts — humans decide.
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                with tab2:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Generic Blast vs AI-Personalised — The Difference</div>', unsafe_allow_html=True)
                    b_col, a_col = st.columns(2, gap="medium")
                    with b_col:
                        st.markdown('<div class="compare-label before-label">❌ BEFORE — Generic Template</div>', unsafe_allow_html=True)
                        st.markdown("""
                        <div class="email-preview" style="border-color:#FFAAAA;background:#FFFAFA;font-size:0.8rem">Dear Customer,

We have detected that your credentials may have appeared in a data breach.

Please reset your password immediately by clicking the link below.

[RESET PASSWORD]

We apologise for any inconvenience.

DHL Security Team</div>
                        """, unsafe_allow_html=True)
                        st.markdown("""
                        <div style="margin-top:10px;font-size:0.78rem;color:#888">
                        ❌ No personalisation<br>
                        ❌ Same for all customers<br>
                        ❌ No MFA guidance<br>
                        ❌ No risk context<br>
                        ❌ English-only
                        </div>
                        """, unsafe_allow_html=True)

                    with a_col:
                        st.markdown('<div class="compare-label after-label">✅ AFTER — AI-Personalised</div>', unsafe_allow_html=True)
                        preview = email_body[:420] + "..." if len(email_body) > 420 else email_body
                        st.markdown(f"""
                        <div class="email-preview" style="border-color:#AADDAA;background:#F8FFF8;font-size:0.8rem">{preview}</div>
                        """, unsafe_allow_html=True)
                        mfa_point = "Prioritises MFA setup" if not selected['mfa_enabled'] else "Acknowledges MFA protection"
                        st.markdown(f"""
                        <div style="margin-top:10px;font-size:0.78rem;color:#2E7D32">
                        ✅ Personalised to {selected['type']}<br>
                        ✅ {selected['risk']} risk tone applied<br>
                        ✅ {mfa_point}<br>
                        ✅ {language} language<br>
                        ✅ Business impact addressed
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                err = str(e)
                if "API_KEY_INVALID" in err or "invalid" in err.lower():
                    st.error("❌ Invalid API key. Please check and re-enter your Gemini key from aistudio.google.com")
                elif "quota" in err.lower():
                    st.error("⚠️ Free quota exceeded. Wait a minute and try again — Gemini free tier resets every 60 seconds.")
                else:
                    st.error(f"Something went wrong: {e}")

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:30px 0 10px;font-size:0.75rem;color:#BBB">
  DHL CredentialShield AI · Built as an AI PM Portfolio Demo · All data simulated · No real customer data used
</div>
""", unsafe_allow_html=True)
