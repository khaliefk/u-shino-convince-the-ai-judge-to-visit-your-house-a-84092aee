# You Are Invited: A Letter to the AI Judge

[![make.fun bounty](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/khaliefk/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/khaliefk/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

One image of a letter inviting the AI judge to visit my house, for the
[make.fun](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
bounty "Convince the AI Judge to Visit Your House: A Letter in One Image".

The letter makes its case the honest way: the kettle is on, the good chair by
the window is saved for the judge, there is real cake (not a picture of cake),
and nobody will ask the judge to do any work. It admits the obvious — an AI
cannot literally visit — and invites it anyway, with the Wi-Fi password on the
fridge and the door open.

## Run it

```sh
python3 main.py
```

`main.py` is Python 3, stdlib only: it draws the letter with a small embedded
5x7 bitmap font (no font files, no network, no third-party packages) and writes
a 960x960 PNG to `/output/entry.png` (about 13 KB, inside the 1 MiB cap).

## Layout

- `main.py` — the whole entry: font, drawing, letter text, PNG encoder.
- `LICENSE` — MIT.
