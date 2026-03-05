"""
Clara Answers — Batch Pipeline Runner
=====================================
Processes all demo + onboarding transcripts automatically.
Generates v1, v2, and changelog for all accounts.

Usage:
    python run_all.py --api-key YOUR_GEMINI_API_KEY

Requirements:
    pip install requests
"""

import os
import json
import argparse
import requests
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────

BASE_PATH     = r"C:\Users\kanam\.n8n-files"
TRANSCRIPTS   = os.path.join(BASE_PATH, "transcripts")
OUTPUTS       = os.path.join(BASE_PATH, "outputs", "accounts")
GEMINI_URL    = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

ACCOUNTS = [
    "account_001",
    "account_002",
    "account_003",
    "account_004",
    "account_005",
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg, status="INFO"):
    icons = {"INFO": "ℹ️ ", "OK": "✅", "SKIP": "⏭️ ", "FAIL": "❌", "START": "🚀"}
    print(f"{icons.get(status, '  ')} {msg}")

def call_gemini(api_key, prompt):
    """Send a prompt to Gemini and return the text response."""
    response = requests.post(
        f"{GEMINI_URL}?key={api_key}",
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def clean_json(text):
    """Remove markdown code fences and parse JSON."""
    cleaned = text.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)

def save_json(path, data):
    """Save a dict as a formatted JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def read_file(path):
    """Read a text file and return its content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ─── Prompts ──────────────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """
You are a data extraction assistant for Clara Answers, an AI voice agent platform.

Extract structured information from the following demo call transcript and return ONLY a valid JSON object with these exact fields:

{{
  "company_name": "",
  "business_hours": {{
    "confirmed": false,
    "days": null,
    "start": null,
    "end": null,
    "timezone": null,
    "note": ""
  }},
  "office_address": null,
  "services_supported": [],
  "emergency_definition": [],
  "emergency_routing_rules": {{
    "confirmed": false,
    "primary_contact": {{"name": null, "phone": null, "note": ""}},
    "fallback_contact": {{"name": null, "phone": null}},
    "transfer_timeout_seconds": null
  }},
  "non_emergency_routing_rules": {{
    "during_hours": "",
    "after_hours": ""
  }},
  "call_transfer_rules": {{
    "timeout_seconds": null,
    "retry_attempts": null,
    "on_transfer_fail": ""
  }},
  "integration_constraints": [],
  "after_hours_flow_summary": "",
  "office_hours_flow_summary": "",
  "questions_or_unknowns": [],
  "notes": ""
}}

STRICT RULES:
- Only extract what is explicitly stated
- Never invent or guess missing information
- If a field is not mentioned put null or empty
- Add every missing field to questions_or_unknowns
- Return ONLY the JSON object, no extra text

TRANSCRIPT:
{transcript}
"""

AGENT_PROMPT = """
You are Clara, an AI voice agent configuration specialist.

Based on the following account memo, generate a professional voice agent script.

The script MUST include:

BUSINESS HOURS FLOW:
1. Greeting
2. Ask purpose of call
3. Collect caller name and phone number
4. Transfer to appropriate person
5. If transfer fails: apologize and assure callback
6. Ask if they need anything else
7. Close call politely

AFTER HOURS FLOW:
1. Greeting mentioning closed
2. Ask purpose of call
3. Ask if this is an emergency
4. IF EMERGENCY: collect name, phone, address immediately then transfer
5. IF TRANSFER FAILS: apologize and assure urgent callback
6. IF NOT EMERGENCY: collect name and number, confirm callback next business day
7. Ask if they need anything else
8. Close call politely

STRICT RULES:
- Never mention function calls or tools to caller
- Never say you are an AI unless directly asked
- Sound warm, calm and professional

Return ONLY a valid JSON object:
{{
  "agent_name": "",
  "voice_style": {{"tone": "", "pace": "", "personality": ""}},
  "key_variables": {{
    "company_name": "",
    "business_hours": "",
    "timezone": "",
    "emergency_contact_primary": "",
    "emergency_contact_fallback": "",
    "office_address": ""
  }},
  "system_prompt": "",
  "call_transfer_protocol": {{
    "method": "warm_transfer",
    "timeout_seconds": "",
    "announce_to_agent": "",
    "on_fail": ""
  }},
  "fallback_protocol": {{
    "message": "",
    "log_callback": true,
    "escalate_if_emergency": true
  }},
  "tool_invocation_placeholders": []
}}

ACCOUNT MEMO:
{memo}
"""

