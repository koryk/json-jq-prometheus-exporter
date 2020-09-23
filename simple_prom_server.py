from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, Gauge
import json
import sys
import jq
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO

#.rxs.obs[0].msg.aqi
#"name":"AQI",
#"key_prefix":"home_aqi_",
#"json_path":"/home/kory/air_qual_light/aqi_output.json",
#"path":"/aqi/metrics",
#"jq_map":".rxs.obs[0].msg.aqi"
#

class MyHandler(SimpleHTTPRequestHandler):
    config = None
    def send_head(self):
        self.pull_config()
        path = self.check_paths()

        response_code = 404
        if path is None:
            body = "404 Not Found"
        else:
            registry = self.prometheus_temperature(path)
            response_code = 200
            body = generate_latest(registry)
        self.send_response(response_code)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return BytesIO(body)

    def check_paths(self):
        print(self.config)
        for entry in self.config:
            if entry['path'] == self.path:
                return entry
        return None

    def prometheus_temperature(self,paths):
        registry = CollectorRegistry()
        #json config file request /path -> json path
        #json config defines: key_prefix, json file, request path, meta name
        for path in paths['json']:
            with open(path['path'], 'r') as f:
                json_data = json.load(f)
                for result_key in path['jq_map']:
                    results = jq.all(path['jq_map'][result_key],json_data)
                    print(results)
                    if len(results) <= 1:
                        suffix = ''
                    else:
                        suffix = 0
                    print(len(results))
                    for r in results:
                        gauge_key = paths['key_prefix']+result_key+str(suffix)
                        g = Gauge(gauge_key, paths['name'], registry=registry)
                        if isinstance(suffix, int):
                            suffix+=1
                        g.set(str(r))
        return registry

    def pull_config(self):
        if self.config is not None:
            return
        with open('config.json') as json_file:
            self.config = json.load(json_file)


HandlerClass = MyHandler
ServerClass  = HTTPServer

httpd = ServerClass (('0.0.0.0',9999), HandlerClass)
httpd.serve_forever()
