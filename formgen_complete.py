from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import yaml
import argparse

# set form api scopes
SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# load credentials
store = file.Storage("token.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("client_secret_980008295896-itr48p4d1logvum8gs64svc628g1forr.apps.googleusercontent.com.json", SCOPES)
    creds = tools.run_flow(flow, store)

# setup service
form_service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# load yaml file
def load_structure(file_path):
    if file_path is None:
        print("Google OAUTH2.0 Authentication flow completed. Path was not provided. Example usage with path: python3 formgen_complete.py -p templategame.yaml")
        exit(0)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# create form
def create_form(service, form_structure):
    form = {
        "info": {
            "title": form_structure['form_title'],
            # "description": form_structure.get('description', '')
            
            #google oauth doesnt allow description to be added during form creation request? must be added using batch update
        }
    }
    # create the form
    result = service.forms().create(body=form).execute()
    form_id = result['formId']

    # add sections and questions sequentially in reverse order
    keys = [key for key in form_structure.keys() if key not in ['form_title', 'description']]
    keys.reverse()

    for key in keys:
        add_section(service, form_id, form_structure[key])

    return form_id

def add_section(service, form_id, section):
    requests = []
    
    # add section header
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
    
    # add textblock if it exists
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

    # add questions
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

    # execute the batch update
    batch_update_request = {
        "requests": requests
    }
    service.forms().batchUpdate(formId=form_id, body=batch_update_request).execute()

if __name__ == "__main__":
    # load the YAML structure
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", help = "Enter Path to the yaml file")

    args = parser.parse_args()

    # form_structure = load_structure('games/bardgame/bardgame.yaml')
    form_structure = load_structure(args.path)

    # generate the form and print ID
    form_id = create_form(form_service, form_structure)
    print(f"Form created with ID: {form_id}")
