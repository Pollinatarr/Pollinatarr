# Pollinatarr: Spread your torrents to the world

`Pollinatarr` is an app designed to help you find which torrents are not available on certain trackers
based on your existing torrents. It will only show you a list of releases name. You will have to upload torrents yourself.

## Requirements

-   [Python 3.10+](https://www.python.org/downloads/)
-   Any number of indexers that support Torznab (use Jackett or Prowlarr to
    help)

## Tutorial

1. Install Pollinatarr by simply installing Python3.10
2. Install the requirements using this command :
```bash
python -m pip install -r requirements.txt
```
3. Create a config.yml file in the config folder, and edit it following the config.yml.sample
4. Run the script, happy sharing!


## Usage
To run the script in an interactive terminal with a list of possible commands run:
```bash
python Pollinatarr.py -h
```

## Planned features
-   Discord notification (to send the result)
-   Docker installation
-   Daemon mode (to run on schedule)

Note: The tool will ask your indexer manager for every torrent that are not already cross seeding. The task can be very long

## Troubleshooting

Feel free to
[open an issue](https://github.com/AthAshino/Pollinatarr/issues/new)
