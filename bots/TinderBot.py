from time import sleep
import random
import requests, os

from bots.base.Bot import Bot

class TinderBot(Bot):
  """
  Tinder Bot class
  """
  def __init__(self):
    """
    Initialization
    """
    super().__init__('tinder')
  
  def message_all(self):
    """
    Perform the message all action
    """
    base_window = self.driver.window_handles[0]

    messages = [
      "Salut jolie demoiselle.",
      "Je suis désolé de t'annoncer ça, mais ce message est envoyé par un robot.",
      "Vois-tu, en tant que développeur, j'ai autre chose à faire que de passer mon temps à swiper et à envoyer des premiers messages qui restent le plus souvent sans réponses.",
      "Hé oui, nous les devs on est comme ça ^^",
      "J'espère que tu ne le prend pas mal...",
      "Si t'es étonnée par mon talent, tu peux me répondre, et peut-être que nous pourrons continuer la conversation, entre humain cette fois-ci c'est promis ;).",
      "Bonne journée à toi !"
    ]

    matches_tab = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="match-tab"]'))
    
    while True:
      # we wait that the matches are fully loaded
      matches = self.wait.until(lambda d: d.find_elements_by_class_name('matchListItem'))[1:]
        
      if len(matches) < 1:
        break

      matches[0].click()

      # send the messages
      send_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button'))
      msg_box = self.wait.until(lambda d: d.find_element_by_class_name('sendMessageForm__input'))
      for message in messages:
        msg_box.send_keys(message)
        send_btn.click()
        sleep(0.2)
        
      # return to matches tab
      matches_tab.click()

      sleep(0.5)

  def get_image_path(self):
    body = self.driver.find_element_by_xpath('//*[@id="Tinder"]/body')
    bodyHTML = body.get_attribute('innerHTML')
    startMarker = '<div class="Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox" style="background-image: url(&quot;'
    endMarker = '&'

    if not self.begining:
      urlStart = bodyHTML.rfind(startMarker)
      urlStart = bodyHTML[:urlStart].rfind(startMarker)+len(startMarker)
    else:
      urlStart = bodyHTML.rfind(startMarker)+len(startMarker)

    self.begining = False
    urlEnd = bodyHTML.find(endMarker, urlStart)
    return bodyHTML[urlStart:urlEnd]


