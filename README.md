# geigershow
Connect to a local GQ GMC Geiger counter and display in Grafana

## Packages

- requests
- flask


Manually get data:

```python
import requests
connection = requests.get("http://localhost:80/gstat")
print(connection.text)
```