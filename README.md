# clara-voice-agent-pipeline

**Author:** jaswanth.kanamarlapudi  
**Built with:** n8n · Gemini AI · Retell AI  
**Version:** 1.0.0

---

## Overview

`clara-voice-agent-pipeline` is a fully automated n8n pipeline that transforms raw call transcripts into a live, deployed AI voice agent called **Clara** on Retell AI — with no manual prompt writing required.

The pipeline takes call recordings/transcripts from demo and onboarding calls, extracts all the important business rules and routing logic using Gemini AI, builds a structured agent config, and deploys it directly to Retell AI as a working voice agent.

It also supports ongoing updates — when a client submits a new onboarding form, the pipeline automatically merges the new data with the existing config, detects conflicts, and generates an updated V3 agent config.

> **Screenshot — Project Overview**  
><img width="873" height="301" alt="image" src="https://github.com/user-attachments/assets/eebd8193-c4c2-43a0-95c2-53755ab043ec" />



---

## Problem it Solves

Setting up an AI voice agent manually requires:
- Reading through long call transcripts
- Writing detailed prompts by hand
- Manually entering business rules, phone numbers, routing logic
- Re-doing everything when client info changes

This pipeline **automates all of that** — just provide the transcript and the pipeline does the rest.

---

## Architecture

```
Demo Call Transcript
        ↓
   [ Phase 1 - Gemini AI ]
        ↓
   agent_v1.json (initial config)
        ↓
Onboarding Call Transcript
        ↓
   [ Phase 2 - Gemini AI ]
        ↓
   agent_v2.json (complete config)
   change_log.json (what changed)
        ↓
   [ Phase 3 - Retell API ]
        ↓
   Live Clara Voice Agent on Retell
   processing_log.json
        ↓
Client Submits Onboarding Form
        ↓
   [ Phase 4 - Gemini AI ]
        ↓
   agent_v3.json (updated config)
   conflict_report.json
```

---

## Workflows (4 Phases)

---

### Phase 1 — Demo Transcript to V1 Config

**Workflow name:** `Clara Phase 1 - Demo to V1`  
**Trigger:** Manual

**What it does:**  
Reads the demo call transcript and uses Gemini AI to extract an initial agent configuration. Fields not found in the demo call are marked as `UNKNOWN` for Phase 2 to fill in.

> **Screenshot — Phase 1 Workflow**  
<img width="1216" height="443" alt="image" src="https://github.com/user-attachments/assets/b8fbebbe-ced1-4b8c-85c4-2805866088d1" />

> *Add a screenshot of the full Phase 1 workflow canvas in n8n*

**Nodes:**
| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Trigger | Start the workflow |
| Read Transcript | Read/Write Files | Read demo_transcript.txt |
| Extract from File | Extract | Extract text content |
| Gemini AI | AI | Generate V1 config JSON |
| Convert to JSON | Convert | Convert output to file |
| Write agent_v1.json | Read/Write Files | Save config to disk |

**Input:**
```
data/transcripts/demo_transcript.txt
```

**Output:**
```
data/agents/agent_v1.json
```

> **Screenshot — Phase 1 Output**  
<img width="1365" height="571" alt="image" src="https://github.com/user-attachments/assets/c277df56-d58f-48a5-9c30-37eaafc5f055" />
  

---

### Phase 2 — Onboarding Transcript to V2 Config

**Workflow name:** `Clara Phase 2 - Onboarding to V2`  
**Trigger:** Manual

**What it does:**  
Reads the onboarding call transcript and the existing V1 config. Merges them and sends both to Gemini AI to generate a complete V2 config with all UNKNOWN fields filled in. Also generates a detailed change log.

> **Screenshot — Phase 2 Workflow**  
> <img width="1298" height="470" alt="image" src="https://github.com/user-attachments/assets/914df85b-63a2-4d5a-a15e-509bdbe9829d" />
 
> *Add a screenshot of the full Phase 2 workflow canvas in n8n*

**Nodes:**
| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Trigger | Start the workflow |
| Read Transcript | Read/Write Files | Read onboarding_transcript.txt |
| Extract Transcript | Extract | Extract transcript text |
| Read agent_v1.json | Read/Write Files | Read existing V1 config |
| Extract V1 | Extract | Extract V1 JSON text |
| Merge | Merge | Combine transcript + V1 data |
| Gemini V2 | AI | Generate complete V2 config |
| Convert to JSON | Convert | Convert to file |
| Write agent_v2.json | Read/Write Files | Save V2 config |
| Gemini Change Log | AI | Generate detailed change log |
| Convert to JSON | Convert | Convert to file |
| Write change_log.json | Read/Write Files | Save change log |

**Input:**
```
data/transcripts/onboarding_transcript.txt
data/agents/agent_v1.json
```

**Output:**
```
data/agents/agent_v2.json
data/logs/change_log.json
```

