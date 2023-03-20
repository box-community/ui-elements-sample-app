<img src="images/box-dev-logo-clip.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>

# UI Elements Sample App
> This is the companion app to illustrate [this medium article](https://medium.com/box-developer-blog/dive-into-the-box-platform-94ced33c2c86). Check it out.

## Installation

> Get the code
```bash
git clone git@github.com:barduinor/ui-elements-sample-app.git
cd ui-elements-sample-app
```

> Set up your virtual environment
```bash
python3.10 -m venv venv
source ./venv.bin/activate
pip install -r requirements.txt
```

> Create your application environment
```bash
cp .env.example .env
```

> Generate a secret key for your app
```bash
python -c "import os; print(os.urandom(24).hex())"
```

> Generate a fernet (encryption) key for your app
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key()"
```

> Edit your .env file and fill in the information
```
# True for development, False for production
DEBUG=True

# Flask ENV
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY='YOUR_SECRET_KEY'
FERNET_KEY='YOU_ENCRYPTION_KEY'

# Box JWT
JWT_EXPIRATION_SECONDS = 3300

#Sample App Configuration
DEMO_FOLDER_NAME='Bookings'
SIGN_TEMPLATE_ID = 'YOUR DOCUMENT SIGN TEMPLATE ID'
```

> JWT Configuration usgin the config.json file
> Edit/copy your config.json to .config.json.
> (get the file from you development console when you configure the application)
```
{
    "boxAppSettings": {
      "clientID": "YOUR_CLIENT_ID",
      "clientSecret": "YOUR_CLIENT_SECRET",
      "appAuth": {
        "publicKeyID": "YOUR_PUBLIC_KEY_ID",
        "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY-----\n-----END ENCRYPTED PRIVATE KEY-----\n",
        "passphrase": "YOUR_PASSPHRASE"
      }
    },
    "enterpriseID": "YOUR_ENTERPRISE_ID",
  }
```

> Run your server
```bash
flask run
```

> Point your browser to the server (e.g http://127.0.0.1:5000).