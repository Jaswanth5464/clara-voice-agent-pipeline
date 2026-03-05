# 🎙️ Clara Answers — Onboarding Automation Pipeline

> An end-to-end automation pipeline that converts raw call transcripts into production-ready AI voice agent configurations for Clara Answers — a voice agent platform serving fire protection, sprinkler, electrical, HVAC, and facility management companies.

---


VideoLink:
https://drive.google.com/file/d/1ScQcM9VPlkAut_LGgtUtQH6WcKYyds8N/view?usp=sharing



## 📸 Screenshots



---

### 1. Dashboard — Full Overview

<img width="1130" height="592" alt="image" src="https://github.com/user-attachments/assets/d22f29df-5138-4651-80f9-af0121f5bc97" />







---

### 2. Dashboard — Pipeline Summary + Open Unknowns







<img width="1288" height="565" alt="image" src="https://github.com/user-attachments/assets/35950489-3d9b-45b6-ac6a-aaedea39cec0" />

---

### 3. Dashboard — Diff Viewer

<img width="805" height="517" alt="image" src="https://github.com/user-attachments/assets/95a105f7-d4f4-437f-b3d2-aa41dcab493e" />

---

### 4. n8n Pipeline A — Full Canvas

<img width="1298" height="478" alt="image" src="https://github.com/user-attachments/assets/7d0c1726-2d54-4b04-aa7c-1901617282f3" />


---

### 5. n8n Pipeline B — Full Canvas

<img width="1255" height="410" alt="image" src="https://github.com/user-attachments/assets/77b40d22-c406-457e-b93b-dd5ca7ab2699" />

---

### 6. Batch Runner — Terminal Output


<img width="790" height="462" alt="image" src="https://github.com/user-attachments/assets/a1aa482a-bc5e-4050-855f-56958e2d96cf" />


<img width="794" height="403" alt="image" src="https://github.com/user-attachments/assets/faf85c96-97a3-4711-bac5-fc5bdff42016" />


---

### 7. Output Folder Structure

<img width="896" height="377" alt="image" src="https://github.com/user-attachments/assets/5248ebcf-5982-4a71-9dc7-0dd9091b3cf1" />




<img width="947" height="344" alt="image" src="https://github.com/user-attachments/assets/06e58b0b-d187-4ef4-aed9-96ac7bbff592" />




<img width="827" height="345" alt="image" src="https://github.com/user-attachments/assets/069e3960-49ed-4a00-838b-8e9b5f6f9160" />





<img width="1055" height="300" alt="image" src="https://github.com/user-attachments/assets/07565c69-fc5e-4cce-8404-058a94b7b8cd" />



---

## 📌 What This Does

This pipeline automates the entire Clara onboarding workflow:

```
Demo Call Transcript
        ↓
Pipeline A (n8n + Gemini AI)
        ↓
account_memo_v1.json + agent_spec_v1.json
        ↓
Onboarding Call Transcript
        ↓
Pipeline B (n8n + Gemini AI)
        ↓
account_memo_v2.json + agent_spec_v2.json + changelog.json
        ↓
Live Dashboard (real-time visibility)
```

No manual configuration. No hallucinated data. Every missing field is explicitly flagged.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  INPUT LAYER                            │
│   demo_transcript.txt   onboarding_transcript.txt       │
└────────────────┬───────────────────┬────────────────────┘
                 │                   │
        Pipeline A               Pipeline B
                 │                   │