> **Screenshot — Phase 2 V2 Output**  
><img width="631" height="541" alt="image" src="https://github.com/user-attachments/assets/284e40df-8fa3-4f40-9ffd-3cae3c08f3ed" />


> **Screenshot — Change Log Output**  
> <img width="738" height="552" alt="image" src="https://github.com/user-attachments/assets/403ef2a2-4abf-496e-9eed-f691c79197f0" />



---

### Phase 3 — Push to Retell AI

**Workflow name:** `Clara Phase 3 - Push to Retell`  
**Trigger:** Manual

**What it does:**  
Takes the complete V2 config and deploys it to Retell AI. Creates a Retell LLM with the full Clara prompt, then creates the Retell Agent with the correct voice and language settings.

> **Screenshot — Phase 3 Workflow**  
<img width="1338" height="407" alt="image" src="https://github.com/user-attachments/assets/fac5cc2d-d0d7-491c-b400-de7b691db709" />

> *Add a screenshot of the full Phase 3 workflow canvas in n8n*
<img width="1305" height="264" alt="image" src="https://github.com/user-attachments/assets/4bc42a9d-ecf1-4642-b87d-c2449d232040" />

**Nodes:**
| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Trigger | Start the workflow |
| Read agent_v2.json | Read/Write Files | Read V2 config |
| Extract from File | Extract | Extract JSON text |
| Parse V2 | Code | Parse the agent config |
| Create Retell LLM | HTTP Request (POST) | Create LLM on Retell |
| Update LLM Prompt | HTTP Request (PATCH) | Push full prompt to LLM |
| Save Log | Code | Build processing log |
| Convert to JSON | Convert | Convert log to file |
| Write processing_log.json | Read/Write Files | Save log to disk |

**Retell API calls:**
| Call | Method | Endpoint |
|------|--------|---------|
| Create LLM | POST | `https://api.retellai.com/create-retell-llm` |
| Create Agent | POST | `https://api.retellai.com/create-agent` |
| Update Prompt | PATCH | `https://api.retellai.com/update-retell-llm/{llm_id}` |

**Deployed agent details:**
```
Agent Name:  ABC Fire Protection Services - Clara
Agent ID:    agent_c8db37afdedaf2f3f5e93ec21b
LLM ID:      llm_814e3922270b9029ef6ac68052da
Voice:       11labs-Adrian
Language:    en-US
Model:       gpt-4o
```

> **Screenshot — Retell Dashboard**  
<img width="1329" height="543" alt="image" src="https://github.com/user-attachments/assets/d4b4bacb-b3aa-418e-9714-b4cfa25dd344" />

> *Add a screenshot of Clara agent appearing in Retell AI dashboard*

> **Screenshot — Retell LLM Prompt**  
> <img width="692" height="558" alt="image" src="https://github.com/user-attachments/assets/f7dbf52e-7b27-48cf-ae52-d8fe5151458f" />

> *Add a screenshot of the LLM prompt loaded in Retell AI*

> **Screenshot — Phase 3 Processing Log**  
> <img width="407" height="589" alt="image" src="https://github.com/user-attachments/assets/8ea778c5-8076-478a-9a71-522707d9ba97" />


---

### Phase 4 — Onboarding Form to V3 Config

**Workflow name:** `Clara Phase 4 - Form Merge to V3`  
**Trigger:** Webhook (POST)

**What it does:**  
Listens for form submissions via webhook. Gemini AI merges new form data with existing V2 config to produce V3. Also runs a conflict check and generates a conflict report.

> **Screenshot — Phase 4 Workflow**  
> <img width="1281" height="329" alt="image" src="https://github.com/user-attachments/assets/443fb303-619f-48d3-a284-9e77a3962f88" />

> *Add a screenshot of the full Phase 4 workflow canvas in n8n*

**Nodes:**
| Node | Type | Purpose |
|------|------|---------|
| Webhook | Webhook | Receive form submission |
| Read agent_v2.json | Read/Write Files | Read existing V2 config |
| Extract from File | Extract | Extract V2 JSON |
| Parse V2 for Merge | Code | Parse V2 config |
| Merge | Merge | Combine form data + V2 |
| Gemini Merge V3 | AI | Generate V3 config |
| Convert to JSON | Convert | Convert to file |
| Write agent_v3.json | Read/Write Files | Save V3 config |
| Gemini Conflict Check | AI | Detect conflicts |
| Convert to JSON | Convert | Convert to file |
| Write conflict_report.json | Read/Write Files | Save conflict report |
| Respond to Webhook | Respond | Send success response |

**Input:**
```
POST http://localhost:5678/webhook/clara-form-submit
Body: { "business_hours": "...", "main_transfer_number": "...", ... }
```

**Output:**
```
data/agents/agent_v3.json
data/logs/conflict_report.json
```


---

## Complete File Structure

