sudo apt-get install livestreamer -y
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install termcolor
pip install requests
pip install better_exceptions
sudo rm get-pip.py
echo "Installation completed!"
