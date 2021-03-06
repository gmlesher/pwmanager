from cryptography.fernet import Fernet
import os
import json
from dotenv import load_dotenv
load_dotenv()

# key used for encryption, stored in .env 
key = os.getenv('ENC_KEY').encode('utf-8')

def load_and_dump(acct, password):
    """loads and writes .json files. Account name and encrypted passwords
    are stored in 'pw_data.json' file"""
    try:
        with open('pw_data.json', 'r') as current_json: 
            old_data = json.load(current_json)
    except (FileNotFoundError, ValueError) as exc:
        print(f'***File not found or no data in file***')
        print(exc)
        print("Creating and/or adding data to file...")
        data = {}
        data['accounts'] = []
        data['accounts'].append({
            'app': {
                'name': f'{acct}',
                'password': f'{password}',
            },  
        })
        with open('pw_data.json', 'w') as f: 
            json.dump(data, f, indent=4)
    else:
        data = old_data
        # if account name is already in json file, update the password with new 
        # password, to be written in new json file
        for app in data['accounts']:
            if app['app']['name'] == acct:
                app['app']['password'] = password
                break
        # if account name is not already present, write new account and password 
        # to end of file
        else:
            data['accounts'].append({
                'app': {
                    'name': f'{acct}',
                    'password': f'{password}',
                },  
            })
        with open('pw_data.json', 'w') as f: 
            json.dump(data, f, indent=4)


def encrypt(password):
    """Encrypts plain text password entered from user in 'create new passsword'
    option in application menu"""
    password = password.encode('utf-8')
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(password)
    plaintext_ciphered = ciphered_text.decode('utf-8')
    return plaintext_ciphered


def decrypt(encrypted_password):
    """Decrypts encrypted password stored in .json file. This function is executed 
    after 'retrieve_encrypted_pw' funciton below"""
    encrypted_password = encrypted_password.encode('utf-8')
    cipher_suite = Fernet(key)
    unciphered_text = cipher_suite.decrypt(encrypted_password)
    plaintext_unciphered = unciphered_text.decode('utf-8')
    return plaintext_unciphered


def retrieve_encrypted_pw(app_name):
    """opens .json file and retrieves encrypted password based on the app name 
    given in option #2 of the menu"""
    with open('pw_data.json', 'r') as current_json: 
            data = json.load(current_json)

    for app in data['accounts']:
        if app['app']['name'] == app_name:
            return app['app']['password']
    
    print(f'No app named "{app_name}" in .json file')
    return 


def delete_app(app_name):
    """opens .json file and deletes app if app_name exists in file"""
    with open('pw_data.json', 'r') as current_json: 
            data = json.load(current_json)

    # iterates through .json file to find "app_name", pops it out of json file
    for i in range(len(data['accounts'])):
        if data['accounts'][i]['app']['name'] == app_name:
                data['accounts'].pop(i)
                break
    
    with open('pw_data.json', 'w') as f: 
            json.dump(data, f, indent=4)