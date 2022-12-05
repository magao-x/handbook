lookyloo
========

If you want to actually look at your science data, you probably want it converted to FITS. This happens automatically for observations with the standard science cameras, but if you have special requirements you can run the exporter in standalone mode. The lookyloo tool identifies ``xrif`` archives written between the start and stop times of a particular observation (as indicated with the observing toggle in the UI), converts them with metadata and telemetry, and saves them in a folder hierarchy to keep things organized by target, observer, semester, etc.

(The exporter is using xrif2fits under the hood to perform the conversion. If you have advanced needs, that's the tool you probably want. You can use the ``--verbose`` switch to lookyloo to see the exact command line it's using to invoke xrif2fits.)

Examples
--------

Converting only camsci1 for observations in 2022A, saving to ``./my_output_dir/``::

    lookyloo -c camsci1 -s 2022A -D ./my_output_dir/

Converting ``camwfs`` image streams in their original cube format::

    lookyloo -c camwfs -C -s 2022A -D ./my_output_dir/

(Note: this will still give you multiple files, but each file will contain multiple frames. Note also that there is no telemetry in the headers when written in cube mode, because there is one header spanning multiple frames, which makes the "correct" value ambiguous.)

Help output
-----------

::

    usage: lookyloo [-h] [-d] [-r] [-i] [-C] [-S] [-v] [-t TITLE] [-e OBSERVER_EMAIL] [-p] [-s SEMESTER] [-c CAMERA]
                    [-X DATA_ROOT] [-O] [-T] [-D OUTPUT_DIR] [--xrif2fits-cmd XRIF2FITS_CMD]

    options:
    -h, --help            show this help message and exit
    -d, --daemon          Whether to start in daemon mode watching for new observations
    -r, --dry-run         Commands to run are printed in debug output (implies --verbose)
    -i, --ignore-history  When a history file (lookyloo_success.txt) is found under the output directory, don't skip files
                            listed in it
    -C, --cube-mode-all   (ignored in daemon mode) Whether to write all archives as cubes, one per XRIF, regardless of the
                            default for the device (implies --omit-telemetry)
    -S, --separate-mode-all
                            (ignored in daemon mode) Whether to write all archives as separate FITS files regardless of the
                            default for the device
    -v, --verbose         Turn on debug output
    -t TITLE, --title TITLE
                            (ignored in daemon mode) Title of observation to collect
    -e OBSERVER_EMAIL, --observer-email OBSERVER_EMAIL
                            (ignored in daemon mode) Skip observations that are not by this observer (matches substrings, case-
                            independent)
    -p, --partial-match-ok
                            (ignored in daemon mode) A partial match (title provided is found anywhere in recorded title) is
                            processed
    -s SEMESTER, --semester SEMESTER
                            Semester to search in, default: 2022B
    -c CAMERA, --camera CAMERA
                            Camera name (i.e. rawimages subfolder name), repeat to specify multiple names. (default: ['camsci1',
                            'camsci2', 'camlowfs', 'camwfs', 'camtip', 'camacq'])
    -X DATA_ROOT, --data-root DATA_ROOT
                            Search directory for telem and rawimages subdirectories, repeat to specify multiple roots. (default:
                            ['/opt/MagAOX', '/srv/icc/data', '/srv/rtc/data'])
    -O, --omit-telemetry  Whether to omit references to telemetry files
    -T, --omit-symlink-tree
                            Whether to skip constructing the parallel structure of symlinks organizing observations by observer
    -D OUTPUT_DIR, --output-dir OUTPUT_DIR
                            output directory, defaults to /data/obs
    --xrif2fits-cmd XRIF2FITS_CMD
                            Specify a path to an alternative version of xrif2fits here if desired

Daemon mode
-----------

The AOC runs an instance of lookyloo that just stays open forever, watching for new observation intervals to start. You can check its status with ``systemctl status lookyloo`` or tail its logs with ``sudo journalctl -fu lookyloo`` (both commands on AOC).