# Internal LLM gateway: Release notes

<!--
Answers: what changed for users and callers, newest first.
Reader: anyone who must act on a change. Call out breaking changes, model retirements and new limits.
Owns: the release history, release versioning, notice periods. Refers to: launch gate evidence (02 §11.2), setting values (04).
Detail: a gateway release = LiteLLM version + config version + IaC version. A model added or retired is a release even if no code changed. Every release gets a row in §2 and an entry in §4, written from the block template in §3.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Release policy

- **Versioning:** [fill: calendar versioning, for example 2026.11.1, or semantic versioning]
- **Where users are told:** [fill: channel, email list, Admin UI banner]
- **Notice for breaking changes and model retirements:** [fill: number of weeks]

## 2. Summary

| Version | Date | LiteLLM | Highlights | Action needed by users |
|---|---|---|---|---|
| EXAMPLE: 2026.12.0 | 2026-12-01 | 1.80.5 | First production release | None: Intune sets up Claude Code and Codex CLI |

## 3. Entry template

Copy this block into §4 for each release, newest first. Keep every heading; write "None" under a heading that has nothing to report.

```markdown
### <version> — <YYYY-MM-DD>
LiteLLM: <old> → <new> · Config: <commit> · IaC: <commit>
Launch gates: <all passed on staging on YYYY-MM-DD; evidence in 02 §11.2>

#### Models
- Added: <public model names, or "None">
- Retired: <names, and whether the alias now points elsewhere or is removed, or "None">

#### Changes
- <change, from the user's point of view>

#### Breaking changes and action needed
- <what breaks, who must act, and by when, or "None">

#### Fixed
- <fix, or "None">
```

## 4. Releases

### EXAMPLE: 2026.12.0 — 2026-12-01
LiteLLM: none → 1.80.5 · Config: `a1b2c3d` · IaC: `d4e5f6a`
Launch gates: all passed on staging on 2026-11-25; evidence in 02 §11.2

#### Models
- Added: `claude-opus`, `claude-haiku`
- Retired: None

#### Changes
- First production release, for engineers in the Tokyo offices.

#### Breaking changes and action needed
- None. Intune sets up Claude Code and Codex CLI.

#### Fixed
- None
