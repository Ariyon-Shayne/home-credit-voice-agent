# Home Credit LAP Voice Agent — Frontend

Responsive landing page with a customer-name prompt and a browser-based Retell Web SDK voice call.

## What happens
1. When the site opens, a modal asks the visitor for their name.
2. The name stays in JavaScript memory for the current page session; it is not written to local storage.
3. When the visitor clicks **Start voice call**, the site calls Retell using `retell-client-js-sdk` and passes the name as `retell_llm_dynamic_variables.customer_name`.
4. The agent prompt should use `{{customer_name}}` (the included project system prompt already does).

## Configure Retell
1. Open `config.js`.
2. Replace `YOUR_RETELL_PUBLIC_KEY` with a Retell **Public Key** intended for browser Web Calls.
3. Replace `YOUR_RETELL_VOICE_AGENT_ID` with your published voice agent ID.
4. In Retell, restrict the public key to the website domain. Add `localhost` for local development if the dashboard allows it, and add your deployed HTTPS domain before sharing.
5. Ensure the agent prompt uses `{{customer_name}}` in the greeting, such as `Hello, may I speak with {{customer_name}}?`.

The page imports `retell-client-js-sdk` dynamically from `https://esm.sh/retell-client-js-sdk@latest`, so an internet connection is required. For a production build, prefer installing and bundling the SDK with your package manager.

## Run locally
From the project root:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`. You can also use VS Code Live Server. Microphone access is supported on `localhost` during development and on HTTPS in production.

## Deploy
Deploy the `frontend` folder to Netlify, Vercel, GitHub Pages, or another static host. Add the deployed HTTPS domain to the Retell public-key allowlist. Then test the deployed page in a fresh browser session.

## Security and privacy
- Never place your private Retell API key in `config.js`, `app.js`, `voice.js`, or any browser code.
- Only use a Retell Public Key intended for browser use and restrict its allowed domains.
- The name entered on the page is held in memory only and is sent to Retell as a dynamic variable when a call starts. It is not used to verify identity.
- Use fictional customer details for assignment testing.

This is an assignment/demo interface, not an official loan application or final approval.
