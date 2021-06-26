import pymysql as pymysql
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from wordcloud import WordCloud, STOPWORDS
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import random



def click_url(url, header):
    req = requests.get(url, header)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup


def pagination(page, search, city):
    my_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        "referrer": "www.Google.com"}
    search = search.replace(" ", "%20")
    # url = 'https://www.indeed.com/jobs?q=software%20developer&l=McKinney%2C%20TX&start=' + str(page)
    url = 'https://www.indeed.com/jobs?q=' + search + '&l=' + city + ',%20TX&start=' + str(page)
    req = requests.get(url, my_header)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup


def is_state(txt):
    states_abbrev = ('AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID',
                     'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND',
                     'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX',
                     'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY')
    for state in range(len(states_abbrev)):
        if txt.upper() == states_abbrev[state].upper():
            return True
    return False


def split_location(loc):
    location_split = loc.replace(",", "").replace("-", "").replace("•", "").split(" ")
    city = state = zip_code = ""
    for element in location_split:
        if element.isnumeric():
            zip_code = element
        elif is_state(element):
            state = element
        elif element.isalpha():
            city = element
    location = {
        'city': city,
        'state': state,
        'zip_code': zip_code,
    }
    return location


def salary_format(sal_split):
    for sal in range(len(sal_split)):
        sal_split[sal] = ''.join(i for i in sal_split[sal] if i.isdigit())

    salary_min_hourly = salary_max_hourly = 0
    salary_hourly = 0
    salary_min_year = 0
    salary_max_year = 0
    if len(sal_split) == 1:
        salary_year = int(sal_split[0])
        if salary_year < 1000:
            salary_hourly = salary_year
            salary_year = 0
            salary_min_hourly = 0
            salary_max_hourly = 0
            salary_min_year = 0
            salary_max_year = 0
    else:
        salary_min_year = int(sal_split[0])
        salary_max_year = int(sal_split[1])
        salary_year = 0
        salary_hourly = 0
        if salary_max_year < 1000:
            salary_min_hourly = salary_min_year
            salary_max_hourly = salary_max_year
            salary_min_year = 0
            salary_max_year = 0
    salary = {
        'salary_year': salary_year,
        'salary_hourly': salary_hourly,
        'salary_min_year': salary_min_year,
        'salary_max_year': salary_max_year,
        'salary_min_hourly': salary_min_hourly,
        'salary_max_hourly': salary_max_hourly
    }
    return salary


def check_languages(desc):
    languages_mentioned = []  # will contain languages mentioned in the description
    word_list = desc.split(" ")  # split description into separate strings
    all_languages = ["JAVA", "C", "C++", "C#", "Python", ".NET", "JavaScript", "PHP", "SQL", "OBJECTIVE-C", "ASSEMBLY",
                     "MATLAB", "PERL", "PASCAL", "R", "RUBY", "VISUAL BASIC", "GO", "GROOVY", "SWIFT", "SAS", "LUA",
                     "DART",
                     "FORTRAN", "COBOL", "SCRATCH", "SCALA", "ABAP", "LISP", "ADA", "RUST", "KOTLIN", "HASKELL", "G",
                     "JULIA", "TCL", "POSTSCRIPT", "ERLANG", "BASH", "HTML", "CSS", "ANGULAR", "REACT", "VUE",
                     "NODE.JS", "NODE", "NODEJS"]
    for word in word_list:  # check for matching languages
        for language in all_languages:
            if word.upper() == language.upper():
                languages_mentioned.append(language.upper())
    languages_mentioned = list(dict.fromkeys(languages_mentioned))  # remove duplicates
    return languages_mentioned


