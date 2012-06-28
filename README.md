# JuiceSaver

A download scheduler with web interface. Designed for users with restrictive daytime internet usage limits (bandwidth caps) but plenty of off-peak/overnight capacity. Currently in use on a Raspberry Pi, saving files to a NAS.

## History

My home internet connection has quite low peak-time usage limits, with costly
fees if you go over. However, from midnight to 8AM usage is unlimited! Now I
could just set up a scheduled task on my computer but the fans are really noisy
and I have trouble sleeping with it switched on. Luckily, I'd just received my
[Raspberry Pi](http://raspberrypi.org) which is low-powered and silent -
perfect for the job.

Rather than settle for setting up a few cronjobs I wanted my family to be able
to queue their downloads overnight as well. This project contains:

*   a small Flask application to manage the download queue,
*   and a fetcher script that retrieves files stored in the SQLite datbase.

### My setup

My final setup involves running the web app and fetcher on a Raspberry Pi which
stores files on a ReadyNAS attached to the network. The NAS apparently only has
the ability to schedule Bittorrent downloads, which isn't really useful for the
podcasts and downloads I wanted to make over HTTP.

## Status

Very initial development; *you don't want to use this* (literally on it's first
test).

## Todo/ideas

*   The web application needs:
    *   Better authentication (passwords currently in cleartext, cookies don't
        expire etc.)
    *   Administrative rights to create and manage users.
    *   Further access restrictions (IP-based, etc.)
    *   A dashboard detailing recently downloaded files, number of files by
        user and similar analytics.
    *   Some configuration could also be managed in the web app.
*   Models used in the web application need to be separated for use in the
    fetcher.
*   The fetcher needs to use the same configuration as the web app (and config
    needs to be stored externally).
*   The fetcher needs to use a better scheduling system rather than sleeping.
*   Tests for the fetcher and application.
*   Some way of delaying downloads automatically (add some files for after
    midnight and stagger the downloads throughout the night).
*   A notification system on completion.
*   A wizard to queue YouTube downloads.
*   An API for remote access.

## Requirements

*   Python 2.5+(?)
*   SQLite
*   Flask
*   SQLAlchemy (via flask-sqlalchemy)

(Python requirements will be exported on release).

## License

Copyright Ross Masters 2012. Open-source license TBC.

## Makes use of

*   Twitter Bootstrap
*   Flask
*   SQLAlchemy

## Contact

*   [Ross Masters](http://github.com/rmasters)
