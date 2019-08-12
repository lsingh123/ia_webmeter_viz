# ia_webmeter_viz

webapp for visualizing ia-webmeter data

**not in production mode, still running on dev server**

## TODO

- improve error handling
- switch to production server
- operationalize

Once these steps have been completed, the app will be ready to run and new
features can be added.

## Using the app

The index page allows the user to select a collection and a date. 
## Requirements

Please set up a virtual environment with Python > 3.0. Install requirements:

`$ pip install -r requirements.txt`

For a guide to virtual environments: https://docs.python-guide.org/dev/virtualenvs/

## API Setup

Open port to cluster on app host and reload ferm:

```$ sudo echo 'saddr $CLUSTER proto tcp dport 5000 ACCEPT;' > /etc/ferm/input/5000 ```

```$ sudo systemctl reload ferm ```

## Web app

`$ python app.py `
