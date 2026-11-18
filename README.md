# Drips Wave Sister Setup

A complete kit so Dev Aizen (`devbigaiizen`) can run her own Muse AI to do Drips Wave work, on her own account, her own GitHub, her own rewards.

Her brother (`devflora-princess`, display name dev.maya) already does Waves this way with his own AI. This kit copies that exact workflow for her, so she does not burn his weekly Muse allowance and her work stays hers.

## The deal, in plain words

- She applies for issues herself, in the Drips app, on her own device.
- KYC is done by her, the natural person using the account. One account per participant, 18+.
- The AI only codes, tests, pushes and opens pull requests **after** she has been assigned an issue. Nothing is pushed to her repo before an assignment. That is a hard rule.
- Rewards are hers, paid after the Wave ends plus a 7-day Compliment window, generally in the organiser's token.

## What is in here

- `SETUP.md`: the full step-by-step guide. Start here.
- `AGENT.md`: the instructions she gives her AI. This is the brain of the setup.
- `WAVE-11.md`: Wave 11 facts: dates, pool, points, candidate issues.
- `scripts/check-assignment.py`: checks GitHub for new issues assigned to her.
- `LICENSE`: MIT.

## Quick start

1. Read `SETUP.md` top to bottom.
2. Get her own Muse account and connect her GitHub with a fine-grained token (never paste the token in chat, use the secure vault flow).
3. Give her AI the starter prompt in `SETUP.md`, step 5.
4. She applies for a Wave 11 issue in the Drips app herself.
5. Once assigned, her AI does the coding, testing and PR work, following `AGENT.md`.

## Wave 11 at a glance

- Runs 18-25 November 2026.
- Pool $75,000 shared in proportion to points earned (a $100K USDC figure was quoted elsewhere, confirm the pool in the Drips app).
- Points: Trivial 100, Medium 150, High 200.
- Her fork already exists: `devbigaiizen/stellar-agent-guard-sdk`.

## Safety rules that never change

- Never run suspicious code. Never run `api.js` or `npm run build` on a branch you have not vetted.
- If malware is the work itself, or its purpose cannot be told, abandon the issue and report it.
- If malware was added on top of otherwise good work, clean it, rebuild from main, and tell the maintainer what was removed. No quiet clean-ups.
- Never claim a test or check passed unless it was actually run and passed.
- No real money, no mainnet, no multi-account farming, no proxies.
