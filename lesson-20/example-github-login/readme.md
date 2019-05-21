#### Dependencies

	Flask==1.0.2
    gunicorn==19.9.0
    requests_oauthlib

As you can see, you'll need to add a new library called `requests_oauthlib`. This library will help you connect to 
GitHub to get login authorization.

#### Deployment

You will need to use your GitHub ID and a GitHub secret key in your app. You must not add this ID and key directly in 
your app, because when you'll push your code to GitHub (or some other Git provider), everyone will be able to see your 
code and the secret key inside. As the name implies, secret key must be kept secret!

So instead you'll put your secret key in an **environment variable** (or "env var" for short). Currently, of the PaaS 
hosting services that we use, only Heroku and Azure support adding env vars. Google App Engine unfortunately doesn't 
(you can store env vars in Datastore or Firestore instead, but let's keep it simple). So don't use GAE for this example. 
Use either Heroku.

#### Create a .gitignore file and a secrets.py file

First create a `.gitignore` file and add this content in:

	*.pyc
	db.json
	secrets.py

Then create a `secrets.py` file with the following contents:

	# this file MUST be in .gitignore
	# do not upload it to GitHub!
	# if you upload it to GitHub, someone can steal your GitHub ID and secret!
	import os
	
	os.environ["GITHUB_CLIENT_ID"] = ""
	os.environ["GITHUB_CLIENT_SECRET"] = ""
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

You will get the GitHub Client ID and Client Secret in the next step.

#### Get your GitHub ID and secret

Go to your GitHub account, find **Settings**, click on **Developer settings** and then on **New OAuth App**.

Or just click on this link: [https://github.com/settings/applications/new](https://github.com/settings/applications/new)

Fill out the form:

<img width="300px" src="https://storage.googleapis.com/smartninja/github-register-oauth-app-1548635618.png">

For the URLs add these temporary links for now:

- **Homepage URL:** `http://127.0.0.1:5000/`
- **Callback URL:** `http://127.0.0.1:5000/github/callback`

But when you'll deploy your app on, for example, Heroku, you'll need to replace `http://127.0.0.1:5000` with the Heroku 
app URL (`https://your-app-id.herokuapp.com`).

Click on **Register application** and you will see your **Client ID** and **Client Secret**.

#### Add ID and Secret into env vars

Copy the client ID and secret and add it into your `secrets.py` file. This will help you use env vars on localhost.

Also create the env vars on Heroku. On Heroku you can find env vars under **Settings/Config Vars**.
