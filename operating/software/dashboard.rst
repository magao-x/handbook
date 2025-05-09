Telemetry and Data Dashboard
============================

The MagAO-X telemetry database is a PostgreSQL database running on AOC that collects device telemetry from the ``.bintel`` and ``.ndjson.gz`` files produced by instrument devices across the computers in MagAO-X. It also tracks the inventory of files for replication to backup volumes and remote sites.

The database is designed to be a central repository for all telemetry data produced by the instrument, and to provide a simple interface for querying and visualizing that data.

Usage
-----

(This assumes someone has set up the database as described in :ref:`setup_telemetry_database`.)

**TODO:** how to perform a query in the notebooks on exao1 and plot the result.

**TODO:** how to view / edit the Grafana dashboards.

