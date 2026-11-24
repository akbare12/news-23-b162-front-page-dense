[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b162-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b162-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A one-image front page summing up 23 November 2026's world news: 31 stories
across 6 regions.

- **Heroes:** the AI rout hits Asia (Kospi −3.3% to 4,708.54), Guterres calls
  for AI regulation before it's too late (Bridgetown summit, 150 delegates),
  and the US lead over China hits a record low (Asia Power Index gap 5.3).
- **Also inside:** 10 cards, a 10-number strip, a world map with 13 numbered
  pins, an 18-item ALSO list, and a DATE CHECK box for stories that are NOT
  from 23 November.

## How it is built

`draw.py` (PIL) renders `entry.png` (1024×1024). `main.py` (stdlib only)
verifies the PNG and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`.
