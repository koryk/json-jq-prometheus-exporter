# Prometheus json exporter with jq

Prometheus endpoint for JSON files.

## Setup

### Dependencies
* Python 3+
* pip

### Install instructions
* `pip install -r requirements.txt`

### config instructions
The config file defines one or more url endpoints for exposing values from one or more JSON files.

The config JSON is an array of endpoints. For each endpoint we have the following values:
* *name* - friendly name
* *key_prefix* - prefix to add to all the prometheus gauges in this config
* *path* - is the URL path for the prometheus endpoint - in the example we use `/aqi/metrics`
* *json* - an array of objects describing the files and fields to extract gauges from. For each object, we expect the fields:
  * *path* - the path of the JSON file on local filesystem
  * *jq_map* - an object of the fields to extract where the key name is the appended to the prefix. The value is the jq syntax of the field. If it returns more than one value, the values will be indexed. https://stedolan.github.io/jq/manual/#Basicfilters

### running
* `python simple_prom_server.py`

### notes/caveats
* The current `config.json` is an example, you will need to rewrite it for your own needs
* This should not be used in production, it was written in a few hours
* This only exposes metrics as gauges - https://prometheus.io/docs/concepts/metric_types/
