from selenium import webdriver
import time, csv

def hashtagUrlCrawller(tag, chromedriverLocation, saveLocation) :
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Chrome/65.0.3325.181")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriverLocation, chrome_options = options)
    driver.get("https://www.instagram.com/explore/tags/%s/" % tag)

    save = []
    last_height = driver.execute_script('return document.body.scrollHeight')

    try :

        for i in range(10000) :
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            new_height = driver.execute_script('return document.body.scrollHeight')

            if new_height != last_height :
                for post in driver.find_elements_by_css_selector("div._mck9w > a") :
                    save.append(post.get_attribute("href"))
                    
                save = list(set(save))
                print(i)
                last_height = new_height

            elif new_height == last_height :
                driver.get("https://www.instagram.com/explore/tags/%s/" % tag)
                time.sleep(10)
                print(i, "refresh")
                last_height = driver.execute_script('return document.body.scrollHeight')

        driver.close()
        for i in save :
            with open(saveLocation, "a", encoding = "UTF-8") as f :
                f.write("%s\n" % i)

    except :
        for i in save :
            with open(saveLocation, "a", encoding = "UTF-8") as f :
                f.write("%s\n" % i)
        


def userPostUrlCrawller(userID, chromedriverLocation, saveLocation) :
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Chrome/65.0.3325.181")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriverLocation, chrome_options = options)
    driver.get("https://www.instagram.com/%s/" % userID)

    save = []
    last_height = driver.execute_script('return document.body.scrollHeight')

    try :

        while (True) :
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            new_height = driver.execute_script('return document.body.scrollHeight')

            if new_height != last_height :
                for post in driver.find_elements_by_css_selector("div._mck9w > a") :
                    save.append(post.get_attribute("href"))
                    
                save = list(set(save))
                print(i)
                last_height = new_height

            elif new_height == last_height :
                break;

        driver.close()
        for i in save :
            with open(saveLocation, "a", encoding = "UTF-8") as f :
                f.write("%s\n" % i)

    except :
        driver.close()
        for i in save :
            with open(saveLocation, "a", encoding = "UTF-8") as f :
                f.write("%s\n" % i)


def postCrawller(urlFile, chromedriverLocation, saveLocation) :
    with open(saveLocation, "a", encoding = "UTF-8") as f :    # csv 저장
            wr = csv.writer(f, delimiter  = "\t")
            wr.writerow(["username", "userUrl", "updated", "hashtag", "likes", "imageUrl"])

    url = []
    with open(urlFile, "r") as f :
        for i in f :
            url.append(i)

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Chrome/65.0.3325.181")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriverLocation, chrome_options = options)
    
    count = 0
    for post in url :
        driver.get(post)

        print(count, end = " ")
        count += 1

        try :
            username = driver.find_elements_by_css_selector("a._2g7d5.notranslate._iadoq")[0].text
        except :
            username = None
            print("skip username", end = " ")
        
        try :
            userUrl = driver.find_elements_by_css_selector("a._2g7d5.notranslate._iadoq")[0].get_attribute("href")
        except :
            userUrl = None
            print("skip userUrl", end = " ")

        try :
            hashtag = []
            for tag in driver.find_elements_by_css_selector("a") :
                if tag.text.find("#") != -1 :
                    hashtag.append(tag.text)
        except :
            hashtag = None
            print("skip hashtag", end = " ")

        try :
            updated = driver.find_elements_by_css_selector("time._p29ma")[0].text
        except :
            updated = None
            print("skip updated", end = " ")

        try :
            if driver.find_elements_by_css_selector("div._3gwk6 > * > span") :  # 좋아요 수
                likes = driver.find_elements_by_css_selector("div._3gwk6 > * > span")[0].text
            elif driver.find_elements_by_css_selector("div._ebcx9 > section._1w76c._nlmjy > div > span") :  # 만약 조회수가 나와있을 경우 클릭하고 좋아요 수를 긁어옴
                driver.find_elements_by_css_selector("div._ebcx9 > section._1w76c._nlmjy > div > span")[0].click()
                likes = driver.find_elements_by_css_selector("div._m10kk > span")[0].text
            else :  # 좋아요 수가 너무 적어서 몇명이 좋아요 했는지 숫자가 안나오면 셀 가치가 없음
                likes = 0
        except :
            likes = None
            print("skip likes", end = " ")

        try :   
            if driver.find_elements_by_css_selector("div._4rbun > img") :   # 이미지
                img = driver.find_elements_by_css_selector("div._4rbun > img")[0].get_attribute("src")
            else :  # 동영상일 경우
                img = driver.find_elements_by_css_selector("div._qzesf > img")[0].get_attribute("src")
        except :
            img = None
            print("skip image", end = " ")

        try :
            with open(saveLocation, "a", encoding = "UTF-8") as f :    # csv 저장
                wr = csv.writer(f, delimiter  = "\t")
                wr.writerow([username, userUrl, updated, hashtag, likes, img])
        except :
            print("skip save", end = "")

        print("")

    driver.close()

    
