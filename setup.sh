# This script uses pip (https://pypi.org/project/pip/) to install dependencies

# Google dependencies https://developers.google.com/sheets/api/quickstart/python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Browser automation software
pip install selenium

# Chromium Web Browser (Open source version of chrome browser)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get install chromium-browser
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install chromium
fi
