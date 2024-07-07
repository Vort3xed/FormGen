from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("client_secret_980008295896-itr48p4d1logvum8gs64svc628g1forr.apps.googleusercontent.com.json", SCOPES)
  creds = tools.run_flow(flow, store)
service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# Prints the title of the sample form:
form_id = "1d-8IwU8awlQ05yU_6bTBivhSO4CSZh5eoB0ejByVew8"
result = service.forms().get(formId=form_id).execute()
print(result)