def followCrawller_instaLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword) :
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Chrome/65.0.3325.181")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriverLocation, chrome_options = options)

    driver.get("https://www.instagram.com/")
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
    time.sleep(1)

    driver.find_element_by_name("username").send_keys(yourid)
    driver.find_element_by_name("password").send_keys(yourpassword)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click()
    time.sleep(3)

    user_url = []
    with open(urlFile, "r") as f :
        for i in f :
            user_url.append(i.replace("\n", ""))

    for url in user_url :
        try :
            driver.get(url)
            user = url[26:len(url)-1]
            print("start", user, "followers")
            time.sleep(1)

            driver.find_elements_by_css_selector("._t98z6")[1].click()
            time.sleep(1)

            last_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')

            count = 0
            while True :
                driver.execute_script('document.getElementsByClassName("_gs38e")[0].scrollTo(0, document.getElementsByClassName("_gs38e")[0].scrollHeight);')
                time.sleep(6)
                new_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')
                if new_height != last_height :
                    print(count)
                    count += 1
                    last_height = new_height
                elif new_height == last_height :
                    print(user, "complete followers")
                    break
                    
            followers = driver.find_elements_by_css_selector("div._2nunc > a")

            for i in followers :
                with open(saveLocation, "a", encoding = "UTF-8") as f :
                    wr = csv.writer(f)
                    wr.writerow([i.text, user])

        except :
            print(user, "has not followers")

        try :
            driver.get(url)
            time.sleep(6)
            print("start", user, "following")

            driver.find_elements_by_css_selector("._t98z6")[2].click()
            time.sleep(6)

            last_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')

            count = 0
            while True :
                driver.execute_script('document.getElementsByClassName("_gs38e")[0].scrollTo(0, document.getElementsByClassName("_gs38e")[0].scrollHeight);')
                time.sleep(6)
                new_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')
                if new_height != last_height :
                    print(count)
                    count += 1
                    last_height = new_height
                elif new_height == last_height :
                    print(user, "complete following")
                    break

            following = driver.find_elements_by_css_selector("div._2nunc > a")

            for i in following :
                with open(saveLocation, "a", encoding = "UTF-8") as f :
                    wr = csv.writer(f)
                    wr.writerow([user, i.text])

        except :
            print(user, "has not following")

    print("finish")
    driver.close()

def followCrawller_facebookLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword) :
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Chrome/65.0.3325.181")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriverLocation, chrome_options = options)

    driver.get("https://www.instagram.com/")
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click()
    time.sleep(1)

    driver.find_element_by_name("email").send_keys(yourid)
    driver.find_element_by_name("pass").send_keys(yourpassword)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
    time.sleep(3)

    user_url = []
    with open(urlFile, "r") as f :
        for i in f :
            user_url.append(i.replace("\n", ""))

    for url in user_url :
        try :
            driver.get(url)
            user = url[26:len(url)-1]
            print("start", user, "followers")
            time.sleep(1)

            driver.find_elements_by_css_selector("._t98z6")[1].click()
            time.sleep(1)

            last_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')

            count = 0
            while True :
                driver.execute_script('document.getElementsByClassName("_gs38e")[0].scrollTo(0, document.getElementsByClassName("_gs38e")[0].scrollHeight);')
                time.sleep(6)
                new_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')
                if new_height != last_height :
                    print(count)
                    count += 1
                    last_height = new_height
                elif new_height == last_height :
                    print(user, "complete followers")
                    break
                    
            followers = driver.find_elements_by_css_selector("div._2nunc > a")

            for i in followers :
                with open(saveLocation, "a", encoding = "UTF-8") as f :
                    wr = csv.writer(f)
                    wr.writerow([i.text, user])

        except :
            print(user, "has not followers")

        try :
            driver.get(url)
            time.sleep(6)
            print("start", user, "following")

            driver.find_elements_by_css_selector("._t98z6")[2].click()
            time.sleep(6)

            last_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')

            count = 0
            while True :
                driver.execute_script('document.getElementsByClassName("_gs38e")[0].scrollTo(0, document.getElementsByClassName("_gs38e")[0].scrollHeight);')
                time.sleep(6)
                new_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')
                if new_height != last_height :
                    print(count)
                    count += 1
                    last_height = new_height
                elif new_height == last_height :
                    print(user, "complete following")
                    break

            following = driver.find_elements_by_css_selector("div._2nunc > a")

            for i in following :
                with open(saveLocation, "a", encoding = "UTF-8") as f :
                    wr = csv.writer(f)
                    wr.writerow([user, i.text])

        except :
            print(user, "has not following")

    print("finish")
    driver.close()