from selenium import webdriver
from time import sleep
from typing import List


class Instabot:
    def __init__(self, user, password):
        self.username = user
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input').send_keys(user)
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input').send_keys(password)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]').click()
        sleep(4)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        sleep(3)

    def get_unfollowers(self) -> List[str]:
        """
        Return a list of people that you follow but dont follow you back
        :return:
        """
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(1)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        return not_following_back

    def _get_names(self) -> List[str]:
        """
        Return a list of the people in the selected scrollbox
        """
        scrollbox = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        sleep(1)
        last_ht = 0
        ht = 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0,arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollbox)
        links = scrollbox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
        return names

    def unfollow_traitors(self, lst) -> None:
        """
        Unfollow the people in the given list
        1. Iterate through each person you follow
            i. check if that person is included in the list
            ii. if in list find the "following" button and click it
            iii. if not in the list go to the next person

        2. Find all tagnames in scroll box
            i. if tagnames are in lst, find the "following" button associated with tag and click it, make sure to delete tagname from lst
            ii. Once all tags in the scrollbox have been checked scroll to the bottom

        """
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        scrollbox = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_ht = 0
        ht = 1
        while last_ht != ht:
            last_ht = ht
            tags = self.driver.find_elements_by_tag_name('a')
            for item in tags:
                if item.text in lst:
                    lst.remove(item.text)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0,arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollbox)





if __name__ == '__main__':
    my_bot = Instabot('username', 'password')
    lst = my_bot.get_unfollowers()
    print(lst)
    my_bot.unfollow_traitors(lst)

