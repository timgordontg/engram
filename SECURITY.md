# Security Policy

engrim is built to be safe to run on your own machine without a second thought. This document
states the security posture plainly and explains how to report anything that looks off.

## Posture

- **No telemetry; local-first.** engrim never phones home with your data and opens no sockets of its
  own. The single exception: the default semantic tier downloads a small embedding model from
  HuggingFace **once** on first run (cached forever after, then fully offline). Run `ENGRIM_EMBED=off`
  for a no-network, pure-standard-library posture with zero third-party code.
- **Minimal dependencies.** The core is pure Python standard library. The default semantic tier adds
  `model2vec` and its lightweight runtime deps (numpy, safetensors, tokenizers, huggingface-hub,
  joblib, tqdm, jinja2) — no torch, no transformers. Lexical mode (`ENGRIM_EMBED=off`) pulls none of
  them.
- **No dangerous primitives.** No `eval`, `exec`, `pickle`, `marshal`, `subprocess`, `os.system`,
  or shell execution anywhere in the code.
- **No unsafe deserialization.** Markdown frontmatter is parsed by hand — engrim does **not** use
  PyYAML/`yaml.load` or `pickle`, the classic remote-code-execution vectors.
- **No SQL injection surface.** Every value derived from user input is passed as a bound `?`
  parameter. Full-text queries are tokenized and quoted before they reach SQLite, so search terms
  containing code symbols or punctuation cannot inject query operators.
- **Private on disk.** The SQLite store is created owner-only (`0600`) on POSIX systems.
- **Local trust model.** engrim reads and writes a SQLite file you own. It does not run anything
  it stores.

## A note on `engrim import` and agent context

Records can be surfaced to an AI agent (e.g. via a Claude Code SessionStart hook). Treat imported
content the way you'd treat anything an agent will read: **only import from sources you trust.**
A markdown file from an untrusted source could contain text crafted to influence an agent that
later reads it — the same prompt-injection caution that applies to any document you feed a model.

## Reporting a vulnerability

Please report security issues privately via **GitHub Security Advisories**
(repo → **Security** tab → **Report a vulnerability**) rather than opening a public issue.

You'll get an acknowledgement, a fix or mitigation as quickly as is practical, and credit if you'd
like it. Thank you for helping keep engrim safe for everyone.
