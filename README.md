# Parcel Delivery Demo
This is a demo built for the **Getting Stuff Done With Data** conference.

It shows how you can built data-driven applications using [Tinybird](tinybird.co).

You can find the [live deployment here](https://gsd-delivery-demo.vercel.app/) to play with the application.

# Creating a free Tinybird account
First sign up for a free Tinybird account at [tinybird.co](tinybird.co).

## Getting your Admin token
When logged into the Tinybird UI, go to 'Manage Auth Tokens' and copy your Admin token.

# Running the demo locally
There are three parts to this demo:
- a web application frontend
- python scripts to simulate activity
- Tinybird data projects

Start by cloning the repo.

## Web application
Install the dependencies

`npm install`

Run the dev server

`npm run dev -- --open`

This will open the application in your browser.

By default, some tokens are hardcoded into the application that let you interact with the demo environment, hosted in a Tinybird managed account.

If you want to connect the web application to your own Tinybird account, see the [Creating a free Tinybird account](#creating-a-free-tinybird-account) sections.

## Tinybird data projects
The Tinybird data project can be found in `tinybird/project`.

To use the Tinybird data project, see the [Creating a free Tinybird account](#creating-a-free-tinybird-account) sections, and [Getting your Admin token](#getting-your-admin-token).

Now change to the Tinybird dir.

`cd tinybird`

Create a Python virtual environment.

`python3 -m venv .venv`

Activate the Python virtual environment.

`source .venv/bin/activate`

Install the dependencies.

`pip install -r requirements.txt`

Now change to the Tinybird project dir.

`cd project`

Authenticate the tinybird-cli with your Admin token.

`tb auth`

Paste your Admin token into the prompt.

Push the Tinybird project to Tinybird.

`tb push`

You can now refresh the Tinybird UI and you project will be ready.

## Python scripts
Enter the event_processor directly.

`cd event_processor`

Create a Python virtual environment.

`python3 -m venv .venv`

Activate the Python virtual environment.

`source .venv/bin/activate`

Install the dependencies.

`pip install -r requirements.txt`

(Optional) Create a `.env` file and add your own Admin token.

The contents should look like

`TB_TOKEN=PASTE_YOUR_TOKEN_HERE`

In one shell session run:

`python journey_completer.py`

In another shell session run:

`python order_event_generator.py`

If you did not create a .env file, the scripts will prompt you to paste your Admin token before they start.