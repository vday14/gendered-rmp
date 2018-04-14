
import sys
import re
from sets import Set
import Queue
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import Professor
import json

# Click the "Load more" button max_prof times
# Write html to file
# Need to load javascript dynamically in order to load professor links
#
# source = source url with All Professors
# max_profs = # of times to click "Load More"
def load_more(source, max_profs):

    load_more_xpath = '//*[@id="mainContent"]/div[1]/div/div[5]/div/div[1]'

    driver = webdriver.Chrome()
    driver.get(source)
    for x in range(max_profs):
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


# "Crawl" the html file outputted from load_more
# Find all the unique professor page links
#
# rate_my_professor = source link to append to local links
def crawl(rate_my_professor):

    f = open("ratemyprofessor.html", "r")
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    f.close()
    professor_urls = Set()

    for href in soup.find_all('a', href=True):
        link = href.get('href')
        if "/ShowRatings.jsp?tid=" in link:
            link = rate_my_professor + link
            professor_urls.add(link)
            # print link

    return professor_urls


# Outputs the links in the set to a file
# set = set of links to write
def output_to_file(set):
    f = open("professor_urls.txt", "w")
    for link in set:
        f.write(link + "\n")
    f.close()


# Get the necessary html for the professor
def get_professor_data(professor_urls):

    prof_dict = {}
    while len(professor_urls) > 0:
        # print len(professor_urls)
        url = professor_urls.pop()
        url = url.encode("utf-8")

        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        prof = soup.find_all('h1', {'class': 'profname'})[0]
        prof_name = prof.getText().encode("utf-8").split()
        prof_name = ' '.join(prof_name)
        print prof_name

        score = soup.find_all('div', {'class': 'grade'})[0]
        score = score.getText().encode("utf-8")
        print score

        prof_tags = {}
        for tags in soup.find_all('span', {'class': 'tag-box-choosetags'}):
            tag = tags.getText().encode("utf-8")
            p = re.compile("\d+")
            num =p.findall(tag)[0]
            tag = tag.split("(")[0].lstrip(' ')
            prof_tags[tag] = num
        print prof_tags

        comments = []
        for comment in soup.find_all('p', {'class': 'commentsParagraph'}):
            comment = comment.getText().encode("utf-8").split()
            comment =' '.join(comment)
            comments.append(comment)
        print comments

        professor = {"url": url,
                    "name": prof_name,
                     "score": score,
                     "tags": prof_tags,
                     "comments": comments
                     }

        pid = re.findall(r'tid=([^]]*)&', url)[0]

        prof_dict[pid] = professor

    output = json.dumps(prof_dict, indent=4)
    f = open("professors.json", "w")
    f.write(output)


# run if main file
if __name__ == "__main__":

    rate_my_professor = "http://www.ratemyprofessors.com/"
    source = 'http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Michigan&schoolID=1258&queryoption=TEACHER'

    # load_more(source, 200)
    professor_urls = crawl(rate_my_professor)
    output_to_file(professor_urls)

    get_professor_data(professor_urls)
