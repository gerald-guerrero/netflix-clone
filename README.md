# Netflix Clone
This repository serves as a simplified clone of Netflix. Its purpose is to have the backend function like Netflix's backend while the frontend remains minimalistic.

# Deployment Instructions

1. Clone the repository and navigate to its location in your file directory
2. Generate a SECRET_KEY variable and save it to a .env file with the format: SECRET_KEY="secret key here". You can do this with the command below or another method of your choosing
   for Mac and linux (WSL on windows systems): `echo "SECRET_KEY=\"$(python3 -c 'import secrets; print(secrets.token_hex(24))')\"" >> .env`
   for windows powershell: `echo "SECRET_KEY=""$(python3 -c 'import secrets; print(secrets.token_hex(24))')""" >> .env`
   Open the .env to ensure the key was generated in the proper format
2. Install virtual environment with the command
   `pip3 install virtualenv` or `pip install virtualenv`
3. While in the repository directory, create the virtual environment with the command
    `virtualenv env`
4. Activate the virtual environment with the command
   `source env/bin/activate`
5. While the virtual envrionment is activated, install the requirements in requirements.txt with the command
   `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
6. Run the app with the command
   `python app.py`

Alternatively, after cloning the repository, you can install the requirements globally if you choose to run it outside the virtual environment with the same command
`pip3 install -r requirements.txt` or `pip install -r requirements.txt`