import requests
from requests.auth import HTTPBasicAuth

url = "https://jira-jdc-t2.devtools.intel.com/rest/api/2/issue/PTS-53706"
auth = HTTPBasicAuth('username', 'password')

response = requests.get(url, auth=auth)
issue_data = response.json()

# Wyświetl wszystkie custom fields
for field_id, field_value in issue_data['fields'].items():
    if field_id.startswith('customfield_'):
        print(f"{field_id}: {field_value}")