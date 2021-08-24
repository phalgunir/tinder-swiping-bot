import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# facebook login credentials
FB_EMAIL = 'email@gmail.com'
FB_PASSWORD = 'password'

chrome_driver_path = '/Applications/chromedriver'
driver = webdriver.Chrome(chrome_driver_path)


def login():
    # click 'log in' on base page
    login_button = driver.find_element_by_xpath('//*[@id="u-648818393"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/span')
    login_button.click()
    time.sleep(3)

    # find all buttons and click 'log in with facebook'
    all_login_buttons = driver.find_elements_by_tag_name('button')
    for login_button in all_login_buttons:
        # if 'log in with facebook' button appears
        if login_button.text.lower() == 'log in with facebook':
            login_button.click()

        # if 'more options' button appears
        elif login_button.text.lower() == 'more options':
            login_button.click()
            time.sleep(2)
            # then click 'log in with facebook'
            new_login_buttons = driver.find_elements_by_tag_name('button')
            for new_login_button in new_login_buttons:
                if new_login_button.text.lower() == 'log in with facebook':
                    new_login_button.click()

    time.sleep(3)
    # changing the window handle to access the login page
    login_page = driver.window_handles[1]
    driver.switch_to.window(login_page)

    # sending facebook login credentials
    driver.find_element_by_id('email').send_keys(FB_EMAIL)
    driver.find_element_by_id('pass').send_keys(FB_PASSWORD)
    time.sleep(2)
    driver.find_element_by_id('loginbutton').click()


tinder_url = 'https://tinder.com'
driver.get(tinder_url)
# storing the current base page window handle to get back to it later
base_page = driver.current_window_handle
time.sleep(3)

login()
time.sleep(5)

# switch handle to base page
driver.switch_to.window(base_page)
# allow location popup
driver.find_element_by_xpath('//*[@id="u1917767827"]/div/div/div/div/div[3]/button[1]').click()
time.sleep(3)
# disable notifications popup
driver.find_element_by_xpath('//*[@id="u1917767827"]/div/div/div/div/div[3]/button[2]').click()
time.sleep(5)


# tinder allows only 100 likes per day on free tier
for n in range(100):
    buttons = driver.find_elements_by_css_selector('button')
    try:
        for button in buttons:
            # click like button
            if button.text == 'LIKE':
                button.click()
                print(f'Liked {n+1}')
                time.sleep(3)

            # # click reject button
            # if button.text == 'NOPE':
            #     button.click()
            #     print(f'Rejected {n+1}')
            #     time.sleep(3)

    except NoSuchElementException:
        print('Waiting for profile to load')
        time.sleep(5)

    except ElementClickInterceptedException:
        driver.find_element_by_xpath('//*[@id="u-318447192"]/div/div/div[1]/div/div[4]/button').click()
        print("Dismissed 'It's a match' popup.")
        time.sleep(3)


driver.quit()
