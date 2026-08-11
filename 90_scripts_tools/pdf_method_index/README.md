# Local PDF / Image OCR Index

这是 Threading 的独立可选工具，用来把用户自己明确授权的 PDF 或图片材料
变成一个**带来源定位的本地检索索引**。它不是普通项目 onboarding 的必需步骤，
也不会把文件上传到 GitHub。

This is an optional standalone Threading tool. It turns explicitly authorised
local PDFs and images into a page- or image-anchored OCR retrieval index. It is
not required for the core profile or Dashboard workflow, and it does not upload
source files to GitHub.

## Boundary / 边界

- Supported inputs: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`, `.tif`, `.tiff`, `.bmp`.
- Without `--source-list`, only supported files directly inside `--source-dir`
  are read; subdirectories are not scanned.
- With `--source-list`, only the listed supported files below that directory are
  read. Path traversal is rejected.
- Derived OCR text and page records belong in the ignored
  `.academic_cache/pdf_index/` directory by default.
- The manifest records source labels and hashes, not the full local source path.
- OCR output is a locator and review aid, not verified quotation, empirical
  evidence or a project claim.
- After locating a page or image, visually check the original source and write a
  bounded evidence or reading note into the user's own Managed Workspace.

## Optional dependencies / 可选依赖

The core Threading workflow does not need these packages. Install them only in a
user-controlled environment when this index is needed:

```bash
python3 -m pip install -r 90_scripts_tools/pdf_method_index/requirements-optional.txt
```

## Build or resume an index / 建立或继续索引

```bash
python3 90_scripts_tools/pdf_method_index/build_week_pdf_index.py \
  --source-dir /path/to/authorised-pdf-and-image-files \
  --output-dir .academic_cache/pdf_index/my_project \
  --source-prefix my-project \
  --source-scope "My own authorised project sources"
```

The builder writes completed PDF pages and image records immediately and resumes
matching records on a later run. Use `--overwrite` when the source or OCR
configuration should be rebuilt. Use `--source-list` when a directory contains
files that must not be inspected.

Example source list:

```text
# one path relative to --source-dir per line
brief.pdf
field-photo-01.jpg
slides/method-map.png
```

## Search an index / 搜索索引

```bash
python3 90_scripts_tools/pdf_method_index/query_week_pdf_index.py \
  "Theory of Change" \
  --index .academic_cache/pdf_index/my_project/page_index.jsonl
```

The result includes a source label, page or image number, hit count, confidence
summary and a short OCR snippet. Use it to locate material, then inspect the
original page or image before citing or recording it as evidence.
