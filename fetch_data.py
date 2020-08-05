import requests
import json

SERVER_URL = "covidbattlegec.knd.codes" # Change after actual Hosting
URL = "https://"+ SERVER_URL +"/api/" # Base url
"""
Hard Code the API_KEY of bot. After allocating in the database.
"""
API_KEY =  "k7MU6E0V1UyI3a13T477BMDQc" # Thrissur
## OR
# API_KEY =  "BYiqDUncnNkgmm6Zlw6KX7HUj" # Ernakulam



#Active beds
ACTIVE_BEDS_URL = URL + "active_beds/"
JSON_DATA = {"API_KEY": API_KEY}

response = requests.post(ACTIVE_BEDS_URL, json=JSON_DATA)
print(json.loads(response.text)) # Comment after use
ACTIVE_BED = json.loads(response.text)

# Patient Details
""" 
Bed Id. Temorarily setting as first bed id from the active bed list. 
Change as required later (Programatically)
"""
BED_ID = ACTIVE_BED["beds"][0] 

PATIENT_DETAILS_URL = URL + "patient_details/"
JSON_DATA = {"API_KEY": API_KEY, "bed_name": BED_ID}
response = requests.post(PATIENT_DETAILS_URL, json=JSON_DATA)
print(json.loads(response.text)) # Comment After use
PATIENT_DETILS = json.loads(response.text)