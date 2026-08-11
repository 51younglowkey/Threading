# Provenance and Licensing Notes

## Optional method packs

The optional GSA Pack contains Semester 1 and Semester 2 catalogues, a
Provotyping method note, a reflection-document video-analysis protocol and a
Stage 3 assessment/ILO audit guide. The methods and protocol are paraphrased
guidance; the course PDFs, assessment forms and guidance videos are not included
in this repository. Course filenames and page numbers are source locators, not a
licence to redistribute the teaching materials.

### How the references work

- The generic `apply-taught-methods` skill can be used without an optional pack. The GSA catalogue is available only after the user selects the GSA Pack.
- A `Course anchor` identifies the teaching source and, where known, a physical page so a reader with authorised access can verify an important definition or diagram.
- The anchor is provenance, not a runtime dependency. Users without the original source can still use the paraphrased method guidance, but they should not claim to have checked the original page.
- `90_scripts_tools/pdf_method_index/` is optional. It runs only when a user supplies an authorised local `--source-dir` containing their own PDFs or images; the source files stay outside this repository and the derived OCR index stays ignored.
- The catalogues do not grant permission to reproduce the course slides, diagrams, extended quotations or assessment material.

For future releases, continue to review whether to:

1. retain the current locator detail;
2. replace it with a more general description of the method family;
3. publish only independently authored paraphrases and public references; or
4. obtain explicit permission for any material that goes beyond a short citation or abstract method summary.

The current public release uses independently authored paraphrases and source
locators without bundling restricted originals. Repeat this review when adding
new pack content.

## Assessment and reflection-document guidance

The GSA Pack includes a reusable analysis protocol for programme guidance videos
and an operational paraphrase of the Stage 3 ILOs, rubric dimensions and grade
bands for the current target cohort. These are scaffolds for local review, not
official assessment authority; verify the authorised source before reusing them
with another cohort.
The current official assessment PDF for the relevant cohort outranks the pack;
the pack does not include assessment forms, guidance videos, subtitles or
displayed student examples.

## Referenced public paper

The Boer and Donovan paper is referenced with bibliographic information and DOI
in the GSA Pack's Provotyping method note. Its PDF is not bundled in this
repository. Use a citation and link rather than redistributing a copy unless the
publisher's terms clearly permit it.

## GSA Pack naming

`GSA Pack` describes an independent academic pack for Design Innovation-related
workflows. It must not imply that the pack or Threading is produced, approved,
sponsored or endorsed by Glasgow School of Art unless explicit permission exists.
Add a clear independent-project disclaimer before publication.

The visible disclaimer is in `NOTICE.md` and at the top of `README.md`.

## Licence decision — confirmed

The owner accepted the split licence on 2026-08-10. Code, documentation, templates and sourced material receive different treatment:

- original scripts and software: **MIT License**;
- original documentation, templates and paraphrased method guidance: **CC BY 4.0**;
- third-party course material and the preserved paper: **no project licence**, with provenance and the original rights retained.

The implementation is in `LICENSE`, `LICENSE-DOCS.md` and `THIRD_PARTY_NOTICES.md`. The licence does not override the remaining provenance, copyright or public-release review.
