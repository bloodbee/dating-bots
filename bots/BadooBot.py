from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from time import sleep
import random
import requests, os

from secrets import username, password

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def download_image(source, destination):
  img_data = requests.get(source).content
  with open(destination, 'wb') as out:
      out.write(img_data)

class BadooBot(object):
  """
  Badoo Bot class
  """
  def __init__(self):
    """
    Initialization
    """
    self.driver = webdriver.Chrome()
    self.wait = WebDriverWait(self.driver, 10)

  def setModel(model):
    self.model = model

  def login(self):
    """
    Perform login with facebook action
    """
    self.driver.get('https://badoo.com/fr/')

    fb_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="page"]/div[2]/div[3]/div/div[3]/div/div[1]/div[2]/div/div/a'))
    fb_btn.click()

    # switch to login popup
    base_window = self.driver.window_handles[0]
    self.driver.switch_to.window(self.driver.window_handles[1])

    if (self.driver.find_element_by_xpath('//*[@id="email"]') and self.driver.find_element_by_xpath('//*[@id="pass"]')):
      email_in = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="email"]'))
      email_in.send_keys(username)

      pw_in = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="pass"]'))
      pw_in.send_keys(password)

      login_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="u_0_0"]'))
      login_btn.click()
    else:
      login_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="u_0_4"]/div[2]/div[1]/div[1]/button'))
      login_btn.click()

    self.driver.switch_to.window(base_window)

    # # validate location
    # popup_1 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
    # popup_1.click()

    # # validate incoming notification from tinder
    # popup_2 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
    # popup_2.click()

  def like(self):
    """
    Perform like action
    """
    like_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[1]/div[1]'))
    like_btn.click()

  def dislike(self):
    """
    Perform dislike action
    """
    dislike_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[2]/div[1]'))
    dislike_btn.click()

  def auto_swipe(self):
    """
    Perform the auto swipe action
    """
    while True:
      sleep(0.5)
      try:
        if random.randrange(0, 100) < random.randrange(70, 80):
          self.like()
        else:
          self.dislike()
      except Exception:
        try:
          self.close_popup()
        except Exception:
          try:
            self.close_match()
          except Exception:
            try:
              if self.out_of_likes():
                print("Out of likes.")
                break
            except Exception:
              print('Unknow error.')
              break
  
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

  def close_popup(self):
    """
    Close annoying popup
    """
    popup_3 = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[2]/div/div[2]')
    if popup_3:
      popup_3.click()

  def close_match(self):
    """
    Close match popup
    """
    match_popup = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[1]/div[4]')
    if match_popup:
      match_popup.click()
  
  def close_payment(self):
    """
    Close payment popup
    """
    payment_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]')
    if payment_popup:
      payment_popup.click()
  
  def out_of_likes(self):
    """
    Close out of likes popup
    """
    likes_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]')
    if likes_popup:
      likes_popup.click()
      return 1

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

  def current_scores(self):
    url = self.get_image_path()
    outPath = os.path.join(APP_ROOT, 'images', os.path.basename(url))
    download_image(url, outPath)
    return self.model.scores(outPath)
  
  def quit(self):
    """
    Perform quit action - Just quit the used driver
    """
    print('End of bot. Have fun ! ;)')
    self.driver.quit()