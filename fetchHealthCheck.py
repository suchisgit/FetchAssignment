import requests
import yaml
import time
import signal
import sys

class HealthChecker:
    def __init__(self, config_file):
        self.endpointDetails = []
        self.endpointStatus = {}
        self.load_configuration(config_file)

    def load_configuration(self, config_file):
        try:
            with open(config_file, 'r') as file:
                self.endpointDetails = yaml.safe_load(file)
                for endpointDetails in self.endpointDetails:
                    self.endpointStatus[endpointDetails['url']] = {'up': 0, 'total': 0}
        except FileNotFoundError:
            print(f"Configuration file '{config_file}' not found.")
            sys.exit(1)

    def check_health(self):
        cycle = 0
        while True:
            cycle += 1
            cycleLatency = 0
            for endpointDetails in self.endpointDetails:
                url = endpointDetails['url']
                method = endpointDetails.get('method', 'GET')
                headers = endpointDetails.get('headers', {})
                body = endpointDetails.get('body', None)
                try:
                    start_time = time.time()
                    response = requests.request(method, url, headers=headers, data=body,timeout=0.5)
                    latency = int((time.time() - start_time) * 1000)
                    cycleLatency += latency
                    if response.status_code >= 200 and response.status_code < 300 and latency < 500:
                        outcome = 'UP'
                        self.endpointStatus[url]['up'] += 1
                    else:
                        outcome = 'DOWN'
                    self.endpointStatus[url]['total'] += 1
                    # print(f"Endpoint '{endpointDetails['name']}' is {outcome} ({response.status_code}, {latency} ms)")
                except requests.RequestException as e:
                    print(f"Failed to connect to '{endpointDetails['name']}': {e}")
                    self.endpointStatus[url]['total'] += 1
            print(f"Test Cycle #{cycle}")
            self.log_endpointStatus()
            wait_time = max(0, 15 - cycleLatency / 1000)
            time.sleep(wait_time)

    def log_endpointStatus(self):
        for url, stats in self.endpointStatus.items():
            if stats['total'] > 0:
                endpointStatus_percentage = (stats['up'] / stats['total']) * 100
                print(f"{url} has {round(endpointStatus_percentage)}% availability percentage")

    def run(self):
        try:
            self.check_health()
        except KeyboardInterrupt:
            print("\nCTRL+C detected. Exiting gracefully.")
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please rerun the command should be: python fetchHealthCheck.py <config_file.yaml>")
        sys.exit(1)
    print("Running Health Check on the given configuration YAML file endpoints...press CTRL + C to exit.")
    config_file = sys.argv[1]
    checker = HealthChecker(config_file)
    checker.run()