def check_degree(desc):
    degrees_mentioned = []  # will contain degrees mentioned in the description
    word_list = desc.replace("'", "").split(" ")  # split description into separate strings
    all_degrees = ["CERTIFICATE", "CERTIFICATION", "ASSOCIATE", "ASSOCIATES", "A.S.", "BACHELOR", "BACHELORS", "B.S.",
                   "MASTER", "MASTERS", "M.S.", "PHD", "PH.D", "DOCTORATE", "DOCTORATES", "DOCTORAL"]
    for word in word_list:  # check for matching degrees
        for degree in all_degrees:
            if word.upper() == degree.upper():
                degrees_mentioned.append(degree.upper())
    degrees_mentioned = list(dict.fromkeys(degrees_mentioned))  # remove duplicates
    for degree in range(len(degrees_mentioned)):  # organize data for database
        if degrees_mentioned[degree].upper() == 'CERTIFICATION':
            degrees_mentioned[degree] = 'CERTIFICATE'
        elif degrees_mentioned[degree].upper() == 'ASSOCIATE' or degrees_mentioned[degree].upper() == 'A.S.':
            degrees_mentioned[degree] = 'ASSOCIATES'
        elif degrees_mentioned[degree].upper() == 'BACHELOR' or degrees_mentioned[degree].upper() == 'B.S.':
            degrees_mentioned[degree] = 'BACHELORS'
        elif degrees_mentioned[degree].upper() == 'MASTER' or degrees_mentioned[degree].upper() == 'M.S.':
            degrees_mentioned[degree] = 'MASTERS'
        elif degrees_mentioned[degree].upper() == 'PH.D' or degrees_mentioned[degree].upper() == 'DOCTORATE' or degrees_mentioned[degree].upper() == 'DOCTORATES' or degrees_mentioned[degree].upper() == 'DOCTORAL':
            degrees_mentioned[degree] = 'PHD'
    return degrees_mentioned


def check_keywords(desc):
    keywords_mentioned = []
    word_list = desc.replace("'", "").split(" ")  # split description into separate strings
    interpersonal_skills = ['Assertiveness','Assertiveness','Bodylanguage','Bullying','Charisma','Clarification','Collaboration','Communication','Communication','Interpersonal','Communication, Barriers to Effective','Communication, Improving','Communication, Non-Verbal','Verbal','Effective','Confidentiality','Conflict','Managing','Conflict','Resolution','Mediation','Conversational','Criticism','Constructive','Criticism','Customer','Telephone','Emotional','Intelligence','Empathy','Employability','Feedback','Group','Behaviours','Cohesiveness','Life-Cycle','Groups', 'Teams','Harassment']
    intrapersonal_skills = ['verbal communication','non-verbal communication','listening','negotiation','solving','decision-making','assertiveness','patience','empathy']
    ide = ['Jupyter ','JupyterLab','Jupyter-Notebooks','RStudio','PyCharm','Notepad++','Spyder','Sublime Text','Vim','Emacs','MATLAB','Atom','Eclipse','NetBeans','IntelliJ','BlueJ','JDeveloper','DrJava','JCreator','jGRASP','Greenfoot','Xcode','Codenvy','RAD','Visual Studio','Visual Studio Code','CodeBlocks','CodeLite','CLion','Qt Creator','Nuclide','WebStorm','Sublime']

    for word in word_list:  # check for matching degrees
        for key in interpersonal_skills:
            if word.upper() == key.upper():
                keywords_mentioned.append(key.upper())
        for key in intrapersonal_skills:
            if word.upper() == key.upper():
                keywords_mentioned.append(key.upper())
        for key in ide:
            if word.upper() == key.upper():
                keywords_mentioned.append(key.upper())
    keywords = list(dict.fromkeys(keywords_mentioned))  # remove duplicates

    # print(keywords)
    return keywords


