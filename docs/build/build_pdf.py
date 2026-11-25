#!/usr/bin/env python3
"""Bangun satu PDF dokumentasi dari seluruh Markdown di folder docs/.

Pemakaian:
    python docs/build/build_pdf.py

Keluaran:
    docs/build/dokumentasi.html  (perantara)
    docs/build/Dokumentasi-Proyek.pdf

Catatan:
- Diagram Mermaid BELUM dirender menjadi gambar oleh skrip ini (butuh Node/mermaid-cli).
  Di PDF, blok diagram ditampilkan sebagai kotak sumber bertanda. Sebelum menyerahkan,
  ekspor setiap diagram ke PNG dari mermaid.live lalu ganti blok tersebut dengan gambar.
- Konversi PDF memakai LibreOffice headless.
"""

from __future__ import annotations

import base64
import hashlib
import html
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import markdown

DOCS_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = DOCS_DIR / "build"

# Urutan dan judul bab pada PDF akhir.
DOCS = [
    ("00-identitas-dan-rencana-proyek.md", "Bab 1 — Identitas Kelompok dan Rencana Proyek"),
    ("01-latar-belakang-dan-tujuan.md", "Bab 2 — Latar Belakang, Tujuan, dan Ruang Lingkup"),
    ("02-stakeholder-dan-hak-akses.md", "Bab 3 — Stakeholder dan Hak Akses"),
    ("03-SRS.md", "Bab 4 — Software Requirements Specification (SRS)"),
    ("04-rancangan-sistem.md", "Bab 5 — Rancangan Sistem"),
    ("05-model-pengembangan.md", "Bab 6 — Model Pengembangan Perangkat Lunak"),
    ("06-manajemen-risiko.md", "Bab 7 — Manajemen Risiko"),
    ("07-rencana-dan-hasil-pengujian.md", "Bab 8 — Rencana dan Hasil Pengujian"),
    ("08-matriks-keterlacakan.md", "Bab 9 — Matriks Keterlacakan"),
    ("09-teknologi-dan-struktur-kode.md", "Bab 10 — Teknologi, Struktur Kode, dan Konvensi"),
    ("10-panduan-screenshot-dan-video.md", "Bab 11 — Panduan Screenshot dan Video"),
    ("11-checklist-pengumpulan.md", "Bab 12 — Checklist Pengumpulan"),
    ("12-database-dan-backup.md", "Bab 13 — Basis Data Online dan Cadangan"),
]

CSS = """
@page { size: A4; margin: 2cm 1.8cm; }
body { font-family: 'Liberation Serif', 'Times New Roman', serif; font-size: 10.5pt;
       color: #1a1a1a; line-height: 1.45; }
.doc { page-break-before: always; }
h1 { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 18pt; color: #1E293B;
     border-bottom: 2px solid #F59E0B; padding-bottom: 4pt; margin: 0 0 14pt 0; }
h2 { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 13pt; color: #1E293B;
     margin: 16pt 0 6pt 0; page-break-after: avoid; }
h3 { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 11pt; color: #334155;
     margin: 12pt 0 4pt 0; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt 0; page-break-after: avoid; }
p { margin: 0 0 6pt 0; text-align: left; }
ul, ol { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin-bottom: 2pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 12pt 0; font-size: 8.5pt;
        page-break-inside: auto; }
th { background: #E2E8F0; color: #111827; text-align: left; padding: 3pt 4pt;
     border: 0.5pt solid #94A3B8; vertical-align: top; font-weight: bold; }
td { border: 0.6pt solid #94A3B8; padding: 3pt 4pt; vertical-align: top; }
tr:nth-child(even) td { background: #F1F5F9; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; background: #F1F5F9;
       padding: 0 2pt; }
/* white-space: pre (bukan pre-wrap): LibreOffice menggantung saat membungkus
   baris panjang pada blok kode. Font dikecilkan agar tetap di dalam margin. */
pre { background: #F8FAFC; border: 0.5pt solid #CBD5E1; padding: 5pt; font-size: 7pt;
      font-family: 'DejaVu Sans Mono', monospace; white-space: pre;
      page-break-inside: avoid; }
blockquote { border-left: 3pt solid #F59E0B; background: #FFFBEB; margin: 8pt 0;
             padding: 6pt 8pt; }
blockquote p { margin: 0; }
.diagram { text-align: center; page-break-after: avoid; margin: 8pt 0 2pt 0; }
.diagram-note { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 8.5pt;
                color: #92400E; background: #FFFBEB; border: 0.5pt dashed #F59E0B;
                padding: 3pt 5pt; margin-top: 10pt; }
.cover { text-align: center; padding-top: 4cm; }
.cover .kicker { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 11pt;
                 color: #64748B; }
.cover h1 { border: none; font-size: 30pt; margin: 0.6cm 0 0.2cm 0; color: #1E293B; }
.cover .sub { font-size: 13pt; color: #334155; }
.cover .meta { margin-top: 2.5cm; font-size: 11pt; line-height: 1.8; }
.cover .rule { width: 40%; margin: 1cm auto; border-top: 3px solid #F59E0B; }
.toc { page-break-before: always; }
.toc li { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 10pt;
          margin-bottom: 4pt; list-style: none; }
"""