┌────────────────▼───────────────────▼────────────────────┐
│               n8n ORCHESTRATION LAYER                   │
│                                                         │
│  [Read File] → [Extract Text] → [Gemini AI]             │
│       → [Format JSON] → [Write Files]                   │
└────────────────────────────────┬────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────┐
│                  OUTPUT LAYER                           │
│                                                         │
│  outputs/accounts/<account_id>/                         │
│    ├── v1/account_memo.json                             │
│    ├── v1/agent_spec.json                               │
│    ├── v2/account_memo.json                             │
│    ├── v2/agent_spec.json                               │
│    └── changelog/changelog.json                         │
└────────────────────────────────┬────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────┐
│              DASHBOARD LAYER                            │
│   Python server (server.py) reads JSON files            │
│   dashboard.html displays live data                     │
│   Diff viewer shows v1 → v2 changes                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
clara-answers-pipeline/
│
├── README.md                          ← You are here
│
├── workflows/
│   ├── pipeline_a_demo.json           ← n8n Pipeline A export
│   └── pipeline_b_onboarding.json     ← n8n Pipeline B export
│
├── scripts/
│   ├── run_all.py                     ← Batch runner (all 5 accounts)
│   └── server.py                      ← Dashboard data server
│
├── dashboard/
│   └── dashboard.html                 ← Live pipeline dashboard
│
├── outputs/
│   └── accounts/
│       ├── account_001/
│       │   ├── v1/
│       │   │   ├── account_memo.json
│       │   │   └── agent_spec.json
│       │   ├── v2/
│       │   │   ├── account_memo.json
│       │   │   └── agent_spec.json
│       │   └── changelog/
│       │       └── changelog.json
│       ├── account_002/  (same structure)
│       ├── account_003/  (same structure)
│       ├── account_004/  (same structure)
│       └── account_005/  (same structure)
│
└── transcripts/
    ├── demo/
    │   ├── account_001_demo.txt
    │   ├── account_002_demo.txt
    │   ├── account_003_demo.txt
    │   ├── account_004_demo.txt
    │   └── account_005_demo.txt
    └── onboarding/
        ├── account_001_onboarding.txt
        ├── account_002_onboarding.txt
        ├── account_003_onboarding.txt
        ├── account_004_onboarding.txt
        └── account_005_onboarding.txt
```

---

## ⚙️ Setup Instructions

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| n8n | 2.3.2+ | Workflow orchestration |
| Python | 3.8+ | Batch runner + dashboard server |
| Gemini API | Free tier | AI extraction + generation |
| Node.js | 18+ | Required by n8n |

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/clara-answers-pipeline.git
cd clara-answers-pipeline
```

---

### Step 2 — Set Up n8n (Local)

```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start

# Open in browser
http://localhost:5678
```

---

### Step 3 — Configure n8n File Access

n8n only allows file access from its designated folder. Copy all files there:

**Windows:**
```powershell
# Create required folders
mkdir C:\Users\<your-username>\.n8n-files\transcripts\demo
mkdir C:\Users\<your-username>\.n8n-files\transcripts\onboarding
mkdir C:\Users\<your-username>\.n8n-files\outputs\accounts\account_001\v1
mkdir C:\Users\<your-username>\.n8n-files\outputs\accounts\account_001\v2
mkdir C:\Users\<your-username>\.n8n-files\outputs\accounts\account_001\changelog
# Repeat for accounts 002-005

# Copy transcripts
copy transcripts\demo\* C:\Users\<your-username>\.n8n-files\transcripts\demo\
copy transcripts\onboarding\* C:\Users\<your-username>\.n8n-files\transcripts\onboarding\
```

---

### Step 4 — Import n8n Workflows

```
1. Open n8n → http://localhost:5678
2. Click "+" → New Workflow
3. Click "..." top right → Import
4. Select workflows/pipeline_a_demo.json
5. Update file paths to match your username
6. Repeat for pipeline_b_onboarding.json
```

---

### Step 5 — Set Up Gemini API Key

```
1. Go to https://aistudio.google.com/app/apikey
2. Create a free API key
3. In n8n → Credentials → Add Google Gemini(PaLM) API
4. Paste your API key
5. Save
```

---

### Step 6 — Install Python Dependencies

```bash
pip install requests
```

---

## 🚀 How to Run

### Option A — Run Single Account via n8n (Visual)

```
1. Open Pipeline A in n8n
2. Click "Execute Workflow"
3. Opens Pipeline B
4. Click "Execute Workflow"
```

