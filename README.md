<img src="images/box-dev-logo-clip.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>

# The Diver Portal - A UI Elements Sample App
This is the companion app to illustrate [this medium article](https://medium.com/box-developer-blog/dive-into-the-box-platform-94ced33c2c86). This is a custom portal using Flask and Python to create an example Diver Portal. It uses Box Sign, Box Tasks, and other Box Platform features. Check it out.

These instructions show using a Box JWT application and service account. You may also use OAuth 2.0 or Client Credentials, but the setup steps will differ.

## Box configuration steps

 It is recommended that you setup this tutorial up in a Sandbox environment, as you will need admin privileges. Find more about sandboxes [here](https://support.box.com/hc/en-us/articles/360043697274-Managing-developer-sandboxes-for-Box-admins).

1. In the Box Admin Console, [confirm Box Sign](https://support.box.com/hc/en-us/articles/4404076971155-Configuring-Box-Sign-Enablement-Settings) is enabled for your enterprise.
2. In the Box Sign section of the main Box Web App, [setup a Box Sign Template](https://support.box.com/hc/en-us/articles/4404094944915-Creating-using-and-sharing-templates) using this [waiver example](https://cloud.box.com/s/kzoulzp51qjektsetshbqo9aw67alp3v).
3. Create a new application in the [Box Developer Console](https://app.box.com/developers/console). Click Create new app > Custom App > Server Authentication(with JWT) > Click Create App.
4. Under the configuration tab, select App + Enterprise, followed by checking the boxes for Read/Write all files and manage sign requests. Then, click Save Changes in the top right.
5. Towards the bottom, generate a new public/private keypair. This will automatically start a download of the JWT config file you will use later. 
6. Copy the client id of the application. Back in the Box Admin Console, follow the steps to [approve a custom application](https://developer.box.com/guides/authorization/custom-app-approval/).
7. Back on the General Settings tab of the application you created in the Box Developer Console, you should now see an email that starts like AutomationUser_... in the Service Account Info section. Copy that email. Back in the main Box Web App, collaborate the service account into the sign template you created in step 2. Templates are stored under the All Files page folder called My Sign Requests by default. You should see a pdf version of the word file, and when you open it, also make note of the the file id for later.

## Installation and configuration

You will need to have [python](https://www.python.org/downloads/) installed on your machine. 

> Get the code
```bash
git clone git@github.com:barduinor/ui-elements-sample-app.git
cd ui-elements-sample-app
```

> Set up your virtual environment
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Create your local application environment file
```bash
cp .env.sample .env
```

> Open the code in the code editor of your choice. For example, if you have the appropriate extension installed for VS Code, you can use the below to open the repository. 
```
code .
```

> Generate a secret key for your app
```bash
python -c "import os; print(os.urandom(24).hex())"
```
> Copy and paste the value in the secret key field in the env file. 

> Generate a fernet (encryption) key for your app
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
```
> Copy and paste the value in the fernet key field in the env file. You only the need the value within the single quotes.

> Drag in the config.json file downloaded after creating your application in an earlier step. Rename it `.config.json`.

> Update the TASK_USER_LOGIN field value in the env file with the Box login you wish to assign tasks to. You will want this to be an account that can login to the main Box Web App. 

> Update the DEMO_FOLDER_NAME field value in the env file to be the name you wish the bookings to be created under. You can leave the default if you wish. This folder will get created the first time you create a booking or use a UI element.

> Update the SIGN_TEMPLATE_ID field value in the env file to be the file id of the sign template you created earlier. You can find the file id by opening the file from the sign request folder and copying the id from the url bar.

## Run the application 

> Run your server
```bash
flask run
```

> Point your browser to the server (e.g http://127.0.0.1:5000).
> Initialize the application by navigating to the /bootstrap route (e.g. http://127.0.0.1:5000/bootstrap). 

Sign up for an account, and then, login using those credntials. Visit the UI Element explorer or content picker to view/create the bookings folder.

In the Box Admin Console, go to the content tab and find the Bookings folder under the application's service account. Collaborate the sign admin's email into the bookings folder. This will allow that user to see the tasks assigned.

Try creating a booking. You should see a waiver automatically get created based on the template id and a Box Sign request emailed to the Diver Portal email you created.

You can sign the waiver and upload a insurance card and drivers license. 

If you login to the sign admin's Box account, you should see tasks appear in the upper right corner. 

## Webhooks

This repo is also used for [another part](https://medium.com/box-developer-blog/hooked-on-the-box-platform-9264a0efb0a) of the blog series on webhooks. 

Back to your developer console and application, flip to the webhooks tab, and create a webhook for the bookings folder. 

Select the following triggers:
* TASK_ASSIGNMENT.UPDATED
* SIGN_REQUEST.COMPLETED
* SIGN_REQUEST.DECLINED
* SIGN_REQUEST.EXPIRED

### Questions
If you get stuck or have questions, make sure to ask on our [Box Developer Forum](https://support.box.com/hc/en-us/community/topics/360001932973-Platform-and-Developer-Forum)
