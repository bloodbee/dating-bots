from selenium.webdriver.common.keys import Keys

from time import sleep
import requests, os

from bots.base.BaseBot import BaseBot

class BadooBot(BaseBot):
  """
  Badoo Bot class
  """
  def __init__(self):
    """
    Initialization
    """
    super().__init__('badoo')
  
  def message_all(self):
    """
    Perform the message all action
    """
    base_window = self.driver.window_handles[0]

    # go to messages
    messages_tab = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="app_s"]/div/div/div/div[1]/div/div[3]/div/a[4]'))
    messages_tab.click()

    messages = [
      "Salut jolie demoiselle. Je suis désolé de t'annoncer ça, mais ce message est envoyé par un robot. Vois-tu, en tant que développeur, j'ai autre chose à faire que de passer mon temps à swiper et à envoyer des premiers messages qui restent le plus souvent sans réponses. Hé oui, nous les devs on est comme ça ^^ J'espère que tu ne le prend pas mal...",
      "Si t'es étonnée par mon talent, tu peux me répondre, et peut-être que nous pourrons continuer la conversation, entre humain cette fois-ci c'est promis ;). Bonne journée à toi !"
    ]

    matches_tab = self.wait.until(lambda d: d.find_elements_by_class_name('contacts__item'))[2:]
    i = 0
    while True:

      if i == len(matches_tab) + 1:
        break
      
      try:
        matches_tab[i].click()

        # send the messages
        msg_box = self.wait.until(lambda d: d.find_element_by_class_name('messenger-tools__input'))
        if msg_box is not None:
          sleep(1)
          for message in messages:
            msg_box = self.wait.until(lambda d: d.find_element_by_class_name('messenger-tools__input'))
            msg_box.send_keys(message)
            sleep(1)
            msg_box.send_keys(Keys.ENTER)
            sleep(1)
        else:
          print('Impossible send message')
      except Exception:
        try:
          self.close_popup()
        except Exception:
          pass

      i = i + 1
      sleep(0.5)
