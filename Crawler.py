
import sys
import re
from sets import Set
import Queue
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver import ActionChains


def crawl(rate_my_professor, source):

    driver = webdriver.Chrome()
    driver.get(source)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    professor_urls = Set()

    for href in soup.find_all('a', href=True):
        link = href.get('href')
        if "/ShowRatings.jsp?tid=" in link:
            link = rate_my_professor + link
            professor_urls.add(link)

    return professor_urls


def load_more(source):

    load_more_xpath = '//*[@id="mainContent"]/div[1]/div/div[5]/div/div[1]'

    driver = webdriver.Chrome()
    driver.get(source)
    for x in range(20):
        try:
            load_more_button = driver.find_element_by_xpath(load_more_xpath)
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(2)
            load_more_button.click()
            time.sleep(2)
        except Exception as e:
            print e
            break
    print "Complete"
    time.sleep(10)
    f = open("ratemyprofessor.html", "w")
    f.write(driver.page_source.encode('utf-8'))
    # print driver.page_source.encode('utf-8')
    f.close()
    driver.quit()


def output_to_file(set):
    f = open("professor_urls.txt", "w")
    for link in set:
        f.write(link + "\n")
    f.close()


# run if main file
if __name__ == "__main__":

    rate_my_professor = "http://www.ratemyprofessors.com/"
    source = 'http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Michigan&schoolID=1258&queryoption=TEACHER'
    #
    # professor_urls = crawl(rate_my_professor, source)
    # output_to_file(professor_urls)

    load_more(source)