```
C:\Users\kanam\.n8n-files\
└── data\
    ├── transcripts\
    │   ├── demo_transcript.txt          ← Input for Phase 1
    │   └── onboarding_transcript.txt    ← Input for Phase 2
    ├── agents\
    │   ├── agent_v1.json                ← Output of Phase 1
    │   ├── agent_v2.json                ← Output of Phase 2
    │   └── agent_v3.json                ← Output of Phase 4
    └── logs\
        ├── change_log.json              ← Output of Phase 2
        ├── processing_log.json          ← Output of Phase 3
        └── conflict_report.json         ← Output of Phase 4
```

> **Screenshot — File Structure**  
<img width="409" height="400" alt="image" src="https://github.com/user-attachments/assets/97908a78-9fc9-4db3-93f6-1203bb354c35" />

> *Add a screenshot of the data folder structure in Windows Explorer*

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| n8n | 2.3.2 (Self Hosted) | Workflow automation engine |
| Gemini AI | gemini-2.5-flash | AI config generation and analysis |
| Retell AI | v1 API | Voice agent deployment platform |
| ElevenLabs | 11labs-Adrian | Voice for Clara |
| GPT-4o | via Retell | LLM powering Clara's responses |

---

## Agent Config Fields

| Field | Description |
|-------|-------------|
| `version` | Config version (v1 / v2 / v3) |
| `source` | Where data came from |
| `client_name` | Name of the client business |
| `location` | Client location |
| `service_types` | Types of services offered |
| `business_hours` | Operating hours |
| `timezone` | Client timezone |
| `main_transfer_number` | Business hours transfer number |
| `after_hours_transfer_number` | After hours emergency number |
| `transfer_timeout_seconds` | How long to wait before transfer fails |
| `emergency_definition` | What counts as an emergency |
| `non_emergency_examples` | Examples of non-emergency calls |
| `servicetrade_rules` | Rules for ServiceTrade integration |
| `fallback_action` | What to do when transfer fails |
| `fallback_sms_number` | SMS number for failed transfer alerts |
| `special_routing_rules` | Special call routing rules |
| `special_constraints` | Any special restrictions |
| `questions_or_unknowns` | Fields still needing clarification |
| `agent_prompt_v2` | Full Clara prompt for the agent |

---

## How to Run

### Prerequisites
- n8n installed and running on `http://localhost:5678`
- Gemini API key configured in n8n credentials
- Retell AI API key configured in n8n Header Auth credentials
- Transcripts placed in correct folder

### Step by Step

**Step 1 — Run Phase 1**
1. Open `Clara Phase 1 - Demo to V1` workflow
2. Click Execute Workflow
3. Check `data/agents/agent_v1.json` was created

**Step 2 — Run Phase 2**
1. Open `Clara Phase 2 - Onboarding to V2` workflow
2. Click Execute Workflow
3. Check `data/agents/agent_v2.json` was created
4. Check `data/logs/change_log.json` was created

**Step 3 — Run Phase 3**
1. Open `Clara Phase 3 - Push to Retell` workflow
2. Click Execute Workflow
3. Check Retell dashboard — Clara agent should appear
4. Check `data/logs/processing_log.json` was created

**Step 4 — Test Phase 4**
1. Open `Clara Phase 4 - Form Merge to V3` workflow
2. Click Listen for test event on Webhook node
3. Run this in PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:5678/webhook-test/clara-form-submit" -Method POST -ContentType "application/json" -Body '{"business_hours": "Monday to Friday 8am to 6pm", "main_transfer_number": "214-555-9999"}'
```
4. Check `data/agents/agent_v3.json` was created
5. Check `data/logs/conflict_report.json` was created

---

## Clara Agent Behavior

**During Business Hours (Mon-Fri 7:30 AM - 5:30 PM CT):**
1. Greets caller: "Hi, this is Clara from ABC Fire Protection, how can I help you?"
2. Collects caller name and phone number
3. Fire alarm inspection calls → transfers to 214-555-0155
4. All other calls → transfers to 214-555-0147
5. Transfer fails after 60 seconds → apologizes and assures callback

**After Hours:**
1. Greets caller: "You have reached ABC Fire Protection after hours."
2. Asks if call is an emergency
3. Emergency → collects name, phone, address → transfers to 214-555-0198
4. Emergency transfer fails → apologizes, assures 15 min callback, sends SMS to 214-555-0199
5. Non-emergency → collects details → confirms next business day callback

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Binary file read error | n8n stores files compressed | Add `destinationKey` in Extract from File node |
| 404 on Retell API | Wrong URL format | Use `https://api.retellai.com/create-agent` (no /v2/) |
| Invalid response engine | Wrong body format | Use `llm_websocket_url` instead of `response_engine` object |
| JSON parse error | Special characters in prompt | Use Add Parameter fields instead of raw JSON body |
| Webhook not registered | Webhook not listening | Click Listen for test event before POST request |
| 2 items from Gemini | Merge node in Append mode | Add Code node before Gemini to combine into 1 item |

---



---

*Built by jaswanth.kanamarlapudi*
