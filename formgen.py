from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import yaml

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("client_secret_980008295896-itr48p4d1logvum8gs64svc628g1forr.apps.googleusercontent.com.json", SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

def load_structure(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_form(service, form_structure):
    form = {
        "info": {
            "title": form_structure['form_title'],
        }
    }
    result = service.forms().create(body=form).execute()
    return result['formId']

