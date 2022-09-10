# Parcel Delivery Demo
This is a demo built for the **Getting Stuff Done With Data** conference.

It shows how you can built data-driven applications using [Tinybird](tinybird.co).

You can find the [live deployment here](https://gsd-delivery-demo.vercel.app/) to play with the application.

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

In the current version, API tokens are hardcoded to the live demo. If you want to run this on your own data project, you'll need to replace the token. This will be improved in later versions.

## Python scripts
Enter the event_processor directly.

`cd event_processor`

Create a Python virtual environment.

`python3 -m venv .venv`

Install the dependencies.

`pip install -r requirements.txt`

In one shell session run:

`python journey_completer.py`

In another shell session run:

`python order_event_generator.py`

## Tinybird data projects
TBD

