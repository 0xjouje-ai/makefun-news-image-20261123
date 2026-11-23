// SPDX-License-Identifier: MIT
// Entry program for the make.fun "Sum up 23 November's world news in
// one image" bounty. The poster itself is pre-drawn (entry.png, produced
// by draw.py in this repository); this program just places an exact copy
// of it at the grader's output path, so both runs write identical bytes.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error("entry.png is missing from this repository");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`wrote ${dest}`);
