// Entry program for the 23 November 2026 world-news image.
// It copies the front page rendered by draw.py into the grader's
// output directory. No network, no dependencies, no work beyond the copy.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outputDir, "entry.png"));
console.log(`entry.png written to ${outputDir}`);
