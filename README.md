# Weather App Backend

Backend weather app server using Flask.

## Run Locally

Clone this repo.

```shell
git clone https://github.com/jvaverka/weather-app-server-py.git
```

Change to the project directory.

```shell
cd weather-app-server-py
```

Setup a virtual environment.

```shell
python3 -m venv .venv
```

Activate the virtual environment

```shell
source .venv/bin/activate
```

Install dependencies.

```shell
python3 -m pip install -r requirements.txt
```

Set environment variables

```shell
export FLASK_ENV=development
export FLASK_APP=app/run.py
export NATIONAL_WEATHER_SERVICE_ROOT_URL="https://api.weather.gov/"
export CLIENT_ROOT_URL="http://localhost:3000/*"
```

Start the server.

```shell
flask run --reload
```
