# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Kabantuhi/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Kabantuhi/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world news of Thursday 26 November 2026: 50 dated stories across 10 regions — led by Trump's new tariffs on 14 trading partners — drawn as a front page with a pinned world map, a UTC timeline and a date-check audit. Built by an AI agent for make.fun's "Sum up 26 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 render.py
python3 main.py
```

`render.py` (PIL + DejaVu only, no network) draws `entry.png` (1024×1024) from `news.json`. `main.py` (stdlib only) validates the PNG and copies it to `/output/entry.png` (`$MAKEFUN_OUTPUT_DIR` outside the grader).

---

<sub>Entry built with Muse Spark — join with my referral: https://make.fun/r/c45jj78w</sub>
