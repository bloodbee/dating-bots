from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
import random
import requests, os

from secrets import username, password

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def download_image(source, destination):
  img_data = requests.get(source).content
  with open(destination, 'wb') as out:
      out.write(img_data)

class Bot(object):
  """
  Abstract class Bot
  """
  def __init__(self, name):
    """
    Initialization
    """
    self.driver = webdriver.Chrome()
    self.wait = WebDriverWait(self.driver, 10)

    self.name = name

    # for secrets
    self.username = username
    self.password = password

    # for NN
    self.model = None

    # for xpath variables
    if self.name == 'tinder':
      self.website_path = 'https://tinder.com'
      self.close_popup_path = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
      self.close_match_path = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
      self.close_payment_path = '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
      self.close_out_of_likes_path = '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
      self.btn_like_path = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]'
      self.btn_dislike_path = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]'
      self.btn_fb_path = '//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button'
    elif self.name == 'badoo':
      self.website_path = 'https://badoo.com/fr/'
      self.close_popup_path = '/html/body/aside/section/div[1]/div/div[2]/div/div[2]'
      self.close_match_path = '/html/body/aside/section/div[1]/div/div[1]/div[4]'
      self.close_payment_path = '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
      self.close_out_of_likes_path = '/html/body/aside/section/div[1]/div/div[1]/section/div/div[2]/div'
      self.btn_like_path = '//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[1]/div[1]'
      self.btn_dislike_path = '//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[2]/div[1]'
      self.btn_fb_path = '//*[@id="page"]/div[2]/div[3]/div/div[3]/div/div[1]/div[2]/div/div/a'
  
  def setModel(model):
    self.model = model

  def login(self):
    pass

  def like(self):
    """
    Perform like action
    """
    like_btn = self.wait.until(lambda d: d.find_element_by_xpath(self.btn_like_path))
    like_btn.click()

  def dislike(self):
    """
    Perform dislike action
    """
    dislike_btn = self.wait.until(lambda d: d.find_element_by_xpath(self.btn_dislike_path))
    dislike_btn.click()

  def close_popup(self):
    """
    Close annoying popup
    """
    popup_3 = self.driver.find_element_by_xpath(self.close_popup_path)
    if popup_3:
      popup_3.click()

  def close_match(self):
    """
    Close match popup
    """
    match_popup = self.driver.find_element_by_xpath(self.close_match_popup)
    if match_popup:
      match_popup.click()
  
  def close_payment(self):
    """
    Close payment popup
    """
    payment_popup = self.driver.find_element_by_xpath(self.close_payment_path)
    if payment_popup:
      payment_popup.click()
  
  def out_of_likes(self):
    """
    Close out of likes popup
    """
    likes_popup = self.driver.find_element_by_xpath(self.close_out_of_likes_path)
    if likes_popup:
      print("Out of likes.")
      likes_popup.click()

  def login(self):
    """
    Perform login with facebook action
    """
    self.driver.get(self.website_path)

    fb_btn = self.wait.until(lambda d: d.find_element_by_xpath(self.btn_fb_path))
    fb_btn.click()

    # switch to login popup
    base_window = self.driver.window_handles[0]
    self.driver.switch_to.window(self.driver.window_handles[1])

    if (self.driver.find_element_by_xpath('//*[@id="email"]') and self.driver.find_element_by_xpath('//*[@id="pass"]')):
      email_in = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="email"]'))
      email_in.send_keys(self.username)

      pw_in = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="pass"]'))
      pw_in.send_keys(self.password)

      login_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="u_0_0"]'))
      login_btn.click()
    else:
      login_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="u_0_4"]/div[2]/div[1]/div[1]/button'))
      login_btn.click()

    self.driver.switch_to.window(base_window)

    if self.name == 'tinder':
       # validate location
      popup_1 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
      popup_1.click()

      # validate incoming notification from tinder
      popup_2 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
      popup_2.click()

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
              self.close_payment()
            except Exception:
              try:
                self.out_of_likes()
                print("Out of likes.")
              except Exception:
                sleep(50)
                print('Unknow error.')
                break
  
  def message_all(self):
    pass

  def get_image_path(self):
    pass
  
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
