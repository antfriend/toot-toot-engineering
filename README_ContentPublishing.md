# TTE Content Publishing
![Toot Toot Engineering](images/time-foundry.svg)
[TTE is free, open-source software licensed under the MIT License.](https://antfriend.github.io/)   
![Release](https://img.shields.io/github/v/release/antfriend/toot-toot-engineering)

Workflow version: 3.8

# What is TTE Content Publishing?

TTE Content Publishing is the delivery side of the Toot Toot Engineering workflow. Each project cycle produces a set of primary artifacts — stories, scripts, firmware sketches, PDFs, or other media — along with structured delivery notes. Finished work is packaged per cycle and published to [antfriend.github.io](https://antfriend.github.io/).

The HUMANS/ directory contains materials intended for human readers rather than agents.

# How a cycle becomes a release

1. Run the TTE workflow to completion — see [The Toot Toot Workflow](README_TTworkflow.md)
2. Confirm primary artifacts exist and meet the quality bar (sources cited, third-party assets documented)
3. For document outputs, produce a print-ready PDF in `deliverables/cycle-XX/output/`
4. Add a delivery note at `deliverables/cycle-XX/DELIVERY.md`
5. Update `RELEASES.md` with the cycle entry and primary artifact links
6. Publish finished content to [antfriend.github.io](https://antfriend.github.io/)

# Deliverables structure

```
deliverables/
  cycle-XX/
    BOOTSTRAP.md       ← the prompt that started the cycle
    STORYTELLER.md     ← narrative / creative brief
    PLAN.md            ← critical path and step log
    REVIEW.md          ← reviewer sign-off
    DELIVERY.md        ← delivery notes and print specs
    assets/            ← source assets (images, data, etc.)
    output/            ← print-ready PDFs or final media
```

# Human-readable documentation

- [antfriend.github.io](https://antfriend.github.io/) — published guides and releases, readable without a Markdown renderer
- [HUMANS/Humon_ReadMe.md](HUMANS/Humon_ReadMe.md) — human-facing overview (agents should ignore unless asked)
- [RELEASES.md](RELEASES.md) — cycle-by-cycle release log

# Relevant RFCs

| RFC | Topic |
|-----|-------|
| [TTE-RFC-0001](RFCs/TTE-RFC-0001-Workflow-and-Roles.md) | Workflow and agent roles |
| [TTE-RFC-0002](RFCs/TTE-RFC-0002-Plan-Log-and-Checklist.md) | Plan, log, and checklist requirements |
| [TTE-RFC-0003](RFCs/TTE-RFC-0003-Definition-of-Done-and-Release.md) | Definition of done, release packaging, quality bar |
