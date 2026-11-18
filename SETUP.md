# Setup Guide: Drips Wave on your own account

For Dev Aizen (`devbigaiizen`). This gets you from zero to a working AI that does Drips Wave coding for you, the same way your brother's AI does it for him, without touching his account or his weekly Muse allowance.

Your own Muse account has its own weekly allowance, separate from his. That is the whole point of this setup.

## Step 0: What you need

- Your own Muse account (free is fine).
- Your own GitHub account: `devbigaiizen`.
- A Drips account, signed in with your GitHub, with KYC completed by you.
- A phone or PC with internet. Nothing to buy.

## Step 1: Get Muse

1. Install the Muse app on your phone, or open it on your PC.
2. Sign in with **your own** account, not your brother's.
3. Your weekly allowance is yours alone. When it runs low, wait for the reset instead of borrowing his account.

## Step 2: Connect your GitHub to Muse

1. In Muse, ask your AI: "Connect my GitHub account."
2. Muse will show a secure setup link. Open it and enter a **fine-grained personal access token** you create on GitHub:
   - GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.
   - Resource owner: your account. Repository access: Public repositories only.
   - Permissions: Contents read and write, Pull requests read and write, Issues read and write.
   - Give it a short expiry (it only needs to cover the Wave, to 25 November 2026).
3. Enter the token only on the secure setup page. **Never paste it in chat**, not even to your own AI, and never put it in a file in this repo.
4. Ask your AI to prove the connection with a harmless read, for example reading your own profile. It should come back as `devbigaiizen`.

## Step 3: Your fork (already done)

Your fork of the Wave repo already exists: `devbigaiizen/stellar-agent-guard-sdk`.

Do not push anything to it until you have been assigned an issue. That rule protects your account.

## Step 4: Give your AI this kit

1. Clone or download this repo on your device, or send its files to your AI in chat.
2. Tell your AI to read `AGENT.md` and `WAVE-11.md` and keep them as its working instructions.
3. Install the two security skills your AI needs for vetting code. They come from the UnitOneAI SecuritySkills pack (MIT licensed, https://github.com/UnitOneAI/SecuritySkills). Tell your AI: `npx skills add UnitOneAI/SecuritySkills`, then pick **secure-code-review** and **dependency-scanning**. Secure-code-review checks code against OWASP ASVS and the CWE Top 25, and dependency-scanning checks dependencies for known vulnerabilities. Your AI uses both before it runs any code it did not write itself.
4. Use the starter prompt in step 5.

## Step 5: The starter prompt (paste this to your AI)

> You are my coding agent for Drips Wave 11. Read AGENT.md and WAVE-11.md in this repo and follow them exactly. My GitHub is devbigaiizen. My fork is devbigaiizen/stellar-agent-guard-sdk. Check whether I have any new Wave 11 assignment. If I do, start the workflow in AGENT.md. Do not push anything to my repo until I have actually been assigned an issue. If I have no assignment yet, tell me that and stay quiet until I ask again.

## Step 6: Apply for an issue (you do this yourself)

1. Open the Drips app and sign in with your GitHub account.
2. Go to Explore, open the active Stellar Wave, and browse the available issues.
3. Read the contributor FAQ first if anything is unclear: https://docs.drips.network/wave/contributors/faq/
4. Click **Apply** on an issue you can finish before the Wave ends, and write a short message about your experience. Mention a previous PR if you have one.
5. Wait for the maintainer to assign you. Applying is not the same as being assigned.

Good first candidates are listed in `WAVE-11.md`. Check the points for each issue in the Drips app before applying, because points can change.

## Step 7: The assignment check

Once you have applied, your AI should check for a new assignment every 5 hours while the Wave is open. Two ways:

- **Automatic:** ask your AI to set up a recurring check in Muse, every 5 hours, that runs `scripts/check-assignment.py` and only messages you when a new assignment appears.
- **Manual:** whenever you want, ask your AI "check for a new Wave 11 assignment" and it runs the same script.

The script needs your GitHub token. Your AI reads it from its secure connection, never from chat. It compares what it finds against `seen.json`, so it never starts the same issue twice.

## Step 8: When you are assigned

Your AI follows `AGENT.md`: it reads the issue, clones your fork, makes a branch, writes the fix, runs the typecheck and unit tests, pushes, and opens the pull request. It shows you the code in plain English before the PR goes up, so you can explain it if the maintainer asks.

You review the PR description before it is submitted. Nothing goes out without you seeing it first.

## Step 9: Getting paid

- Points are awarded when the maintainer marks your issue completed.
- Your share of the pool is proportional to your points, not a fixed amount per issue.
- Payout happens after the Wave ends and the 7-day Compliment window closes. There is no fixed payout date.
- Rewards are generally paid in the organiser's token, and you need a valid wallet address in Drips to withdraw them.
- If you cannot finish an issue before the Wave ends, tell the maintainer immediately.

## If something goes wrong

- **Token rejected (401):** the token expired or was entered wrong. Make a new one and reconnect through the secure setup page.
- **Permission denied (403):** the token lacks a permission. Check step 2 and add Contents, Pull requests and Issues, read and write.
- **AI says an issue looks like malware:** stop. Do not run the code. Tell your brother or the maintainer what you found. See the malware rule in `AGENT.md`.
- **Weekly allowance runs out:** stop and wait for the reset. Do not use anyone else's account to keep going.
