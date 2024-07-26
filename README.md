# FormGen

Dynamically generate google forms using a simple YAML file. 

Operational: `formgen_complete.py`

Capabilities:
- Add text blocks
- Multiple choice questions
- Free response questions
- Free response questions
- Section descriptions

Limited by the functionality of Google Forms API.

## Installation Steps (Windows):

1. Install Python 3.10 on your local device. Any version of Python 3.10+ should work. Installation steps found here: https://phoenixnap.com/kb/how-to-install-python-3-windows

2. Ensure Python 3 was properly installed on your device by running the following command in your terminal: `python3 --version`

3. (Optional) Install Git on your local device. Installation steps found here: https://git-scm.com/download/win

4. Clone the repository to your local device by running the following command in your terminal: `git clone https://github.com/Vort3xed/FormGen.git` If git is not installed, download the repository as a zip file and extract it to your desired location.

5. Navigate to the FormGen directory by running the following command in your terminal: `cd FormGen`

6. Install this required Python package: `pip3 install api-client`

7. Install the required Python packages by running the following command in your terminal: `pip3 install -r requirements.txt`

8. Place your Google API credentials in your working directory.

9. Run the program by running the following command in your terminal. `python3 formgen_complete.py` Your browser should open and you should be prompted to log in to your Google account.

10. Run the program again with a specified path to the yaml file. `python3 formgen_complete.py -p templategame.yaml`
