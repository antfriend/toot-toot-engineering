# My Mental Palace DB
A single-file semantic story database. This cycle stores the Toot Toot Engineering slideshow storyboard.
Agent note: users may refer to this DB and its actions (e.g., "select", "update", "insert", "delete", "upsert") using data-user parlance; interpret those requests as edits to this file's current cursor selection, DB properties, or records. If a request is ambiguous (e.g., multiple possible records), ask a short clarification or select the most recently updated matching record and state the assumption.

```mmpdb
db_id: mmpdb:cycle-01:slideshow
db_name: "Toot Toot Engineering Storyboard"
coord_increment:
  lat: 1
  lon: 1
collision_policy: southeast_step
timestamp_kind: unix_utc
cursor_policy:
  max_preview_chars: 240
  max_nodes: 24
typed_edges:
  enabled: true
  syntax: "type>@TARGET_ID"
  note: "Types are free-form tokens; edges remain directional."
```

```cursor
selected:
  - @SLIDE01
preview:
  @SLIDE01: "Opening foundry scene. Welcome and framing for the cycle."
agent_note: "Storyboard nodes map directly to slide groups in deliverables/cycle-01/SLIDESHOW-cycle.svg."
dot: |
  digraph Cursor {
    rankdir=LR;
    "@SLIDE01" -> "@SLIDE02" [label="leads_to"];
    "@SLIDE02" -> "@SLIDE03" [label="leads_to"];
  }
```

---

@SLIDE01 | created:1700002000 | updated:1700002000 | relates:leads_to>@SLIDE02

## Opening foundry
Welcome to Toot Toot Engineering. Establish the time foundry as the visual motif.

---

@SLIDE02 | created:1700002010 | updated:1700002010 | relates:leads_to>@SLIDE03

## Why it exists
Reliability and clarity for AI collaboration. No hidden magic.

---

@SLIDE03 | created:1700002020 | updated:1700002020 | relates:leads_to>@SLIDE04

## The cycle
Prompt, plan, roles, deliverables, review, delivery, retrospective.

---

@SLIDE04 | created:1700002030 | updated:1700002030 | relates:leads_to>@SLIDE05

## Start with a prompt
README.md contains the lantern prompt that sets the goal.

---

@SLIDE05 | created:1700002040 | updated:1700002040 | relates:leads_to>@SLIDE06

## Work in cycles
Each cycle has a folder and a plan with tracked outputs.

---

@SLIDE06 | created:1700002050 | updated:1700002050 | relates:leads_to>@SLIDE07

## PLAN.md
Critical path and current step. One step, one role, one output.

---

@SLIDE07 | created:1700002060 | updated:1700002060 | relates:leads_to>@SLIDE08

## LOG.md
Decisions and questions are logged for traceability.

---

@SLIDE08 | created:1700002070 | updated:1700002070 | relates:leads_to>@SLIDE09

## Roles overview
Roles take turns to keep the work focused and reviewable.

---

@SLIDE09 | created:1700002080 | updated:1700002080 | relates:leads_to>@SLIDE10

## Bootstrap
Interprets the prompt and proposes team and plan adjustments.

---

@SLIDE10 | created:1700002090 | updated:1700002090 | relates:leads_to>@SLIDE11

## Storyteller
Shapes the narrative arc and timing for the work.

---

@SLIDE11 | created:1700002100 | updated:1700002100 | relates:leads_to>@SLIDE12

## SVG engineer
Defines layout, legibility, and export constraints.

---

@SLIDE12 | created:1700002110 | updated:1700002110 | relates:leads_to>@SLIDE13

## Orchestrator
Maintains PLAN.md, AGENTS.md, and LOG.md to avoid drift.

---

@SLIDE13 | created:1700002120 | updated:1700002120 | relates:leads_to>@SLIDE14

## Core worker
Builds the real artifacts: slides, scripts, assets, or code.

---

@SLIDE14 | created:1700002130 | updated:1700002130 | relates:leads_to>@SLIDE15

## Reviewer
Finds gaps, risks, and missing tests before shipping.

---

@SLIDE15 | created:1700002140 | updated:1700002140 | relates:leads_to>@SLIDE16

## Delivery packager
Assembles final outputs and release notes with logo.

---

@SLIDE16 | created:1700002150 | updated:1700002150 | relates:leads_to>@SLIDE17

## Retrospective
Captures lessons and improvements for the next cycle.

---

@SLIDE17 | created:1700002160 | updated:1700002160 | relates:leads_to>@SLIDE18

## Deliverables folder
All outputs live in deliverables/cycle-XX.

---

@SLIDE18 | created:1700002170 | updated:1700002170 | relates:leads_to>@SLIDE19

## Logo rule
Every final deliverable includes the Toot Toot mark.

---

@SLIDE19 | created:1700002180 | updated:1700002180 | relates:leads_to>@SLIDE20

## Human involvement
Approve guardrails and give feedback after the final step.

---

@SLIDE20 | created:1700002190 | updated:1700002190 | relates:leads_to>@SLIDE21

## Start signal
Say go, proceed, or you got this to begin.

---

@SLIDE21 | created:1700002200 | updated:1700002200 | relates:leads_to>@SLIDE22

## Example output
A slideshow and monologue ready to record and publish.

---

@SLIDE22 | created:1700002210 | updated:1700002210 | relates:leads_to>@SLIDE23

## Quality bar
Cite sources and resolve placeholders before completion.

---

@SLIDE23 | created:1700002220 | updated:1700002220 | relates:leads_to>@SLIDE24

## Back to the foundry
The press stamps a finished artifact with confidence.

---

@SLIDE24 | created:1700002230 | updated:1700002230 | relates:closes>@SLIDE01

## Closing call to action
Return to the foundry and invite the viewer to start a cycle.