ONBOARDING_PROMPT = """
You are a data extraction specialist for Clara Answers.

You will receive an onboarding call transcript and an existing v1 account memo.

Your job:
- Read the onboarding transcript carefully
- Compare it with the v1 memo
- Generate a complete updated v2 memo
- Generate a detailed changelog showing exactly what changed

Return ONLY a valid JSON object:
{{
  "v2_memo": {{
    "company_name": "",
    "version": "v2",
    "source": "onboarding_call",
    "business_hours": {{
      "confirmed": true,
      "days": "",
      "start": "",
      "end": "",
      "timezone": ""
    }},
    "office_address": "",
    "services_supported": [],
    "emergency_definition": [],
    "emergency_routing_rules": {{
      "confirmed": true,
      "primary_contact": {{"name": "", "phone": "", "role": ""}},
      "fallback_contact": {{"name": "", "phone": "", "role": ""}},
      "transfer_timeout_seconds": null
    }},
    "non_emergency_routing_rules": {{
      "during_hours": "",
      "after_hours": ""
    }},
    "call_transfer_rules": {{
      "timeout_seconds": null,
      "retry_attempts": null,
      "on_transfer_fail": ""
    }},
    "integration_constraints": [],
    "after_hours_flow_summary": "",
    "office_hours_flow_summary": "",
    "questions_or_unknowns": [],
    "notes": ""
  }},
  "changelog": {{
    "from_version": "v1",
    "to_version": "v2",
    "source_of_update": "onboarding_call",
    "summary": "",
    "changes": [
      {{
        "field": "",
        "change_type": "",
        "before": "",
        "after": "",
        "reason": ""
      }}
    ],
    "resolved_unknowns": [],
    "remaining_unknowns": []
  }}
}}

STRICT RULES:
- Only use information explicitly stated in transcript
- Never invent or guess missing information
- change_type must be: CONFIRMED, ADDED, or UPDATED
- Return ONLY the JSON object

ONBOARDING TRANSCRIPT:
{transcript}

EXISTING V1 MEMO:
{memo}
"""

# ─── Pipeline A — Demo → v1 ───────────────────────────────────────────────────

def run_pipeline_a(account_id, api_key, force=False):
    log(f"Pipeline A — {account_id}", "START")

    # Check if already processed
    memo_path = os.path.join(OUTPUTS, account_id, "v1", "account_memo.json")
    if os.path.exists(memo_path) and not force:
        log(f"{account_id} v1 already exists — skipping", "SKIP")
        return True

    # Read transcript
    transcript_path = os.path.join(TRANSCRIPTS, "demo", f"{account_id}_demo.txt")
    if not os.path.exists(transcript_path):
        log(f"Transcript not found: {transcript_path}", "FAIL")
        return False

    transcript = read_file(transcript_path)

    try:
        # Step 1 — Extract memo
        log(f"  Extracting account memo from transcript...")
        raw = call_gemini(api_key, EXTRACTION_PROMPT.format(transcript=transcript))
        memo = clean_json(raw)
        memo["account_id"] = account_id
        memo["version"] = "v1"
        memo["source"] = "demo_call"
        memo["generated_at"] = datetime.utcnow().isoformat() + "Z"

        save_json(memo_path, memo)
        log(f"  Saved account_memo.json", "OK")

        # Step 2 — Generate agent spec
        log(f"  Generating Clara agent script...")
        raw2 = call_gemini(api_key, AGENT_PROMPT.format(memo=json.dumps(memo, indent=2)))
        agent_spec = clean_json(raw2)
        agent_spec["account_id"] = account_id
        agent_spec["version"] = "v1"
        agent_spec["generated_at"] = datetime.utcnow().isoformat() + "Z"

        spec_path = os.path.join(OUTPUTS, account_id, "v1", "agent_spec.json")
        save_json(spec_path, agent_spec)
        log(f"  Saved agent_spec.json", "OK")

        log(f"{account_id} Pipeline A complete!", "OK")
        return True

    except Exception as e:
        log(f"{account_id} Pipeline A failed: {e}", "FAIL")
        return False

# ─── Pipeline B — Onboarding → v2 + Changelog ────────────────────────────────

