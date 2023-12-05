from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

ua = UserAgent()

url = "ссылка"
options = webdriver.ChromeOptions()
options.add_argument('--enable-javascript')
options.add_argument(f'user-agent={ua.random}')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def login():
    try:
        driver.get(url=url)

        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "index_email"))
        )
        email_input.clear()
        num = input("Введите свой номер >>>> ")
        email_input.send_keys(num)

        login_button = driver.find_element(By.CLASS_NAME, "FlatButton__in")
        login_button.click()

        code_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "vkc__TextField__input"))
        )

        code = input("Введите код >>>> ")
        code_input.send_keys(code)

    except TimeoutException:
        print("Тайм-аут при ожидании появления элемента. Проверьте правильность идентификатора элемента или увеличьте время ожидания.")
    except Exception as e:
        print(f"Ошибка во время входа: {e}")

def comment_parse():
    try:
        comments_section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "wl_replies"))
        )

        comment_elements = comments_section.find_elements(By.CLASS_NAME, "reply_text")

        for comment_element in comment_elements:
            comment_text = comment_element.text

            comment_text = comment_text.split('\n')[0]

            with open("vk/vk_coments.txt", "a", encoding="utf-8") as file:
                file.write(comment_text + "\n")
            
    except Exception as e:
        print(e)


def main():
    try:
        login()
        time.sleep(15)
        comment_parse()
    except Exception as e:
        print(f"Ошибка main: {e}")

    finally:
        try:
            time.sleep(5)
            driver.close()
            driver.quit()
        except Exception as e:
            print(f"Ошибка при закрытии драйвера: {e}")

if __name__ == "__main__":
    main()
