import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"

orig = "Lima"
dest = "Arequipa"

key = "GTgkkPVaSC9GfGgjVuAMTGLcDXlGGSzW"

url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

json_data = requests.get(url).json()
json_streets = json_data['route']
print(str(json_streets))

