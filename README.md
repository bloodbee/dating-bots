# Tinder Bot
A tinder bot that can do automatic swipes and can send automatic messages.


To install you need [pipenv](https://pipenv.readthedocs.io/en/latest/install/) and a [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/):

- Unzip chromedriver and move it to /usr/local/bin (mac os / linux)
- ``pipenv install``

Create a secrets.py file with variables:
```
 username = 'your_username'
 password = 'your_password'
```

Run the auto swipe mode:
```
pipenv run python main.py -l
```

Run the auto message all mode:
```
pipenv run python main.py -m
```
