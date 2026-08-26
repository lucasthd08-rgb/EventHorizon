# EventHorizon‑AI

> **A rigorous temporal AI platform.**  
> We build and validate forecasting systems with academic‑grade statistical discipline — then turn them into products.

---

# Why This Exists

Most AI forecasting projects sell hype. We sell proof.

Every model released under the EventHorizon umbrella passes through the same rigorous validation pipeline before it ever reaches a client. We document failures as carefully as successes, because **honest methodology is the product**.

---

# Products

| Product | Domain | Status | Key Result | Honest Notes |
|---------|--------|--------|------------|--------------|
| **EventHorizon Crypto** | BTC/USDT 5‑second direction | ✅ Validated | +8 pp edge (60 % vs 52 % baseline) | Economically unviable under standard exchange fees; published as a complete case study |
| **EventHorizon Demand** | Retail demand forecasting (M5 Walmart) | ✅ Validated | 30 % improvement over seasonal baseline (WAPE 30.9 % vs 44.4 %) | Statistically significant in 7/7 stores; WI_1 shows smaller margin (documented openly) |

---

# Validation Pipeline

The same pipeline protects every product we release:

- ⏳ **Walk‑forward analysis** with temporal embargo
- 🧩 **Block bootstrap** by date (respects cross‑sectional correlation)
- 🔀 **Paired gap bootstrap** (model vs. baseline on same days)
- 🔬 **Permutation testing** for classification problems

This pipeline is extracted into a standalone open‑source library:  
[**honest-validation-toolkit**](https://github.com/EventHorizon-ia/honest-validation-toolkit)

---

# Repository Map

| Repository | Purpose | Contents |
|------------|---------|----------|
| [eventhorizon-crypto](https://github.com/EventHorizon-ia/eventhorizon-crypto) | Production code | Trading bot, execution engine, audit dashboard |
| [eventhorizon-demand](https://github.com/EventHorizon-ia/eventhorizon-demand) | Production code | Forecasting API, model serving, dashboard |
| [crypto-h0-edge](https://github.com/EventHorizon-ia/crypto-h0-edge) | Research notebook | Edge discovery, full audit trail, permutation tests |
| [demand-m5](https://github.com/EventHorizon-ia/demand-m5) | Research notebook | M5 baseline, feature iteration, final model, metrics |
| [honest-validation-toolkit](https://github.com/EventHorizon-ia/honest-validation-toolkit) | Shared library | Bootstrap, walk‑forward, permutation, WAPE, MASE |

---

# Philosophy

| Principle | Description |
|-----------|-------------|
| 🔬 **Rigor over Hype** | Every number ships with confidence intervals and documented limitations |
| 🧾 **Honesty over Marketing** | We publish failures as carefully as successes |
| 🛠️ **Products over Promises** | We only charge for systems that have survived real‑world validation |

---

# Author

**Lucas** — 14 years old, Brazil.  
OBCIT finalist.  
Built EventHorizon‑AI alone, from the physics engine to the audit dashboard.

---

# Links

| Resource | URL |
|----------|-----|
| 🚀 EventHorizon‑AI Hub | [github.com/EventHorizon-ia/EventHorizon](https://github.com/EventHorizon-ia/EventHorizon) |
| 📈 Crypto Research | [github.com/EventHorizon-ia/crypto-h0-edge](https://github.com/EventHorizon-ia/crypto-h0-edge) |
| 📦 Demand Research | [github.com/EventHorizon-ia/demand-m5](https://github.com/EventHorizon-ia/demand-m5) |
| 🧪 Validation Toolkit | [github.com/EventHorizon-ia/honest-validation-toolkit](https://github.com/EventHorizon-ia/honest-validation-toolkit) |
| 🌐 Public Audit Dashboard | [eventhorizon-ia.github.io](https://eventhorizon-ia.github.io/trader-ai/dashboard-en.html) |

---

*EventHorizon‑AI — Proof, not promises.*
