# Threading — Extraction Status

Created: 2026-08-10
Status: v0.2 release prepared locally; public branch/tag verification pending

## Purpose

This project is separated from a private academic workspace so it can become a reusable Threading workspace for peers whose individual project context differs but whose academic workflow needs are substantially shared. The GSA Pack is retained as an optional Design Innovation-related academic context, not as the identity of the core project.

## Source boundary

The source workspace remains unchanged. This directory has its own Git repository and does not inherit the source repository's Git history.

## Removed from this copy

- the complete personal Stage 3 project archive, including evidence, interviews, tutor feedback, prototypes, submissions and project-specific outputs;
- academic-year and assessment-reference archives;
- calendar, timetable, deadline and submission records;
- presentations and portfolio exports;
- personal correspondence and handoff/synchronisation records;
- local transfer manifests and project-specific build/automation scripts;
- previously identified raw participant notes, consent forms, participant tracker and research-administration files;
- caches, local backups, dependencies, generated build output and common local secret formats.

## Retained

- reusable workflow and repository rules;
- the optional GSA Pack with Semester 1 and Semester 2 methods, Provotyping,
  reflection-document analysis guidance and Stage 3 assessment/ILO scaffold;
- the verified Provotyping method reference, without its source PDF;
- neutral evidence, reading, interview, prototype-testing and progress templates;
- bounded method-indexing, markdown-indexing and file-backup utilities;
- general evidence-chain and retrospective-warning guidance, pending final review.
- a legacy user-owned project-profile scaffold and clearly labelled synthetic example;
- onboarding, publication-checklist and provenance/licensing notes.
- the confirmed split licence: MIT for original tools, CC BY 4.0 for original documentation/templates, and no Threading licence for third-party material.

## Historical pre-publication gate

At extraction time, the retained tree still required a full privacy, provenance and generalisation review. The historical gate was:

1. scan all retained text, metadata and binary documents for personal or institution-specific material;
2. verify every method source locator and remove unsupported local-path claims;
3. replace remaining project-specific language with neutral examples or explicit placeholders;
4. review templates for data-minimisation and consent safeguards;
5. verify setup and core workflows from a clean environment;
6. inspect the complete Git diff and repository contents before the first public push.

The first local baseline should be committed only after this working tree review; it must not be pushed to GitHub yet.

At the time of extraction, no GitHub publication was authorised by this record.

## Supersession note — 2026-08-11

The owner subsequently authorised a public GitHub release of this cleaned
Threading edition. The historical extraction gate above records the state before
that decision; it does not authorise adding personal project material or
restricted originals. The public edition keeps the GSA assessment content as an
operational paraphrase and keeps the PDF/image index optional and local-first.

## Current v0.2 status — 2026-08-11

The v0.2 implementation adds Git-ignored Managed Workspaces under
`projects/local/<slug>/`, an installable natural-language Skill, existing-project
adoption, legacy migration, Figma evolution candidates, chat reconciliation,
linked read-only GSA activation, safe update checks and a local doctor. The
legacy `profiles/` layer remains only as a migration path; it is not the default
project storage model.