# //////////////////////////////////////////////////////////////////////////////////////// get_post() start
def get_post(page):
    my_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    entries = []
    post = page.find_all('div', class_='jobsearch-SerpJobCard')
    for element in post:
        url_post = element.find('a', attrs={'class': 'jobtitle turnstileLink'})['href']
        url_post = "https://www.indeed.com" + url_post
        title = element.find('a', attrs={'class': 'jobtitle'}).text.strip()
        company = element.find('span', attrs={'class': 'company'}).text.strip()
        location_dict = []
        try:
            location = element.find(class_='location').text.strip()
            location_dict = split_location(location)
        except NoSuchElementException:
            location = ""

        remote = False
        try:
            remote_check = element.find('span', attrs={'class': 'remote'}).text.strip()
            remote = True
        except AttributeError:
            remote = False
        if title.upper().find("REMOTE") != -1:
            remote = True

        salary = {}
        try:
            salary_split = element.find('span', attrs={'class': 'salaryText'}).text.strip().replace(',', "").replace(
                '$', "").strip().split("-")
            salary = salary_format(salary_split)
        except AttributeError:
            salary = {
                'salary_year': 0,
                'salary_hourly': 0,
                'salary_min_year': 0,
                'salary_max_year': 0,
                'salary_min_hourly': 0,
                'salary_max_hourly': 0
            }

        job_description = element.find('div', attrs={'class': 'summary'}).text.strip().replace("\n", "")

        page = click_url(url_post, my_header)
        job_description = get_description(page)

        date_days = 0
        date_text = element.find(class_='date').text.strip()
        if date_text.upper() == "TODAY" or date_text.upper() == "JUST POSTED":
            date = datetime.datetime.now()
        else:
            date_days = int(''.join(i for i in date_text if i.isdigit()))
            date = datetime.datetime.now() - datetime.timedelta(days=date_days)  # subtract 'days ago' from current date
        date = date.strftime("%x")  # change to mm/dd/yy format

        popular_words = most_common_word(job_description, 10)

        entry = {
            'url': url_post,
            'title': title,
            'company': company,
            'location': location_dict,
            'remote': remote,
            'salary': salary,
            'job_description': job_description,
            'most_common_words': popular_words,
            'keywords': check_keywords(job_description),
            'languages': check_languages(job_description),
            'degrees': check_degree(job_description),
            'date': str(date)
        }
        entries.append(entry)
        print(entry)
    return entries


# //////////////////////////////////////////////////////////////////////////////////////// get_post() end


def get_description(page):
    job_description = ""
    try:
        job_description = page.find('div', attrs={'id': 'jobDescriptionText'}).text.strip().replace("\n", " ").replace('\\', "")
    except AttributeError:
        print(page.current_url)
        print("LINE 200 -- job_description not found")
    return job_description


def most_common_word(desc, num_results):
    desc_list = desc.split(" ")
    counter = {}
    for i in desc_list:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    most_common = sorted(counter, key=counter.get, reverse=True)
    results = most_common[:num_results]
    return results


def connect_to_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='###',
        db='indeeddb'
    )

    if conn:
        print("\nConnected to database")
        return conn
    else:
        print("Failed to connect to database")
        return


def insert_to_db(data, conn):
    if len(data) < 1:
        print("INVALID DATA")
        return

    my_cursor = conn.cursor()

    for entry in data:
        sql = "INSERT IGNORE INTO post (url,title,company,city,state,zip_code,remote,job_description, date_posted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (str(entry['url']), str(entry['title']), str(entry['company']), str(entry['location']['city']),
               str(entry['location']['state']), str(entry['location']['zip_code']), entry['remote'],
               str(entry['job_description']), str(entry['date']))
        my_cursor.execute(sql, val)
        for lang in entry['languages']:
            sql = "INSERT IGNORE INTO languages (url,language) VALUES (%s, %s)"
            val = (str(entry['url']), str(lang))
            my_cursor.execute(sql, val)
        for degree in entry['degrees']:
            sql = "INSERT IGNORE INTO degrees (url,degree) VALUES (%s, %s)"
            val = (str(entry['url']), str(degree))
            my_cursor.execute(sql, val)
        for word in range(len(entry['most_common_words'])):
            sql = "INSERT IGNORE INTO most_common_words (url,ranking,word) VALUES (%s, %s, %s)"
            val = (str(entry['url']), int(word), str(entry['most_common_words'][word]))
            my_cursor.execute(sql, val)
        for word in entry['keywords']:
            sql = "INSERT IGNORE INTO keywords (url,word) VALUES (%s, %s)"
            val = (str(entry['url']), str(word))
            my_cursor.execute(sql, val)
        sql = "INSERT IGNORE INTO  salary(url,salary_year,salary_hourly,salary_min_year,salary_max_year,salary_min_hourly,salary_max_hourly) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (str(entry['url']), str(entry['salary']['salary_year']), str(entry['salary']['salary_hourly']),
               str(entry['salary']['salary_min_year']), str(entry['salary']['salary_max_year']),
               str(entry['salary']['salary_min_hourly']), str(entry['salary']['salary_max_hourly']))
        my_cursor.execute(sql, val)
    try:
        conn.commit()
        print("Successfully inserted data into database")
    except pymysql.IntegrityError:
        print("Failed to Insert data into database")
    conn.close()


