# FrostSkyNet Data Tools — public examples

Clean, score, and format small text datasets with three pay-per-request APIs.

- Storefront: https://frostskynet-tools.frostskynet-api.workers.dev/
- Developer guide: https://frostskynet-tools.frostskynet-api.workers.dev/docs/
- API: https://route-a-worker.frostskynet-api.workers.dev/
- OpenAPI: https://frostskynet-tools.frostskynet-api.workers.dev/openapi.json

**Preview release:** mainnet payment offers are enabled, but real-USDC settlement testing and public directory indexing remain pending. These public examples are unpaid checks and recorded synthetic outputs, not proof of mainnet settlement.

| Route | Purpose | Price per API request | Complete JSON body limit |
|---|---|---:|---:|
| POST /clean | Convert text, JSON or JSONL to cleaned JSONL | 0.005 USDC | 51,200 UTF-8 bytes |
| POST /judge | Add fixed-rule quality scores; optional pattern redaction/filtering | 0.01 USDC | 10,240 UTF-8 bytes |
| POST /format | Convert JSONL to JSONL, chat examples or Markdown | 0.005 USDC | 51,200 UTF-8 bytes |

All tools take `{ "input": "…", "options": {} }` and return `{ "output": "…", "stats": {} }` on success. Use one response's output as the next call's input. Each call is paid separately. There is no /pipeline endpoint. Judge uses fixed rules, not an AI model; detection is incomplete and can produce false positives. CSV parsing is not offered through this API.

## Run an unpaid offer check

These scripts contain no wallet functionality, secret-file reading, payment authorization, or automatic payment retry. They use synthetic data, print only status and policy-match booleans, and suppress raw response/error content.

Node.js 22 or later:

```sh
node check_offer.mjs
```

Python 3.10 or later, standard library only:

```sh
python check_offer.py
```

Both inspect the /clean offer for Base mainnet, native USDC, the intended receiver, and the exact 0.005 USDC amount. HTTP 402 is expected. A signed request is needed to obtain transformed output from the API; these scripts never sign one.

## Recorded examples

`examples.json` contains the clean → judge → format chain generated locally using synthetic input. No wallet or payment was used to generate it. The storefront lets you view and download these examples for free.

## Payment clients

Use your own reviewed x402-compatible client and secure wallet storage for paid requests. Check all offered terms before signing and set spending limits. Do not manually send USDC to the seller to unlock a request. Never put private keys, recovery phrases, credentials, or signed payment headers in this repository, API input, issues, or support messages.

After a paid timeout or unclear result, investigate public settlement evidence before authorizing again. Do not infer settlement solely from HTTP 200. The website does not connect wallets or provide checkout.

This repository contains public client examples only; it is not the private server project. Example code is provided under the included MIT license. Hosted API use is priced separately as above.
