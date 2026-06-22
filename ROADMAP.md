# Roadmap

engrim is intentionally small. The roadmap widens what a memory layer can do **without** breaking
the core principle: *retrieve a relevant, meaning-ranked slice — never dump raw history* — and stay
local and private.

## v0.4 (shipped)

- **`engrim sync` + seed-once context build** — one-time mirror of file-memory into the store on a
  project's first run, then db-canonical.
- **Full-conversation log** — `Stop` hook tails Claude Code's transcript JSONL into an append-only
  `log` table (offset cursor + uuid dedup). Complete, never loaded into context.
- **The minder (`engrim assist`)** — `UserPromptSubmit` hook that auto-injects the relevant db slice
  per prompt: ranked retrieval, term-gated, ~150-token cap, hits-only.
- **Full four-hook loop in `engrim setup`** — SessionStart/UserPromptSubmit/Stop/SessionEnd, all
  idempotent and guarded.

## v0.5 (shipped)

- **Semantic minder** — `assist` fuses bm25 + embedding cosine (reciprocal-rank fusion) so it
  surfaces *conceptually* relevant memory, not just lexical matches. Embeddings are computed with a
  fast static embedder (model2vec) and stored in the same SQLite file.

## v0.6 — works out of the box (shipped)

The semantic tier went from opt-in to **on by default**, so a clean install delivers meaning-based
recall with zero extra steps:

- **Bundled** — model2vec is a core dependency; no separate extra to discover.
- **Default-on** — semantic is enabled whenever the backend imports; `ENGRIM_EMBED=off` is the
  opt-out (pure-lexical, zero third-party deps, fully offline).
- **Auto-embed on `add`** — new records are searchable by meaning immediately; no manual `engrim
  embed`.
- **`engrim setup` warms the model** with a visible one-time message, so session hooks never
  cold-download mid-prompt.
- **Visible restore** — the boot pack shows exactly what was reloaded, so a first-run user *sees*
  the save come back (and learns it's safe to clear).

## Layered scopes — the global user-layer (shipped)

Memory is project-scoped by design, but some truths are about *you*, not any one repo (who authors
your code, how you like commits written, conventions you hold everywhere). engrim now keeps a single
**global user-layer** and co-loads it alongside whatever project you're in:

- **`engrim add --global`** writes to the layer; **every read** (boot pack, the minder, `recall`)
  spans the current project *plus* global, so user-level truths ride into every session everywhere.
- **Purely additive** — a project's own records never leak across projects, the global layer flows
  through the same fair, budget-capped boot pack (no bloat), and `ENGRIM_NO_GLOBAL=1` is a full
  opt-out that restores project-only reads exactly.
- **Vertical layering, not horizontal federation** — deliberately *user ⊕ project*, never arbitrary
  multi-project loading, which would dilute the lean pack that is the whole point.

## v0.7 — "safe to clear"

The trust problem: a first-run user has no evidence engrim will hand their context back, so they
won't clear aggressively. Closing it with an **honest coverage signal** on the existing transcript
log:

- **`engrim review` (shipped)** — scans recent log turns for decision-signal language and checks each
  against curated memory (semantic when available, calibrated to err toward flagging). Reports what
  may not be captured *before* you clear; says *"looks safe to clear"* only when nothing's
  outstanding. Honest by construction — it never claims a safety it can't verify (#143).
- **Auto-promote (next)** — let `review` / the agent one-shot a flagged decision into curated memory
  (`engrim add --from-log …`), so closing the gap is a keystroke instead of a retype.
- **PreCompact hook (next)** — run the coverage check automatically right before the agent compacts,
  nudging a flush of uncaptured decisions at the exact moment they'd otherwise be lost.

## Retrieval quality — "smart, hot context loading"

The differentiator. Two tiers:

- **Tier A — RAG craft, unlocked by a resident daemon.** A tiny long-lived process keeps the model
  warm (semantic drops from ~tens-of-ms to ~1ms per prompt), which makes affordable: a stronger
  contextual embedder, a **cross-encoder rerank** on the top-k, and **adaptive fusion** that weights
  lexical vs. semantic by query character (code-symbol queries → lexical; abstract queries →
  semantic).
- **Tier B — closed-loop relevance learning.** engrim uniquely has the signal: the minder *injects*
  a record, and the transcript log captures whether the conversation then *used* or *ignored* it.
  Mining inject-vs-used learns per-project relevance — boosting records that earn their injection.
  No markdown file or vanilla RAG tool can copy this; it needs the inject+log loop engrim already
  has.

## Other

- **`engrim export`** — round-trips `import`: dump records to markdown / JSON for backup and portability.
- **`PreCompact` checkpoint hook** — nudge a flush of uncaptured decisions right before the agent
  compacts its context.
- **Near-duplicate detection** — warn on a high-similarity `add` (embeddings already exist to catch it).
- **`engrim doctor`** — one-shot health: backend on?, embedded N/total, stale-state count, per-project
  token size, dup risk.
- **Record linking** — first-class edges so you can recall a neighborhood ("everything tied to this
  decision").

## Principles that won't change

- **Local & private.** No telemetry, no phone-home. Your memory stays on your machine. (The only
  network touch is a one-time embedding-model download; `ENGRIM_EMBED=off` removes even that.)
- **Minimal, vetted dependencies** — and a pure-standard-library lexical mode for a zero-third-party
  posture.
- **Retrieve the relevant slice — never dump raw context.**
- **Complement the engine, never intrude.** engrim amplifies your agent's native memory; it doesn't
  replace it or fight it.

Ideas and pull requests welcome.
