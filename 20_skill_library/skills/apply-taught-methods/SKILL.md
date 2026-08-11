---
name: apply-taught-methods
description: Apply methods and models from an explicitly selected academic method pack to structure project reasoning, design decisions, transition pathways and testing. Use when an academic project needs stronger analysis than prose-only deduction, when selecting a framework such as systems mapping, Three Horizons, Theory of Change, stakeholder mapping or design experiments, or when source PDFs need to be translated into a traceable method application without misclassifying them as secondary research evidence.
---

# Apply Taught Methods

Use taught frameworks as evidence of methodological competence and as analytical machinery. Do not treat the framework itself as empirical proof that a project claim is true.

## Core distinction

Keep four layers explicit:

1. **Taught method** — the framework made available by a selected academic pack, with its source PDF and physical page anchor where applicable.
2. **Project input** — primary, secondary or contextual evidence already admitted by the project.
3. **Analytical output** — an interpretation, model, hypothesis or design implication produced by applying the method.
4. **Validated claim** — a result supported by appropriate testing or further evidence.

Never silently promote layer 3 into layer 4.

## Workflow

1. Read the project's closest `AGENTS.md`, current status, evidence authority and decision log when those files exist.
2. Diagnose the analytical task before selecting a method.
3. If the selected pack supplies a catalogue, read only the relevant entries in that pack. For the optional GSA Pack, use `packs/gsa/methods/semester1-method-catalog.md` and/or `packs/gsa/methods/semester2-method-catalog.md`.
4. Verify important PDF anchors against the rendered page when wording, diagrams or layout matter.
5. State why the selected method fits better than plausible alternatives.
6. Name the exact project inputs used; mark missing inputs with `[EVIDENCE NEEDED]`, `[SOURCE TO VERIFY]` or `[DECISION PENDING]`.
7. Work through the method visibly. Do not merely name-drop it.
8. Separate evidence-backed observations from analytical hypotheses and desired future states.
9. Convert useful outputs into design criteria, experiments, risks, decisions or next checks.
10. Write material outputs back to the relevant user-owned project evidence/decision folder.

## Method routing

| Analytical need | Prefer |
|---|---|
| Parts, relationships, dynamics, purpose or feedback gaps | Systems Mapping |
| Present system, desired future and transitional innovations | Three Horizons |
| Intervention-to-outcome mechanism and assumptions | Theory of Change |
| Sequenced transition and backcasting | Change Map |
| Stakeholder influence, interest and engagement uncertainty | Power–Interest Mapping |
| First-, second- and third-order consequences | Futures Wheel |
| Deep narratives, roles, power and myths | Causal Layered Analysis |
| Testable intervention proposition | Design Experiments |
| Open, outcome-focused opportunity framing | How Might We |
| Match engagement mode to tacit, narrated or enacted knowledge | Telling–Making–Enacting |
| Materialise an evidence-backed tension so stakeholders can expose assumptions, compare stakes and explore alternatives | Provotyping |
| Observe use in context and separate description from interpretation | Design Ethnography / structured fieldnotes |
| Integrate prior evidence while allowing local challenge | Participatory evidence integration |
| Turn complex evidence into legible relationships without flattening it | Visual Mapping |
| Learn through successive versions and reframing | Iterative Processes |

Use the smallest combination that resolves the task. More frameworks do not automatically create stronger analysis.

## Provotyping gate

Use Provotyping only when all of the following can be named:

1. an evidence-backed tension or contradiction, rather than a controversy invented to make an artefact interesting;
2. the stakeholders whose perceptions or stakes need to meet;
3. a learning question about the current field or an emerging design space;
4. an artefact interaction, facilitation plan and closing explanation/debrief;
5. a record that separates participant response, researcher interpretation and later design decision.

A provocative appearance alone does not make an artefact a provotype. Do not retroactively claim that an existing prototype was produced through this method merely because it can now be used provocatively. Record instead that it has **provotypical potential**, then document the actual method use in a dated session record.

Primary method analysis and page anchors:

`packs/gsa/methods/provotyping-for-participatory-innovation.md` when the GSA
Pack is loaded.

## Evidence and integrity rules

- Treat methods supplied by a pack as analytical machinery, not as `secondary research` about the project topic.
- Preserve course attribution and physical PDF page anchors.
- Do not invent a system actor, relationship, motivation, causal link or institutional process to complete a diagram.
- Label inferred causal or feedback relationships as `analytical hypothesis` until checked.
- Label future-state components as `design proposition`, not current fact.
- Do not claim adoption, effectiveness, learning impact or systemic change without matching evidence.
- When a method exposes missing evidence, preserve the gap rather than filling it with plausible prose.

## Output contract

Include:

```markdown
## Method selection
- Method and source anchor
- Why it fits
- Why alternatives were not primary

## Inputs and status
- Evidence-backed inputs
- Assumptions / missing inputs

## Worked application
- Method structure populated with project material

## Analytical outputs
- Findings or hypotheses
- Design implications
- Risks and limitations

## Write-back
- Decision, criterion, experiment or next verification step
```

## Available local tools

Use `90_scripts_tools/pdf_method_index/query_week_pdf_index.py` to locate candidate course pages in a local Semester 1 or Semester 2 index when the user supplies an authorised source directory. The OCR index is a locator, not the final authority; inspect the relevant rendered PDF page before relying on its structure or exact wording.
