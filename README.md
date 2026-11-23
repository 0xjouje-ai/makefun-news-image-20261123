[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/0xjouje-ai/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/0xjouje-ai/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# Monday 23 November 2026 — The World in One Day

A newspaper front page that sums up Monday 23 November 2026 in a single
image, drawn from scratch with Python and Pillow.

## The day's five stories

- **COP31 collapses with no deal** — the EU and UK reject a text that never
  names fossil fuels; the longest COP on record ends with nothing.
- **Tankers burn in the Strait of Hormuz** — more tankers are struck and hit
  mines; attacks on shipping reach their highest level since the war began.
- **Sea drones sink a Russian warship** — suspected Ukrainian drones hit the
  corvette Merkury at Benghazi; the ship capsizes, 10 hurt.
- **Mexico captures "Chapo Isidro"** — Mexican forces seize the FBI's
  $5m-wanted Fausto Isidro Meza-Flores in Sinaloa after firefights kill 11.
- **Liverpool rout ten-man United** — in Pochettino's debut at Anfield, and
  Marquez seals an eighth MotoGP crown.

Every story above happened, or was first reported, on Monday 23 November 2026.

## How it works

`draw.py` renders the 1024×1024 front page (masthead, four story cards with
hand-drawn pictograms, a full-width sport strip) and saves it as `entry.png`.
`main.ts` copies `entry.png` to the output directory the grader provides.

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

This repository is an entry in the
[make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).
