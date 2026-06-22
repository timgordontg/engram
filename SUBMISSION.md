# Plugin directory submission — copy/paste source

Material for submitting engrim to the Claude Code community plugin directory.

**Where to submit:** the in-app form (not a GitHub PR).
- Individual author: Console → **platform.claude.com/plugins/submit**
- Team/Enterprise org with directory-management access: **claude.ai/admin-settings/directory/submissions/plugins/new**

**Before submitting:** run `claude plugin validate .` (the review pipeline runs the same
check, plus automated safety screening). Approved plugins are pinned to a commit SHA in
`anthropics/claude-plugins-community` and install as `@claude-community`; CI bumps the pin
as you push, and the public catalog syncs nightly.

**Positioning:** lead with honest daily-driver credibility ("I run it on my own work"),
never cold-test claims.

---

## Name

engrim

## Tagline (one line)

Cross-session memory for Claude Code — so you can `/clear` aggressively and never lose the *why*.

## Short description (listing card)

A local, project-scoped memory store that remembers your decisions and their rationale, then
hands back just the relevant slice — at session start and on every prompt. Clearing context
without it is like closing a long doc without hitting save; engrim is the save button. Hybrid
keyword + semantic retrieval over a tagged SQLite store. Self-installs on first run.

## Full description

Long Claude Code sessions accumulate the *reasoning* behind your work — why you chose Postgres
over SQLite, which approach you rejected and why, what the constraints are. The moment you
`/clear`, that rationale is gone, and you re-explain it next session. engrim fixes exactly that.

It wires four lifecycle hooks into your sessions:

- **SessionStart** — injects a budget-capped boot pack of your project's curated decisions, plus
  a tail of recent activity, so a fresh session starts already oriented.
- **UserPromptSubmit** — a lightweight "minder" pulls only the few records relevant to your
  current prompt (hybrid keyword + semantic ranking), so memory self-retrieves without you asking.
- **Stop** — quietly tails the transcript into an append-only log (never enters context).
- **SessionEnd** — a one-time, seed-gated mirror of your existing file-memory.

Everything is **local and project-scoped** — a tagged SQLite store at `~/.engrim`, self-scoped by
working directory, so one store serves many projects cleanly. The semantic embedder ships
bundled, so meaning-based recall works out of the box with no API key and no external calls. A
`review` command and an ambient status line tell you, honestly, whether your recent decisions are
captured before you clear.

**Why I built it:** I run engrim on my own daily work in Claude Code. The value I keep getting is
decision/rationale continuity — the "why we chose X" that's normally lost on `/clear` — and it
compounds the more aggressively you clear.

## Metadata

- **Repo:** https://github.com/timgordontg/engrim
- **License:** MIT
- **Requires:** `uv`, or `python3` with `pip`/`ensurepip` (hooks no-op gracefully if neither is present)
- **Marketplace:** `/plugin marketplace add timgordontg/engrim` then `/plugin install engrim@engrim`
