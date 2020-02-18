import sys
from bots.TinderBot import TinderBot as TinderBot
from bots.BadooBot import BadooBot as BadooBot

def main(argv):
  """
  Main function to manage commands and what to do.
  """
  if '-h' in sys.argv:
    print('main.py -tl || main.py -tm  || main.py -bl || main.py -bm')
    print('-tl will launch the tinder bot and start the auto swipe')
    print('-tm will launch the tinder bot and message all matched persons')
    print('-bl will launch the badoo bot and start the auto swipe')
    print('-bm will launch the badoo bot and message all matched persons')
    print('One bot at a time !')
    sys.exit()
  elif '-tl' in sys.argv:
    print('Launch the tinder bot in auto swipe mode...')
    bot = TinderBot()
    bot.login()
    bot.auto_swipe()
    bot.quit()
  elif '-tm' in sys.argv:
    print('Launch the tinder bot in message all matchs mode...')
    bot = TinderBot()
    bot.login()
    bot.message_all()
    bot.quit()
  elif '-bl' in sys.argv:
    print('Launch the badoo bot in auto swipe mode...')
    bot = BadooBot()
    bot.login()
    bot.auto_swipe()
    bot.quit()
  elif '-bm' in sys.argv:
    print('Launch the badoo bot in message all matchs mode...')
    bot = BadooBot()
    bot.login()
    bot.message_all()
    bot.quit()
      

if __name__ == "__main__":
  main(sys.argv[1:])
  exit()