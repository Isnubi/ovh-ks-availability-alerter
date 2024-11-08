This project is a docker container that checks the availability of Kimsufi OVH servers and sends a notification to a ntfy server when a server becomes available.

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

# Usage
Edit the `servers.json` file to include the servers you want to check. The format is:
```json
[
    {
	"name": "Server Name",
	"url": "https://eu.api.ovh.com/1.0/dedicated/server/datacenter/availabilities?country=FR&datacenter=gra"
    }
]
```

Then set the ntfy.sh URL in the `compose.yml` file:
```yaml
    environment:
      - NTFY_URL=https://ntfy.example.com/alerting
```

Then run the following command:
```bash
docker compose up -d
```

# Example
There is an example `servers.json` file included in the repository. It checks the availability for a **KS-A** server in the **gra**, **rbx** and **sbg** datacenters. 
