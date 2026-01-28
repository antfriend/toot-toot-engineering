# TTE-RFC-0001
## Toot Toot Engineering Workflow and Roles
### Version 1.0

Status: Draft

This RFC defines the core workflow, roles, and role discipline for TTE.

---

## 1. Roles
The following roles are defined:
- Bootstrap
- Orchestrator
- Storyteller
- SVG engineer
- Core worker
- Image producer
- PDF assembler
- Reviewer
- Delivery packager
- Retrospective

---

## 2. Role Discipline
- One step, one agent, one role.
- Agents proceed without human feedback between steps unless blocked.
- The human co-producer is only required for environment approvals or
  after the final step.

---

## 3. Cycle Rules
- Deliverables MUST be written to `deliverables/cycle-XX/`.
- Cycle 01 uses the prompt in `README.md`; later cycles use the
  prompt in that cycle's `BOOTSTRAP.md`.
- A step cannot be marked complete if its outputs contain placeholders.

End TTE-RFC-0001