### Option B — Run All 5 Accounts via Batch Script

```bash
python scripts/run_all.py --api-key YOUR_GEMINI_API_KEY
```

**Additional options:**
```bash
# Run only Pipeline A (demo → v1)
python scripts/run_all.py --api-key YOUR_KEY --pipeline a

# Run only Pipeline B (onboarding → v2)
python scripts/run_all.py --api-key YOUR_KEY --pipeline b

# Force reprocess even if files exist
python scripts/run_all.py --api-key YOUR_KEY --force
```

**Expected output:**
```
🎙️ Clara Answers — Batch Pipeline Runner
   Processing 5 accounts

✅ account_001 Pipeline A complete!
✅ account_002 Pipeline A complete!
...

📊 BATCH RUN SUMMARY
─────────────────────────────────────
Account         Pipeline A    Pipeline B
account_001     ✅ Done       ✅ Done
account_002     ✅ Done       ✅ Done
account_003     ✅ Done       ✅ Done
account_004     ✅ Done       ✅ Done
account_005     ✅ Done       ✅ Done
─────────────────────────────────────
Pipeline A: 5/5 accounts processed
Pipeline B: 5/5 accounts processed
```

---

## 📊 How to View the Dashboard

### Step 1 — Start the data server
```bash
python scripts/server.py
```

### Step 2 — Open the dashboard
```
Open dashboard/dashboard.html in your browser
```

### Dashboard Features:
- **Stats cards** — total accounts, v2 complete, pending, open unknowns
- **Pipeline table** — all accounts with version, status, confidence score
- **v1/v2 buttons** — view raw JSON memo for each version
- **Diff button** — side-by-side changelog viewer (green = added, red = before)
- **Open unknowns panel** — all missing fields flagged per account
- **Pipeline summary** — total fields extracted, avg confidence, changelogs

---

## 📋 Output Format

### account_memo.json
```json
{
  "account_id": "account_001",
  "company_name": "Apex Fire Protection",
  "version": "v1",
  "source": "demo_call",
  "business_hours": {
    "confirmed": false,
    "days": null,
    "timezone": null,
    "note": "NOT MENTIONED in demo call"
  },
  "emergency_definition": ["sprinkler leak", "fire alarm"],
  "emergency_routing_rules": {
    "primary_contact": {"name": null, "phone": null},
    "fallback_contact": {"name": null, "phone": null}
  },
  "questions_or_unknowns": [
    "Business hours not stated",
    "Emergency contact number missing"
  ]
}
```

### agent_spec.json
```json
{
  "agent_name": "Clara — Apex Fire Protection",
  "version": "v1",
  "voice_style": {"tone": "warm", "pace": "natural"},
  "system_prompt": "You are Clara... [full script]",
  "call_transfer_protocol": {...},
  "fallback_protocol": {...}
}
```

### changelog.json
```json
{
  "from_version": "v1",
  "to_version": "v2",
  "summary": "6 fields confirmed during onboarding",
  "changes": [
    {
      "field": "business_hours",
      "change_type": "CONFIRMED",
      "before": "UNKNOWN",
      "after": "Mon-Fri 08:00-17:00 EST",
      "reason": "Confirmed on onboarding call"
    }
  ],
  "resolved_unknowns": ["Business hours confirmed"],
  "remaining_unknowns": []
}
```

---

## 🔄 Pipeline Flow Detail

### Pipeline A — Demo Call → v1

| Step | Node | Action |
|------|------|--------|
| 1 | Read File | Read demo transcript from disk |
| 2 | Extract from File | Convert binary to text |
| 3 | Gemini AI | Extract company info into structured JSON |
| 4 | Code | Clean + format + add metadata |
| 5 | Write File | Save account_memo.json |
| 6 | Gemini AI | Generate Clara voice agent script |
| 7 | Code | Clean + format agent spec |
| 8 | Write File | Save agent_spec.json |

### Pipeline B — Onboarding → v2 + Changelog