def select_from_db(sql, conn):
    print("~ SELECTING FROM DATABASE")
    my_cursor = conn.cursor()

    my_cursor.execute(sql)
    rows = my_cursor.fetchall()
    return rows


def bar_graph(data, x_title, legend_title):
    if len(data) < 1:
        print("Not enough data to make a bar graph")
        return
    else:
        print("********************************")
        print("Status: CREATING BAR GRAPH")
        print("********************************")

    names = []
    vals = []
    for i in range(len(data)):
        names.append(str(data[i][0]))
        vals.append(int(data[i][1]))
    df = pd.DataFrame({x_title:names, legend_title:vals})
    ax = df.plot.bar(x=x_title, y=legend_title, rot=0, color='green', figsize=(15,7))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def pie_chart(data, title):
    if len(data) < 1:
        print("Not enough data to make a bar graph")
        return
    else:
        print("********************************")
        print("Status: CREATING PIE CHART")
        print("********************************")

    names = []
    vals = []
    for i in range(len(data)):
        names.append(str(data[i][0]))
        vals.append(int(data[i][1]))

    df = pd.DataFrame({title:vals}, index=names)
    plot = df.plot.pie(y=title, figsize=(7,7))
    plt.show()


def line_graph(data, title):
    if len(data) < 1:
        print("Not enough data to make a bar graph")
        return
    else:
        print("********************************")
        print("Status: CREATING LINE GRAPH")
        print("********************************")

    names = []
    vals = []
    for i in range(len(data)):
        names.append(str(data[i][0]))
        vals.append(int(data[i][1]))
    print(names)
    df = pd.DataFrame({title:vals}, index=names)
    lines = df.plot.line()
    plt.tight_layout()
    plt.show()


def word_cloud(data):
    new_str = ""
    for desc in data:
        new_str += str(desc).replace("'", "")

    wordcloud = WordCloud(width=800, height=400, max_font_size=100, max_words=100, background_color="white").generate(new_str)

    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def progress_bar(index, total, bar_len=50, title='Please wait'):
    percent_done = (index + 1) / total * 100
    percent_done = round(percent_done, 1)

    done = round(percent_done / (100 / bar_len))
    togo = bar_len - done

    done_str = '█' * int(done)
    togo_str = '░' * int(togo)

    print(f'\r{title}: [{done_str}{togo_str}] {percent_done}% done', end="", flush=True)


print("=== Indeed Scraper ===")
print("1. Start Scraping")
print("2. Database")
print("0. Exit")

print("---------------------------------")
choice = int(input("Enter an option: "))
print("---------------------------------")
if choice == 1:
    city = input("Enter a city: ")
    search_field = input("Enter a search field for Indeed: ")
    num_pages = int(input("How many pages would you like to scrape? "))
    starting_page = int(input("Which page would you like to start on? "))
    if starting_page == 1:
        starting_page = 0
    percent_complete = 0
    print("***************************")
    print("Status: STARTING")
    print("~ " + str(percent_complete) + " of " + str(num_pages) + " pages complete")
    print("***************************")
    count = 0
    for i in range(starting_page*10, (num_pages*10)+(starting_page*10), 10):
        count += 1
        page = pagination(i, search_field, city)
        results = get_post(page)
        print(results)
        conn = connect_to_db()
        insert_to_db(results, conn)
        print("-------------------------------")
        print("~ " + str(count) + " of " + str(num_pages) + " pages complete")
        print("-------------------------------")
        rand_time = random.randint(450, 700)
        print("*******************************************************")
        minutes = int(rand_time/60)
        seconds = int((float(rand_time/60) - minutes) * 60)
        print("Status: SLEEPING FOR " + str(minutes) + " MINUTES and " + str(seconds) + " SECONDS")
        print("*******************************************************")
        for current_time in range(rand_time):
            progress_bar(current_time, rand_time)
            time.sleep(1)
        print("\n")
    print("***************************")
    print("Status: FINISHED")
    print("***************************")
