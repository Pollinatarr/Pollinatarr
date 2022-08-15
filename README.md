# uncross_seed: Find your uncross_seed torrents

`uncross_seed` is an app designed to help you find which torrents are not available on certain trackers
based on your existing torrents. It will only show you a list of releases name. You will have to upload torrents yourself.

## Requirements

-   [Python 3.10+](https://www.python.org/downloads/)
-   Any number of indexers that support Torznab (use Jackett or Prowlarr to
    help)

## Tutorial

1. Install uncross_seed by simply installing Python3.10
2. Install the requirements using this command :
```bash
python -m pip install -r requirements.txt
```
3. Create a config.yml file in the config folder, and edit it following the config.yml.sample
4. Run the script, happy sharing!


## Usage
To run the script in an interactive terminal with a list of possible commands run:
```bash
python uncross_seed.py -h
```

Note: The tool will ask your indexer manager for every torrent that are not already cross seeding. The task can be very long

## Troubleshooting

Feel free to
[open an issue](https://github.com/AthAshino/uncross_seed/issues/new)