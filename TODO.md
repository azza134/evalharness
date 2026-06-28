# Harness — future work

## Centralise all editables into one config (DX / usability)

**Goal:** one centralised place for every editable input/parameter, so a user can point the
harness at their own document/model/questions without digging through logic. Right now the
"editables" are scattered across files and inline in the code — that's a barrier for anyone
who isn't the author.

**Editables to pull into a single config** (e.g. a `config.py`, `config.yaml`, or a clearly
marked CONFIG block at the top):
- The grounding document (`document.txt` path / contents)
- The questions: in-document, abstention, and perturbation
- The perturbation itself (the secret fact-swap)
- `N` (samples per cell)
- The three instruction strengths (STRONG / MODERATE / WEAK) and the `STRICT` text
- Gradee model + provider, and judge model + provider — including the **ability to swap which vendor (Claude / GPT) plays gradee vs judge** in either direction (and keep the cross-vendor property whichever way it's set)
- Gold-label file path (`judge_gold.json`)
- API key handling

**Why:** makes the harness easy for users to pick up and run on their own material — the
difference between "a thing only Andrew can run" and "a thing anyone can configure." A real
step toward it being a product, not just a personal prototype.

*(Captured 2026-06-28, mid Latitude 37 application — not to be built now; revisit after the deadline.)*

## Automated judge pass/fail gate

**Goal:** turn judge validation from a manual eyeball into a coded verdict. Right now
`validate_judge()` in `judge.py` prints raw agreement, Cohen's kappa, and the disagreement
list — but never declares pass/fail. The human decides.

**Proposed gate:** PASS only if **(a)** Cohen's kappa ≥ a threshold (e.g. 0.8) **AND**
**(b)** zero disagreements on the clean anchors (`clean-leak anchor` / `clean-faithful anchor`
roles). Borderline disagreements are allowed. Print an explicit PASS/FAIL with the reason.

**Why:** makes "is this judge trustworthy?" reproducible instead of a vibe, and lets
`harness.py` refuse to run on an unvalidated or failing judge. The anchors are the real gate —
a judge that fumbles an obvious case is broken regardless of the aggregate number.

*(Captured 2026-06-28.)*