elif choice == 2:
    print("********************************")
    print("\t\t\tDATABASE")
    print("********************************")
    print("1. Make a SQL query")
    print("2. Gather Statistics")

    print("---------------------------------")
    choice2 = int(input("Enter an option: "))
    print("---------------------------------")

    print("********************************")
    print("Status: CONNECTING TO DATABASE")
    print("********************************")
    conn = connect_to_db()
    if choice2 == 1:
        sql = input("Enter SQL command: ")
        select_from_db(sql, conn)
    elif choice2 == 2:
        print("********************************")
        print("\t\t\tStatistics")
        print("********************************")
        print("1. Make bar graphs")
        print("2. Make pie charts")
        print("3. Make line graphs")
        print("4. Make word clouds")

        print("---------------------------------")
        choice3 = int(input("Enter an option: "))
        print("---------------------------------")

        if choice3 == 1:
            # bar graph of most common languages
            sql = "SELECT city, COUNT(city) " \
                  "FROM post " \
                  "GROUP BY city " \
                  "ORDER BY COUNT(city) DESC"
            result_city_count = select_from_db(sql, conn)
            bar_graph(result_city_count, 'Cities', 'Job listings from cities')

            # bar graph of most common languages
            sql = "SELECT language, COUNT(language) " \
                  "FROM languages " \
                  "GROUP BY language " \
                  "ORDER BY COUNT(language) DESC"
            result_language_count = select_from_db(sql, conn)
            bar_graph(result_language_count, 'Languages', 'Language')

            # bar graph of amount of remote jobs in cities
            sql = "SELECT city, COUNT(remote) " \
                  "FROM post " \
                  "WHERE remote = 1 AND city != 'States' AND city != 'Texas'" \
                  "GROUP BY city " \
                  "ORDER BY COUNT(remote) DESC"
            result_language_count = select_from_db(sql, conn)
            bar_graph(result_language_count, 'Cities', 'Remote jobs available')
        elif choice3 == 2:
            # pie chart of most popular degrees
            sql = "SELECT degree, COUNT(degree) " \
                  "FROM degrees " \
                  "GROUP BY degree"
            result_degree_count = select_from_db(sql, conn)
            pie_chart(result_degree_count, 'Degrees')
        elif choice3 == 3:
            # line graphs of different salary categories
            sql = "SELECT language, AVG(salary_year) FROM salary, languages WHERE salary_year > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average salary per year by language')
            sql = "SELECT language, AVG(salary_hourly) FROM salary, languages WHERE salary_hourly > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average salary per hour by language')
            sql = "SELECT language, AVG(salary_min_year) FROM salary, languages WHERE salary_min_year > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average minimum salary per year by language')
            sql = "SELECT language, AVG(salary_max_year) FROM salary, languages WHERE salary_max_year > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average maximum salary per year by language')
            sql = "SELECT language, AVG(salary_max_hourly) FROM salary, languages WHERE salary_max_hourly > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average minimum salary per hour by language')
            sql = "SELECT language, AVG(salary_max_hourly) FROM salary, languages WHERE salary_max_hourly > 0 AND salary.url = languages.url GROUP BY language"
            result_degree_count = select_from_db(sql, conn)
            line_graph(result_degree_count, 'Average maximum salary per hour by language')
        elif choice3 == 4:
            # word cloud of most popular words in job descriptions
            sql = "SELECT DISTINCT job_description " \
                  "FROM post "
            result_job_descriptions = select_from_db(sql, conn)
            word_cloud(result_job_descriptions)

            # word cloud of most popular words in job descriptions
            sql = "SELECT DISTINCT word " \
                  "FROM keywords " \
                  "GROUP BY word"
            result_keywords = select_from_db(sql, conn)
            word_cloud(result_keywords)

else:
    exit()

# posts[0].click()
# print(driver.switch_to.window(driver.window_handles[1]))
# print(driver.current_url)
# page = click_url(driver.current_url, my_header)
# inspect_page(page)
