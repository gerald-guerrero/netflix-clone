# Netflix Clone
This repository serves as a simplified clone of Netflix. Its purpose is to have the backend function like Netflix's backend while the frontend remains minimalistic.

# Deployment Instructions
You will need to use python3 to preceed with the instructions  

1. Clone the repository and navigate to its location in your file directory
2. Generate a SECRET_KEY variable and save it to a .env file with the format: SECRET_KEY="secret key here". You can do this with the command below or another method of your choosing  
   Mac, Linux, WSL on Windows: `echo "SECRET_KEY=\"$(python3 -c 'import secrets; print(secrets.token_hex(24))')\"" >> .env`  
   Windows Powershell: `echo "SECRET_KEY=""$(python3 -c 'import secrets; print(secrets.token_hex(24))')""" >> .env`  
   Open the .env to ensure the key was generated in the proper format  
3. Create a virtual environment using the command:  
   `python3 -m venv venv`  
4. Activate the virtual environment with the command:  
   Mac, Linux, WSL on Windows: `source venv/bin/activate`  
   Windows powershell: `venv\Scripts\activate`  
5. While the virtual envrionment is activated, install the requirements in requirements.txt with the command  
   `pip3 install -r requirements.txt`  
6. Run the app with the command  
   `python3 app.py`  

You can deactivate the virtual environment by entering `deactivate` in the terminal  
Alternatively, You can skip steps 3 and 4 if you choose to install the dependencies and run the app globally
