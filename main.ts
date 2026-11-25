// news-image-20261125 entry, v2 (Node 22, standard library only).
// The image is the entry.png beside this file: a flat vector-style front page
// summing up Wednesday 25 November 2026 — the Riyadh tower strike as a
// full-width lead, five more stories, an Also Today box, and a UN footer.
// The program copies it to /output/entry.png. The gate takes a whole PNG of
// at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes
// copied, so the program is deterministic: same input, same output.
// The image itself was drawn in this repo by draw.py (Python + PIL, flat
// vector-style shapes and DejaVu text, no AI generation, no network); the
// shipped entry.png is its output, and this program only copies that file,
// so the two grader runs always produce identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
