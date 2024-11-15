# Introduction

This project is a docker container that checks the availability of Kimsufi OVH servers and sends a notification to a ntfy server when a server becomes available.

# How to use

1. Create a docker compose file with the following content:
```yaml
services:
  app:
    image: ghcr.io/isnubi/ovh-ks-availability-alerter:latest
    volumes:
      - ./servers.json:/app/servers.json
    environment:
      - NTFY_URL=https://ntfy.example.com/alerting
      - POLL_INTERVAL=60
    restart: unless-stopped
```
2. Run the following command:
```bash
docker compose up -d
```

# Configuration

## Environment variables

- `NTFY_URL`: The URL of the ntfy server to send notifications to.
- `POLL_INTERVAL`: The interval in seconds to check the availability of the servers.

## OVH API

You can use this [API page](https://eu.api.ovh.com/console/?section=%2Fdedicated%2Fserver&branch=v1#get-/dedicated/server/datacenter/availabilities) to find the url for the servers you want to check.

Here is a tab for OVH datacenters:
```
EUROPE
rbx: Roubaix, France
sbg: Strasbourg, France
gra: Gravelines, France
par: Paris, France
lon: London, UK
fra: Frankfurt, Germany
waw: Warsaw, Poland

NORTH AMERICA
bhs: Beauharnois, Canada

ASIA
syd: Sydney, Australia
sgp: Singapore
```

## `servers.json`

Edit the `servers.json` file to include the servers you want to check. The format is:
```json
[
    {
	"name": "Server Name",
	"url": "https://eu.api.ovh.com/1.0/dedicated/server/datacenter/availabilities?country=FR&datacenter=gra"
    }
]
```

# Example
There is an example `servers.json` file included in the repository. It checks the availability for a **KS-A** server in the **gra**, **rbx** and **sbg** datacenters. 

# License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

