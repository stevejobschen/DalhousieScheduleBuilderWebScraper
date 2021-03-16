# class scrapper
from bs4 import BeautifulSoup
import requests

from ParseCourse import *
import db
from settings import *

def isHeaderRow(row):
    try:
        row['valign']
        return True
    except:
        return False

def parseUrl(url):
    pageCount = 1
    courses = []
    j = 0
    while j < pageCount:
        newUrl = url + "&s_numb=&n=" + setPageHelper(j + 1)
        html_doc = requests.get(newUrl).text
        print(newUrl)
        # use bs4
        # MARK: PAGECOUNT
        soup = BeautifulSoup(html_doc, 'lxml')

        # //Read total number of pages
        try:
            pageCount = len(soup.find_all('table', attrs={'class': 'plaintable'})[3].find('center').find_all('a')) + 1
        except:
            pageCount = 1

        # MARK: ROWS
        # read table line by line
        rows = soup.find_all('table', attrs={'class': 'dataentrytable'})[1].find_all('tr')

        headerIndexs = []
        for i, row in enumerate(rows):
            if isHeaderRow(rows[i]):
                headerIndexs.append(i)

        courses_raw = []
        for i in range(0, len(headerIndexs) - 1):
            course_raw = rows[headerIndexs[i]:(headerIndexs[i + 1])]
            courses_raw.append(course_raw)
        course_raw = rows[headerIndexs[len(headerIndexs) - 1]:]
        courses_raw.append(course_raw)

        for course in courses_raw:
            courses.append(parseCourse(course))
        j += 1
    return courses


def setPageHelper(page):
    if page < 1:
        return '1'
    elif page == 1:
        return '1'
    else:
        return str((20 * (page - 1)) + 1)


def main():
    database = db.Database()
    # Fall and winter cource
    for subject in Settings.semester:
        url = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=" + Settings.termsLibrary[Settings.terms] + "&s_subj=" + subject + "&s_district=" + Settings.district

        # THIS IS THE FINAL ARRAY WITH ALL INFORMATION IN IT
        # use as data[courseindex] .title or .classes[classindex] for full info
        data = parseUrl(url)
        database.saveCourses(data)

if __name__ == "__main__":
    main()