def strip_md_links(text: str) -> str:
    """Ubah [teks](berkas.md#anchor) menjadi 'teks' agar PDF tidak berisi tautan mati."""
    return re.sub(r"\[([^\]]+)\]\([^)]*\.md(?:#[^)]*)?\)", r"\1", text)


IMG_DIR = BUILD_DIR / "img"


def png_size(data: bytes) -> tuple[int, int]:
    if len(data) < 24:
        return (0, 0)
    return struct.unpack(">II", data[16:24])


def mermaid_png(source: str) -> bytes | None:
    """Render diagram Mermaid menjadi PNG lewat kroki.io (tanpa Node).

    Hasil di-cache di docs/build/img agar build ulang tidak memanggil jaringan terus.
    """
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
    cached = IMG_DIR / f"mermaid-{digest}.png"
    if cached.exists():
        return cached.read_bytes()

    request = urllib.request.Request(
        "https://kroki.io/mermaid/png",
        data=source.encode("utf-8"),
        headers={"Content-Type": "text/plain", "User-Agent": "SIKULIAH-docs/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError):
        return None
    if not data.startswith(b"\x89PNG"):
        return None
    cached.write_bytes(data)
    return data


def render_mermaid_blocks(body: str) -> str:
    pattern = re.compile(r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.DOTALL)

    def repl(match: re.Match[str]) -> str:
        source = html.unescape(match.group(1)).strip("\n")
        data = mermaid_png(source)
        if data is None:
            return (
                '<div class="diagram-note">Diagram Mermaid — render gagal; ekspor PNG dari '
                "mermaid.live sebelum menyerahkan PDF.</div>"
                f"<pre>{html.escape(source)}</pre>"
            )
        width, height = png_size(data)
        scale = 1.0
        if width:
            scale = min(620 / width, 640 / height, 1.0) if height else min(620 / width, 1.0)
        display_width = max(int(width * scale), 120) if width else 620
        encoded = base64.b64encode(data).decode("ascii")
        return (
            f'<p class="diagram"><img src="data:image/png;base64,{encoded}" '
            f'width="{display_width}" alt="Diagram Mermaid"></p>'
        )

    return pattern.sub(repl, body)


def soffice_command() -> list[str]:
    """Pilih binary LibreOffice yang aman dijalankan headless.

    `soffice` polos dapat menggantung di lingkungan tanpa profil pengguna yang bisa ditulis.
    Skrip pembungkus (jika tersedia) mengatur HOME dan profil sementara.
    """
    import glob
    import os

    env_cmd = os.environ.get("SOFFICE_CMD")
    if env_cmd:
        return env_cmd.split()
    for pattern in (
        "/home/*/.claude/skills/synced/*/pptx/scripts/office/soffice.py",
        str(Path.home() / ".claude/skills/**/office/soffice.py"),
    ):
        matches = glob.glob(pattern, recursive=True)
        if matches:
            return [sys.executable, sorted(matches)[0]]
    return ["soffice"]


def kill_soffice() -> None:
    """Hentikan sisa proses LibreOffice yang memegang lock profil.

    Tanpa ini, konversi kedua dan seterusnya akan menggantung sampai timeout.
    Pola [s]office membuat pkill tidak mencocokkan baris perintahnya sendiri.
    """
    subprocess.run(
        ["pkill", "-9", "-f", "[s]office.bin"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def convert(html_text: str, name: str) -> Path:
    """Render HTML menjadi PDF lewat LibreOffice di direktori sementara."""
    tmp = Path(tempfile.mkdtemp(prefix=f"sikuliah-{name}-"))
    source = tmp / f"{name}.html"
    source.write_text(html_text, encoding="utf-8")

    for attempt in (1, 2):
        kill_soffice()
        try:
            subprocess.run(
                [
                    *soffice_command(),
                    "--headless",
                    "--norestore",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(tmp),
                    str(source),
                ],
                check=True,
                timeout=180,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
            print(f"[percobaan {attempt}] konversi {name} gagal: {exc}", file=sys.stderr)
            continue
        produced = tmp / f"{name}.pdf"
        if produced.exists() and produced.stat().st_size > 0:
            final = BUILD_DIR / f".part-{name}.pdf"
            shutil.copyfile(produced, final)
            return final

    raise RuntimeError(f"Gagal membuat PDF bagian '{name}'")


def fragment(filename: str) -> str:
    path = DOCS_DIR / filename
    if not path.exists():
        print(f"[peringatan] tidak ditemukan: {path}", file=sys.stderr)
        return ""
    text = strip_md_links(path.read_text(encoding="utf-8"))
    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"]
    )
    return f'<div class="doc">{render_mermaid_blocks(body)}</div>'


def wrap(body: str, title: str = "Dokumentasi Proyek SIKULIAH") -> str:
    return (
        "<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    )


def build() -> int:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    cover = """
<div class="cover">
  <p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>
  <div class="kicker">TUGAS 1 KELOMPOK &mdash; REKAYASA PERANGKAT LUNAK</div>
  <h1>SIKULIAH</h1>
  <div class="sub">Learning Management System Kampus Berbasis Web<br/>Python &middot; Django</div>
  <div class="rule"></div>
  <div class="meta">
    <strong>Kelompok 22</strong><br/>
    Ridwan Rasyid &mdash; 1003260037<br/>
    <em>Dikerjakan mandiri atas persetujuan dosen pengampu</em><br/><br/>
    Institut Teknologi Tangerang Selatan<br/>
    November 2026
  </div>
</div>
"""

    toc_items = "\n".join(f"<li>{title}</li>" for _, title in DOCS)
    toc = f'<div class="toc"><h1>Daftar Isi</h1><ol>{toc_items}</ol></div>'

    # Dibagi tiga bagian: tiap konversi lebih kecil dan lebih andal.
    parts = [
        convert(wrap(cover), "sampul"),
        convert(wrap(toc), "daftar-isi"),
        convert(wrap("".join(fragment(f) for f, _ in DOCS[:6])), "bagian-1"),
        convert(wrap("".join(fragment(f) for f, _ in DOCS[6:])), "bagian-2"),
    ]

    target = BUILD_DIR / "Dokumentasi-Proyek.pdf"
    if shutil.which("pdfunite"):
        subprocess.run(
            [*["pdfunite"], *[str(p) for p in parts], str(target)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for part in parts:
            part.unlink(missing_ok=True)
    else:
        shutil.copyfile(parts[0], target)
        print("[peringatan] pdfunite tidak ada; PDF hanya berisi sampul", file=sys.stderr)

    kill_soffice()
    print(f"PDF dibuat: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
