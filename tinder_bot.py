from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
import random

from secrets import username, password

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get('https://tinder.com')

        fb_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button'))
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

        # validate location
        popup_1 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
        popup_1.click()

        # validate incoming notification from tinder
        popup_2 = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
        popup_2.click()

    def like(self):
        like_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]'))
        like_btn.click()

    def dislike(self):
        dislike_btn = self.wait.until(lambda d: d.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]'))
        dislike_btn.click()

    def auto_swipe(self):
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
                                print("Plus de like disponible.")
                                break
                        except Exception:
                            print('Erreur inconnue.')
                            break
    
    def message_all(self):
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

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()
    
    def close_payment(self):
        payment_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]')
        payment_popup.click()
    
    def out_of_likes(self):
        likes_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]')
        if likes_popup:
            likes_popup.click()
            return 1
    
    def quit(self):
        print('Fin du bot. Have fun ! ;)')
        self.driver.quit()
