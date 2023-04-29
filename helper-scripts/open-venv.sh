#bash script for loading virtual environment and installing requirements
# Usage: source open-venv.sh

#activate virtual environment
source venv/bin/activate
#install requirements
pip install -r requirements.txt
#run the app
python app.py