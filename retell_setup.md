# Retell AI Setup and Testing Guide

Dashboard screens and menu labels can change; use the current Retell documentation if a label differs.

## A. Create an agent
1. Sign in at https://dashboard.retellai.com/
2. Create a new voice agent.
3. Name it `Home Credit LAP Qualification Agent`.
4. Select a hosted Retell LLM or the current equivalent response engine.
5. Choose a professional voice with clear Indian English pronunciation.
6. Start with English. Test Hindi separately after English rules pass.
7. Set an initial greeting that only verifies identity, e.g. `Hello, may I speak with {{customer_name}}?`
8. Paste `prompts/system_prompt.txt` into the LLM prompt/instructions field.
9. Configure dynamic variables using the exact syntax supported by your agent/call setup. Do not assume every placeholder is automatically injected.
10. Save the draft and use the dashboard's simulation/test feature.

Official docs:
- https://docs.retellai.com/
- https://docs.retellai.com/api-references/create-agent
- https://docs.retellai.com/api-references/get-call

## B. Important variable guidance
- Set company_name, customer_name, agent_name, agent_gender and language_to_speak using supported dynamic variables or fixed test values.
- If current date/time variables are not supported, remove their need or supply values through a supported call configuration.
- Conversation history and the latest utterance are normally managed by the conversation engine. Do not expect literal placeholders to update by themselves.
- Use verified RAG content only. If no source is available, say product details are not available rather than inventing them.

## C. Run tests
Start with simulated/browser testing, then use only authorized test calls with fictional identities.
Run the scenarios in `sample_test_cases.json`:
1. Happy path: all seven checklist items pass.
2. Agricultural property: immediate disqualification.
3. Cash income: immediate disqualification.
4. Originals unavailable: immediate disqualification.
5. Tenure 2 years: disqualification.
6. Tenure 16 years: disqualification.
7. Request 90 lakh: ask whether 75 lakh is acceptable.
8. Existing property loan or EMI reduction: transfer referral.
9. Busy customer: ask callback time and end current call.
10. Out-of-order answers: remember known fields.
11. Contradictory/corrected answers: use latest clear correction; clarify unresolved contradiction.
12. Ambiguous documents: clarify rather than assume.
13. Interest-rate question: do not invent a rate.

Reset call state between scenarios. Review the transcript and audio after each run. Only mark a test passed after confirming the behavior.

## D. Review call recordings and transcripts
1. Open the dashboard's call history / call logs.
2. Select the completed test call.
3. Review the transcript and recording.
4. Look for a share/public-log action if available.
5. Test shared links in a private/incognito browser window.
6. Confirm both audio and transcript can be accessed by the evaluator.
7. Check whether signed URLs expire before submitting.

## E. Optional API retrieval
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and set your own API key and an existing test call ID.
3. Set environment variables in your shell or use a local dotenv loader of your choice. This script does not automatically read `.env`.
4. Run `python app/retell_call_details.py`.
5. Check the output for transcript, recording_url and public_log_url. Fields may be absent based on call state/configuration.
6. Never publish the API key or commit `.env`.

## F. Before submission
- Keep test identities fictional.
- Do not make real customer calls without organizational approval and compliance checks.
- Do not describe preliminary qualification as loan approval.
- Verify links, recording access and transcript completeness.