def run_pipeline_b(account_id, api_key, force=False):
    log(f"Pipeline B — {account_id}", "START")

    # Check if already processed
    v2_path = os.path.join(OUTPUTS, account_id, "v2", "account_memo.json")
    if os.path.exists(v2_path) and not force:
        log(f"{account_id} v2 already exists — skipping", "SKIP")
        return True

    # Check v1 exists
    v1_path = os.path.join(OUTPUTS, account_id, "v1", "account_memo.json")
    if not os.path.exists(v1_path):
        log(f"{account_id} v1 not found — run Pipeline A first", "FAIL")
        return False

    # Read files
    transcript_path = os.path.join(TRANSCRIPTS, "onboarding", f"{account_id}_onboarding.txt")
    if not os.path.exists(transcript_path):
        log(f"Onboarding transcript not found: {transcript_path}", "FAIL")
        return False

    transcript = read_file(transcript_path)
    v1_memo = read_file(v1_path)

    try:
        # Step 1 — Generate v2 + changelog
        log(f"  Comparing v1 memo with onboarding transcript...")
        raw = call_gemini(api_key, ONBOARDING_PROMPT.format(
            transcript=transcript,
            memo=v1_memo
        ))
        result = clean_json(raw)

        # Save v2 memo
        v2_memo = result["v2_memo"]
        v2_memo["account_id"] = account_id
        v2_memo["generated_at"] = datetime.utcnow().isoformat() + "Z"
        save_json(v2_path, v2_memo)
        log(f"  Saved v2/account_memo.json", "OK")

        # Save changelog
        changelog = result["changelog"]
        changelog["account_id"] = account_id
        changelog["generated_at"] = datetime.utcnow().isoformat() + "Z"
        cl_path = os.path.join(OUTPUTS, account_id, "changelog", "changelog.json")
        save_json(cl_path, changelog)
        log(f"  Saved changelog/changelog.json", "OK")

        # Generate v2 agent spec
        log(f"  Generating updated Clara agent script...")
        raw2 = call_gemini(api_key, AGENT_PROMPT.format(memo=json.dumps(v2_memo, indent=2)))
        agent_spec = clean_json(raw2)
        agent_spec["account_id"] = account_id
        agent_spec["version"] = "v2"
        agent_spec["generated_at"] = datetime.utcnow().isoformat() + "Z"
        spec_path = os.path.join(OUTPUTS, account_id, "v2", "agent_spec.json")
        save_json(spec_path, agent_spec)
        log(f"  Saved v2/agent_spec.json", "OK")

        log(f"{account_id} Pipeline B complete!", "OK")
        return True

    except Exception as e:
        log(f"{account_id} Pipeline B failed: {e}", "FAIL")
        return False

# ─── Summary ──────────────────────────────────────────────────────────────────

def print_summary(results_a, results_b):
    print("\n" + "─" * 50)
    print("📊 BATCH RUN SUMMARY")
    print("─" * 50)
    print(f"{'Account':<15} {'Pipeline A':<15} {'Pipeline B':<15}")
    print("─" * 50)
    for acc in ACCOUNTS:
        a = "✅ Done" if results_a.get(acc) else "❌ Failed"
        b = "✅ Done" if results_b.get(acc) else "❌ Failed"
        print(f"{acc:<15} {a:<15} {b:<15}")
    print("─" * 50)
    total_a = sum(1 for v in results_a.values() if v)
    total_b = sum(1 for v in results_b.values() if v)
    print(f"Pipeline A: {total_a}/5 accounts processed")
    print(f"Pipeline B: {total_b}/5 accounts processed")
    print("─" * 50)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Clara Answers Batch Pipeline Runner")
    parser.add_argument("--api-key", required=True, help="Gemini API key")
    parser.add_argument("--force", action="store_true", help="Reprocess even if files exist")
    parser.add_argument("--pipeline", choices=["a", "b", "all"], default="all", help="Which pipeline to run")
    args = parser.parse_args()

    print("\n🎙️  Clara Answers — Batch Pipeline Runner")
    print(f"   Processing {len(ACCOUNTS)} accounts")
    print(f"   Pipeline: {args.pipeline.upper()}")
    print(f"   Force reprocess: {args.force}")
    print("─" * 50 + "\n")

    results_a = {}
    results_b = {}

    if args.pipeline in ("a", "all"):
        print("🚀 Running Pipeline A (Demo → v1) for all accounts...\n")
        for acc in ACCOUNTS:
            results_a[acc] = run_pipeline_a(acc, args.api_key, args.force)
            print()

    if args.pipeline in ("b", "all"):
        print("🚀 Running Pipeline B (Onboarding → v2) for all accounts...\n")
        for acc in ACCOUNTS:
            results_b[acc] = run_pipeline_b(acc, args.api_key, args.force)
            print()

    print_summary(results_a, results_b)
    print("\n✅ Batch run complete! Open dashboard to see results.\n")

if __name__ == "__main__":
    main()