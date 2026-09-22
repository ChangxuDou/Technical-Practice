# on the terminal

# use command "pip3 install requests"

# command "pip3 install --upgrade pip" to upgrade
# command "pip3 list" to look at the package version that installed in our machine

# command"pip3 install requests==2.9.0"to install the old version like:2.9.0

# command"pip3 install requests==2.9.*" to install the latest compatible version
# or "pip3 install requests~=2.9.0""

# command"pip3 uninstall requests" to uninstall the package

import requests

# can read the detail about request on website: pypi.org
response = requests.get("http://google.com")
print(response)

