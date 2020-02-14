# Meeting Apps Bots
A tinder and a badoo bot that can do automatic swipes and can send automatic messages.


To install you need [pipenv](https://pipenv.readthedocs.io/en/latest/install/) and a [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/):

- Unzip chromedriver and move it to /usr/local/bin (mac os / linux)
- ``pipenv install``

Create a secrets.py file with variables:
```
 username = 'your_username'
 password = 'your_password'
```

Run the auto swipe mode for tinder bot:
```
pipenv run python main.py -tl
```
Run the auto swipe mode for badoo bot:
```
pipenv run python main.py -bl
```

Run the auto message all mode for tinder bot:
```
pipenv run python main.py -tm
```
Run the auto message all mode for badoo bot:
```
pipenv run python main.py -bm
```


Source : 
Bot inspired by [Aaron](https://github.com/aj-4/tinder-swipe-bot) and a lot of code taken from his repo, thanks to him!
