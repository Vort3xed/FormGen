from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import yaml

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# Load credentials
store = file.Storage("token.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("client_secret_980008295896-itr48p4d1logvum8gs64svc628g1forr.apps.googleusercontent.com.json", SCOPES)
    creds = tools.run_flow(flow, store)

# Build the service
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
            # "description": form_structure.get('description', '')
        }
    }
    # Create the form
    result = service.forms().create(body=form).execute()
    form_id = result['formId']

    # Add sections and questions sequentially in reverse order
    keys = [key for key in form_structure.keys() if key not in ['form_title', 'description']]
    keys.reverse()

    for key in keys:
        add_section(service, form_id, form_structure[key])

    return form_id

def add_section(service, form_id, section):
    requests = []
    
    # Add section header
    requests.append({
        "createItem": {
            "item": {
                "title": section['title'],
                "description": section.get('description', ''),
                "pageBreakItem": {}
            },
            "location": {
                "index": 0
            }
        }
    })
    
    # Add textblock if it exists
    if 'textblock' in section:
        requests.append({
            "createItem": {
                "item": {
                    "title": section['textblock']['title'],
                    "description": section['textblock']['description'],
                    "textItem": {}
                },
                "location": {
                    "index": 1  # Ensure textblock appears after the section header
                }
            }
        })

    # Add questions
    index = 2  # Start after section header and textblock
    for question in section.get('questions', []):
        if question['type'] == 'multiple_choice':
            question_item = {
                "title": question['text'],
                "questionItem": {
                    "question": {
                        "required": False,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": option['text']} for option in question['options']],
                            "shuffle": False,
                        }
                    }
                }
            }
        elif question['type'] == 'short_answer':
            question_item = {
                "title": question['text'],
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            }
        else:
            continue
        
        requests.append({
            "createItem": {
                "item": question_item,
                "location": {
                    "index": index
                }
            }
        })
        index += 1

    # Execute the batch update
    batch_update_request = {
        "requests": requests
    }
    service.forms().batchUpdate(formId=form_id, body=batch_update_request).execute()

if __name__ == "__main__":
    # Load the YAML structure
    form_structure = load_structure('games/actualgame.yaml')

    # Create the form
    form_id = create_form(form_service, form_structure)
    print(f"Form created with ID: {form_id}")
