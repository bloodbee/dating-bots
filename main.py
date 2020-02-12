import sys
from tinder_bot import TinderBot

def main(argv):
  """
  Main function to manage commands and what to do.
  """
  if '-h' in sys.argv:
    print('main.py -l || main.py -m')
    print('-l will launch the bot and start the auto swipe')
    print('-m will launch the bot and message all matched persons')
    print('One bot at a time !')
    sys.exit()
  elif '-l' in sys.argv:
    print('Launch the bot in auto swipe mode...')
    bot = TinderBot()
    bot.login()
    bot.auto_swipe()
    bot.quit()
  elif '-m' in sys.argv:
    print('Launch the bot in message all matchs mode...')
    bot = TinderBot()
    bot.login()
    bot.message_all()
    bot.quit()
      

if __name__ == "__main__":
  main(sys.argv[1:])
  exit()