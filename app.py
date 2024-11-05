import json
import requests
import time
import os

class ServerAvailabilityChecker:
    def __init__(self,
                 ntfy_url: str,
                 server_list_file: str = './servers.json',
                 poll_interval: int = 60):
        """
        Initialize the availability checker with a server list file, ntfy instance URL, and poll interval
        """

        self.server_list_file = server_list_file
        self.ntfy_url = ntfy_url
        self.ntfy_headers = { "Title": "Server Availability Alert" }
        self.poll_interval = poll_interval
        self.alerted_servers = {}

    def load_server_list(self):
        """
        Load sever list from a jSON file containing server names and URLs.
        Example JSON format:
        [
            {
                "name": "server1",
                "url": "http://example.com/server1/status"
            },
            {
                "name": "server2",
                "url": "http://example.com/server2/status"
            }
        ]
        """

        with open(self.server_list_file) as file:
            self.server_list = json.load(file)

    def fetch_availability(self, url: str) -> dict | None:
        """
        Fetch the server availability data from the given URL.
        Expects JSON response with following format:
        [
            {
                "fqn": "server1.ram-xxx.storage-xxx",
                "memory": "ram-xxx",
                "planCode": "server1",
                "storage": "storage-xxx",
                "datacenters": [
                    {
                        "availability": "unavailable",
                        "datacenter": "dc1"
                    },
                    {
                        "availability": "1H-low",
                        "datacenter": "dc2"
                    },
                    {
                        "availability": "1H-high",
                        "datacenter": "dc3"
                    }
                ]
            }
        ]
        """

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch data from {url}: {e}")
            return None

    def check_and_alert(self):
        """
        Checks server availability and sends alert if the server bceomes newly available in any datacenter.
        """
        for server in self.server_list:
            name = server["name"]
            url = server["url"]
            availability_data = self.fetch_availability(url)

            if availability_data:
                for datacenter in availability_data[0]["datacenters"]:
                    dc_name = datacenter["datacenter"]
                    is_available = datacenter["availability"]

                    if is_available != "unavailable" and not self.alerted_servers.get((name, dc_name), False):
                        self.send_alert(name, dc_name, is_available)
                        self.alerted_servers[(name, dc_name)] = True
                    elif is_available == "unavailable":
                        self.alerted_servers[(name, dc_name)] = False

    def send_alert(self, server_name: str, datacenter_name: str, availability_type: str):
        """
        Sens an alert to the ntfy instance with the server and datacenter availability information.
        """

        alert_message = f"Server {server_name} is now available ({availability_type}) in datacenter {datacenter_name}"
        try:
            response = requests.post(self.ntfy_url, headers=self.ntfy_headers, data=alert_message.encode('utf-8'))
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send alert: {e}")

    def run(self):
        """
        Main method to run periodic checks.
        """

        self.load_server_list()
        try:
            while True:
                self.check_and_alert()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print("Exiting...")


if __name__ == "__main__":
    server_list_file = "./servers.json"
    ntfy_url = os.getenv("NTFY_URL")
    poll_interval = int(os.getenv("POLL_INTERVAL"))

    if not ntfy_url:
        raise ValueError("NTFY_URL environment variable is required")

    checker = ServerAvailabilityChecker(ntfy_url, server_list_file, poll_interval)
    checker.run()

