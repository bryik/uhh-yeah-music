# uhh-yeah-music

Scraping scripts used in a weekend project to build a Spotify playlist of UYD intros and outros. For more info, see [this blog post](https://blog.wsundine.com/post/spotify-doesn-t-have-a-playlist-importer/).

# Setup

1. Create a virtual environment
2. `pip install -r requirements.txt`

# Usage

## Scraping episodes

Run:

```bash
python scraper.py
```

The result should be `./uym.json`.

## Transforming to a list of songs

Run:

```bash
python songparser.py
```

The result should be `./uym-songs.json`.