| Step | Node | Action |
|------|------|--------|
| 1 | Read File | Read onboarding transcript |
| 2 | Extract from File | Convert to text |
| 3 | Read File | Read existing v1 memo |
| 4 | Extract from File | Convert to text |
| 5 | Gemini AI | Compare v1 + transcript → generate v2 + changelog |
| 6 | Code | Split v2_memo and changelog, format both |
| 7 | Write File | Save v2/account_memo.json |
| 8 | Write File | Save changelog/changelog.json |
| 9 | Write File | Save v2/agent_spec.json |

---

## 🧠 Prompt Hygiene

The generated agent prompt follows strict conversation hygiene:

**Business Hours Flow:**
1. Warm greeting with company name
2. Ask purpose of call
3. Collect caller name and phone number
4. Transfer to appropriate contact
5. If transfer fails → apologize and assure callback
6. Ask if anything else needed
7. Close call politely

**After Hours Flow:**
1. Greeting mentioning closed
2. Ask purpose of call
3. Confirm if emergency
4. If emergency → collect name, number, address → transfer immediately
5. If transfer fails → apologize, assure urgent callback
6. If non-emergency → collect details, confirm next-day callback
7. Ask if anything else needed
8. Close call politely

**Strict Rules Enforced:**
- Never mention function calls or tools to caller
- Never claim to be human or AI unless asked
- Never invent contact details not in the memo
- Sound warm, calm and professional at all times

---

## ✅ Assignment Checklist

| Requirement | Status |
|-------------|--------|
| Pipeline A — demo → v1 | ✅ Done |
| Pipeline B — onboarding → v2 | ✅ Done |
| account_memo.json per account | ✅ Done |
| agent_spec.json per account | ✅ Done |
| changelog.json per account | ✅ Done |
| questions_or_unknowns handling | ✅ Done |
| No hallucination of missing data | ✅ Done |
| Versioning v1 → v2 | ✅ Done |
| n8n workflow exports | ✅ Done |
| Batch runner script | ✅ Done |
| Idempotent (skip if exists) | ✅ Done |
| Dashboard UI | ✅ Bonus |
| Diff viewer | ✅ Bonus |
| Confidence scores | ✅ Bonus |
| Batch summary metrics | ✅ Bonus |

---

## ⚠️ Known Limitations

1. **n8n file access** — n8n only reads/writes from `~/.n8n-files/` on local setup. In production, replace with cloud storage (S3, Google Drive).

2. **Gemini free tier** — Rate limits may slow batch processing. Add `time.sleep(2)` between calls if hitting limits.

3. **Sample transcripts** — The 5 transcripts used are representative samples. Real production transcripts from actual demo calls will produce richer extractions.

4. **Retell API** — Retell does not offer free programmatic agent creation. The `agent_spec.json` output is designed to be manually imported into Retell UI or used via their paid API in production.

5. **Single file storage** — Outputs are stored as local JSON files. In production, replace with Supabase or PostgreSQL for multi-user access.

---

## 🚀 What I Would Improve With Production Access

1. **Retell API integration** — Auto-create and update agents via Retell API instead of manual import
2. **Supabase backend** — Replace local JSON files with a proper database for multi-user, concurrent access
3. **Webhook triggers** — Trigger pipelines automatically when new call recordings land in storage
4. **Audio transcription** — Add Whisper transcription node so pipeline accepts raw audio files
5. **Confidence thresholds** — Auto-flag accounts below 70% confidence for human review
6. **Slack notifications** — Notify team when new account is onboarded or unknowns are detected
7. **Retell agent testing** — Auto-test generated prompts against sample calls before deployment

---

## 🎥 Demo Video

[Watch the pipeline demo on Loom](https://drive.google.com/file/d/1ScQcM9VPlkAut_LGgtUtQH6WcKYyds8N/view?usp=sharing) ← Add your Loom link here

---

## 📞 Contact

Built as part of Clara Answers Intern Assignment.

---

*This pipeline is zero-cost. No paid APIs, subscriptions, or services were used.*
