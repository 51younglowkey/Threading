#!/usr/bin/env python3
"""Build a page-anchored OCR index for authorised PDFs and images.

Source files are opened read-only. Derived OCR records are written under the
git-ignored ``.academic_cache`` directory by default. This tool is optional;
the core Threading profile and Dashboard do not require its dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DIR = ROOT / "course_sources"
DEFAULT_OUTPUT_DIR = ROOT / ".academic_cache" / "pdf_index" / "week_pdf"
INDEX_VERSION = 2
RENDER_DPI = 180
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
SUPPORTED_EXTENSIONS = PDF_EXTENSIONS | IMAGE_EXTENSIONS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OCR an explicitly authorised PDF/image directory with page anchors."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Directory containing explicitly authorised PDF and image files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Derived cache directory. Keep this outside version control.",
    )
    parser.add_argument(
        "--source-list",
        type=Path,
        default=None,
        help="Optional UTF-8 file containing one supported file path relative to source-dir per line.",
    )
    parser.add_argument(
        "--source-prefix",
        default="course-materials",
        help="Stable source label written before each source-relative path.",
    )
    parser.add_argument(
        "--source-scope",
        default="Explicitly authorised local PDF/image directory only",
        help="Human-readable scope statement stored in the manifest.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Rebuild pages/images even when a matching cached record exists.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional source-file limit for diagnostics.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def document_id(path: Path) -> str:
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", path.stem).strip("-") or "document"
    suffix = hashlib.sha1(path.name.encode("utf-8")).hexdigest()[:10]
    return f"{safe_stem}-{suffix}"


def source_label(source_dir: Path, source_path: Path, source_prefix: str) -> str:
    return str(Path(source_prefix) / source_path.relative_to(source_dir))


def read_source_list(source_dir: Path, source_list: Path) -> list[Path]:
    source_paths: list[Path] = []
    for line_number, raw_line in enumerate(
        source_list.read_text(encoding="utf-8").splitlines(), start=1
    ):
        entry = raw_line.strip()
        if not entry or entry.startswith("#"):
            continue
        candidate = (source_dir / entry).resolve()
        if source_dir not in candidate.parents:
            raise ValueError(f"Source-list entry escapes source-dir at line {line_number}: {entry}")
        if not candidate.is_file() or candidate.suffix.lower() not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ValueError(
                f"Missing or unsupported source-list entry at line {line_number}: {entry} "
                f"(supported: {supported})"
            )
        source_paths.append(candidate)
    return sorted(set(source_paths), key=lambda path: str(path.relative_to(source_dir)).casefold())


def normalise_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def load_cached_pages(
    path: Path,
    source_sha256: str,
    expected_source_label: str,
    expected_render_dpi: int | None,
) -> dict[int, dict[str, Any]]:
    if not path.exists():
        return {}
    pages: dict[int, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            if (
                record.get("index_version") == INDEX_VERSION
                and record.get("source_sha256") == source_sha256
                and record.get("source_label") == expected_source_label
                and record.get("render_dpi") == expected_render_dpi
            ):
                pages[int(record["page_number"])] = record
    return pages


def load_optional_dependencies() -> tuple[Any, Any, Any, Any, Any] | None:
    """Load OCR dependencies only after argument parsing and source validation."""

    try:
        import numpy as np
        import pypdfium2 as pdfium
        from PIL import Image
        from rapidocr import RapidOCR
    except (ImportError, OSError) as exc:
        missing = getattr(exc, "name", None) or str(exc)
        requirements = Path(__file__).with_name("requirements-optional.txt")
        print(
            "Optional PDF/image indexing dependencies are missing: "
            f"{missing}. Install them in your own environment with:\n"
            f"  python3 -m pip install -r {requirements}\n"
            "The core Threading Dashboard does not require these dependencies.",
            file=sys.stderr,
        )
        return None
    try:
        engine = RapidOCR()
    except (ImportError, OSError) as exc:
        requirements = Path(__file__).with_name("requirements-optional.txt")
        print(
            "The OCR engine could not start: "
            f"{exc}\nInstall the optional dependencies with:\n"
            f"  python3 -m pip install -r {requirements}\n"
            "The core Threading Dashboard does not require these dependencies.",
            file=sys.stderr,
        )
        return None
    return np, pdfium, Image, RapidOCR, engine


def ocr_lines(engine: Any, np_module: Any, rendered: Any) -> tuple[list[dict[str, Any]], str]:
    result = engine(np_module.asarray(rendered))
    txts = getattr(result, "txts", None)
    boxes = getattr(result, "boxes", None)
    scores = getattr(result, "scores", None)
    if txts is None and isinstance(result, (tuple, list)) and len(result) >= 3:
        boxes, txts, scores = result[0], result[1], result[2]

    lines: list[dict[str, Any]] = []
    if txts is not None and boxes is not None and scores is not None and len(txts) > 0:
        for box, text, score in zip(boxes, txts, scores):
            cleaned = str(text).strip()
            if not cleaned:
                continue
            lines.append(
                {
                    "text": cleaned,
                    "confidence": round(float(score), 6),
                    "bbox_px": [[round(float(x), 2), round(float(y), 2)] for x, y in box],
                }
            )
    return lines, "\n".join(line["text"] for line in lines)


def build_record(
    *,
    engine: Any,
    np_module: Any,
    rendered: Any,
    native_text: str,
    source_path: Path,
    source_dir: Path,
    source_prefix: str,
    source_sha256: str,
    doc_id: str,
    source_type: str,
    page_number: int,
    page_count: int,
    render_dpi: int | None,
) -> dict[str, Any]:
    lines, ocr_text = ocr_lines(engine, np_module, rendered)
    search_text = normalise_text("\n".join(part for part in (native_text, ocr_text) if part))
    scores = [line["confidence"] for line in lines]

    return {
        "index_version": INDEX_VERSION,
        "document_id": doc_id,
        "source_type": source_type,
        "file_name": source_path.name,
        "source_label": source_label(source_dir, source_path, source_prefix),
        "source_sha256": source_sha256,
        "page_number": page_number,
        "page_count": page_count,
        "page_width_px": rendered.width,
        "page_height_px": rendered.height,
        "render_dpi": render_dpi,
        "ocr_engine": "RapidOCR",
        "native_text": native_text,
        "ocr_text": ocr_text,
        "search_text": search_text,
        "ocr_lines": lines,
        "mean_confidence": round(fmean(scores), 6) if scores else None,
        "low_confidence_line_count": sum(score < 0.65 for score in scores),
    }


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def index_pdf(
    *,
    pdfium: Any,
    engine: Any,
    np_module: Any,
    source_path: Path,
    source_dir: Path,
    source_prefix: str,
    source_sha256: str,
    doc_id: str,
    cache_path: Path,
    cached: dict[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    document = pdfium.PdfDocument(str(source_path))
    page_count = len(document)
    records: list[dict[str, Any]] = []
    try:
        print(f"{source_path.name}: {page_count} pages")
        for zero_based_page in range(page_count):
            page_number = zero_based_page + 1
            if page_number in cached:
                record = cached[page_number]
            else:
                page = document[zero_based_page]
                try:
                    scale = RENDER_DPI / 72
                    rendered = page.render(scale=scale).to_pil().convert("RGB")
                    native_text = normalise_text(page.get_textpage().get_text_range())
                    record = build_record(
                        engine=engine,
                        np_module=np_module,
                        rendered=rendered,
                        native_text=native_text,
                        source_path=source_path,
                        source_dir=source_dir,
                        source_prefix=source_prefix,
                        source_sha256=source_sha256,
                        doc_id=doc_id,
                        source_type="pdf",
                        page_number=page_number,
                        page_count=page_count,
                        render_dpi=RENDER_DPI,
                    )
                finally:
                    page.close()
                print(f"  page {page_number}/{page_count}: {len(record['ocr_lines'])} lines")
            records.append(record)
            # Make every completed page recoverable after interruption.
            write_jsonl(cache_path, records)
    finally:
        document.close()
    return records, page_count


def index_image(
    *,
    image_module: Any,
    engine: Any,
    np_module: Any,
    source_path: Path,
    source_dir: Path,
    source_prefix: str,
    source_sha256: str,
    doc_id: str,
    cache_path: Path,
    cached: dict[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    if 1 in cached:
        records = [cached[1]]
        write_jsonl(cache_path, records)
        return records, 1

    with image_module.open(source_path) as image:
        rendered = image.convert("RGB")
    record = build_record(
        engine=engine,
        np_module=np_module,
        rendered=rendered,
        native_text="",
        source_path=source_path,
        source_dir=source_dir,
        source_prefix=source_prefix,
        source_sha256=source_sha256,
        doc_id=doc_id,
        source_type="image",
        page_number=1,
        page_count=1,
        render_dpi=None,
    )
    write_jsonl(cache_path, [record])
    print(f"  image: {len(record['ocr_lines'])} lines")
    return [record], 1


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not source_dir.is_dir():
        print(f"Source directory does not exist: {source_dir}", file=sys.stderr)
        return 2
    if args.limit is not None and args.limit <= 0:
        print("--limit must be a positive integer", file=sys.stderr)
        return 2

    try:
        if args.source_list is not None:
            source_list = args.source_list.expanduser().resolve()
            if not source_list.is_file():
                print(f"Source list does not exist: {source_list}", file=sys.stderr)
                return 2
            source_paths = read_source_list(source_dir, source_list)
        else:
            source_paths = sorted(
                (
                    path
                    for path in source_dir.iterdir()
                    if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
                ),
                key=lambda path: path.name.casefold(),
            )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.limit is not None:
        source_paths = source_paths[: args.limit]
    if not source_paths:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        print(
            f"No authorised PDF/image sources resolved under: {source_dir} "
            f"(supported: {supported})",
            file=sys.stderr,
        )
        return 2

    dependencies = load_optional_dependencies()
    if dependencies is None:
        return 2
    np_module, pdfium, image_module, _rapid_ocr_class, engine = dependencies

    documents_dir = output_dir / "documents"
    documents_dir.mkdir(parents=True, exist_ok=True)
    document_summaries: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for source_index, source_path in enumerate(source_paths, start=1):
        source_sha256 = sha256_file(source_path)
        doc_id = document_id(source_path)
        cache_path = documents_dir / f"{doc_id}.jsonl"
        source_kind = "pdf" if source_path.suffix.lower() in PDF_EXTENSIONS else "image"
        expected_dpi = RENDER_DPI if source_kind == "pdf" else None
        expected_label = source_label(source_dir, source_path, args.source_prefix)
        cached = (
            {}
            if args.overwrite
            else load_cached_pages(cache_path, source_sha256, expected_label, expected_dpi)
        )

        try:
            if source_kind == "pdf":
                records, page_count = index_pdf(
                    pdfium=pdfium,
                    engine=engine,
                    np_module=np_module,
                    source_path=source_path,
                    source_dir=source_dir,
                    source_prefix=args.source_prefix,
                    source_sha256=source_sha256,
                    doc_id=doc_id,
                    cache_path=cache_path,
                    cached=cached,
                )
            else:
                records, page_count = index_image(
                    image_module=image_module,
                    engine=engine,
                    np_module=np_module,
                    source_path=source_path,
                    source_dir=source_dir,
                    source_prefix=args.source_prefix,
                    source_sha256=source_sha256,
                    doc_id=doc_id,
                    cache_path=cache_path,
                    cached=cached,
                )
        except Exception as exc:  # Preserve failures without mislabelling the source.
            failures.append(
                {
                    "file_name": source_path.name,
                    "source_type": source_kind,
                    "status": "fetch_failed",
                    "error": str(exc),
                }
            )
            print(f"  FAILED: {source_path.name}: {exc}", file=sys.stderr)
            continue

        all_records.extend(records)
        document_summaries.append(
            {
                "document_id": doc_id,
                "source_type": source_kind,
                "file_name": source_path.name,
                "source_label": expected_label,
                "source_sha256": source_sha256,
                "page_count": page_count,
                "indexed_pages": len(records),
                "bytes": source_path.stat().st_size,
                "cache_file": str(cache_path.relative_to(output_dir)),
            }
        )
        print(f"[{source_index}/{len(source_paths)}] indexed {source_path.name}")

    all_records.sort(key=lambda record: (record["file_name"].casefold(), record["page_number"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "page_index.jsonl", all_records)
    manifest = {
        "index_version": INDEX_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_scope": args.source_scope,
        "source_dir_name": source_dir.name,
        "source_list_used": bool(args.source_list),
        "render_dpi": RENDER_DPI,
        "ocr_engine": "RapidOCR",
        "supported_source_types": sorted(SUPPORTED_EXTENSIONS),
        "document_count": len(document_summaries),
        "page_count": len(all_records),
        "documents": document_summaries,
        "failures": failures,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Indexed {len(all_records)} pages/images from {len(document_summaries)} sources; "
        f"failures={len(failures)}; output={output_dir}"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
