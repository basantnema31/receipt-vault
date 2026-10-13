# ReceiptVault 🔐

**Zero-Leak, Local-AI Bookkeeping & Invoice Parser for Freelancers**

*Built for the Hacktoberfest Open-Source AI Challenge: Week 2 — "Side Hustle"*

---

## 💼 The Problem & Why Someone Would Pay For It

Freelancers, agency owners, and independent contractors regularly sign **strict Non-Disclosure Agreements (NDAs)** with clients. They cannot upload confidential invoices, receipts, project milestones, or subcontractor bills to cloud LLMs (like OpenAI or Anthropic) without risking breach of contract or leaking proprietary pricing.

Yet, manual bookkeeping takes 4 to 8 hours per week and standard accounting software charges \$30–\$60/month. 

**ReceiptVault** solves this with a privacy-first, offline open-weight AI architecture:
- 🛡️ **Zero Data Egress:** All parsing and entity extraction runs locally using open-weight models.
- ⚡ **Automated Categorization:** Classifies expenses into standard tax categories.
- 📊 **One-Click Tax Export:** Generates clean, audited CSV ledger ready for accountants.
- 💰 **Monetization Viability:** Freelancers happily pay a one-time \$29–\$49 lifetime license or \$9/mo offline desktop utility to maintain complete client confidentiality while saving dozens of hours each month.

## 🚀 Why Open Innovation Matters

1. **Client Confidentiality & Zero Telemetry:** Open-weight models can run air-gapped on any machine with zero network traffic.
2. **Deterministic Economics:** Using closed APIs incurs recurring token fees and risks unexpected price hikes. Open-weight models ensure a fixed, predictable cost structure.
3. **Model Sovereignty:** Developers and users are free to swap, fine-tune, or quantize models (e.g. Qwen2.5, Llama 3.2, or SmolLM) to specific international tax codes.

## 🛠️ Quickstart

```bash
pip install flask
python app.py
```

Access the dashboard at `http://localhost:5002`

## 📄 License

MIT License — See [LICENSE](./LICENSE)
