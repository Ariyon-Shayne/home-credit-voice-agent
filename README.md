# Home Credit LAP Voice Agent — Starter Project

This ZIP contains the prompt, a Python eligibility-rule validator, sample test scenarios, and optional Retell API helper code for the Home Credit Loan Against Property (LAP) assignment.

## Important

- This is a **starter integration**, not a complete production calling system.
- The Retell dashboard setup is still required: create an agent, configure its voice, paste the system prompt, and connect any required call tools.
- The Python validator does **not** understand speech or extract facts from a transcript. It validates structured data supplied to it.
- Do not put real customer data or API keys in source code.
- Use fictional test customers until your organization has approved any real outbound calling and recording.
- Preliminary eligibility is not loan approval.

## Files

- `prompts/system_prompt.txt` — complete prompt for the Retell LLM instruction field.
- `app/eligibility.py` — eligibility rules and outcome logic.
- `app/retell_call_details.py` — optional example to retrieve a call transcript and recording/public-log URLs.
- `tests/test_eligibility.py` — unit tests for important business rules.
- `.env.example` — environment variable template.
- `requirements.txt` — Python dependencies for the optional API helper/tests.
- `retell_setup.md` — dashboard configuration and testing instructions.
- `sample_test_cases.json` — manual conversational test cases.

## Quick start

### 1. Create a virtual environment (optional but recommended)

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Validate business rules locally

```bash
python -m unittest discover -s tests -v
```

The tests use only fictional data and do not make calls.

### 3. Configure Retell

Follow `retell_setup.md`. Copy the contents of `prompts/system_prompt.txt` into the agent's prompt/instructions field. Replace or configure placeholders according to the current Retell dashboard and your chosen call flow.

### 4. Retrieve a call record (optional)

Copy `.env.example` to `.env`, set `RETELL_API_KEY` and `RETELL_CALL_ID`, then run:

```bash
python app/retell_call_details.py
```

The script only retrieves metadata for a call that already exists. It does not place calls or publish recordings. Verify URLs and sharing permissions in Retell before submitting.

## Frontend demo

A polished responsive landing page is included in `frontend/`. Configure `frontend/config.js` with a Retell **Public Key** and **Voice Agent ID**, then run `python -m http.server 5500 --directory frontend` from the project root and open `http://localhost:5500`. See `frontend/README.md` for deployment and security notes. Never put a private Retell API key in frontend files.


## Frontend customer-name personalization
The `frontend/` now asks for a customer name on page load and passes it to Retell as `customer_name` when starting a browser voice call. See `frontend/README.md` for setup. Use a Retell Public Key in frontend code; never expose a private API key.
