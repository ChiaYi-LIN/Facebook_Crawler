#%% [markdown]
# 2019/6/7, 1900~2300, 4
# 2019/6/8, 0700~0900, 2
# 2019/6/9, 1100~1300, 2
# 2019/6/10, 1130~1300, 1.5
# 2019/6/10, 1400~1530, 1.5
# 2019/6/12, 2330~0200, 2.5

#%%
from selenium import webdriver
import pandas as pd
from time import sleep, mktime
import os, re
from time import sleep, mktime
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#%%
# # Unused
# def login_FB():
#     email = input("Please input the account email: ")
#     password = getpass.getpass("Please input the password: ")
#     account = [str(email), str(password)]
#     return account

# # Unused
# def group_url():
#     url = input("Please input group URL: ")
#     # url = "https://www.facebook.com/groups/jobsandinternship/"
#     return url

def set_time():
    # year = input("Year of first post (YYYY): ")
    # month = input("Month of first post (MM): ")
    # day = input("Day of first post (DD): ")
    # date = str(year) + "-" + str(month) + "-" + str(day)
    date = "2019/06/11"
    try:
        timestamp = mktime(datetime.strptime(date, "%Y/%m/%d").timetuple())
        timestamp = int(timestamp)
        return(timestamp)
    except:
        print("Invalid input.")
        return("Error")

def check_group_approved():
    try:
        # 公開社團
        if browser.find_element_by_xpath("//div[@class='_19s_']").text == "公開社團":
            return "公開社團"
    
        # 頁面有顯示"加入社團"按鈕
        browser.find_element_by_xpath("//div[@class='_21kr']")
        return "未加入社團"
    except:
        try:
            # 頁面有顯示"已加入"或"等待批准中"按鈕
            apply = browser.find_element_by_xpath("//a[contains(@class,'_42ft _4jy0 _55pi _2agf _4o_4 _p')]")
            if apply.text == "已加入":
                return "已加入社團"
            elif apply.text == "等待批准中":
                return "等待批准中"
        except:
            return "未知錯誤"

def sort_posts_by_time(url):
    if re.search('CHRONOLOGICAL', url, re.IGNORECASE):
        return 0
    else:
        print("依照最新貼文排序")
        if url[-1:] == "/":
            target_url = url + "?sorting_setting=CHRONOLOGICAL"
            browser.get(target_url)
            return 0
        else:
            target_url = url + "/?sorting_setting=CHRONOLOGICAL"
            browser.get(target_url)
            return 0
        
def get_all_posts_in_page():
    return(browser.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']"))

def get_this_post():
    return(browser.find_element_by_xpath("//div[@class='_5pcr userContentWrapper']"))

def get_post_user_name(this_post):
    full_name_title = this_post.find_element_by_xpath(".//h5[@class='_7tae _14f3 _14f5 _5pbw _5vra']")
    return(full_name_title.find_element_by_xpath(".//span[contains(@class,'fwb')]").text)

def get_post_user_id(id_url):
    return str(re.search("id=(.+?)&", id_url).group(1))

def get_post_user_url(this_post):
    return str(this_post.find_element_by_xpath(".//a[contains(@class, '_5pb8')]").get_attribute("href"))

def get_post_datetime(this_post):
    date_time_span = this_post.find_element_by_xpath(".//span[@class='fsm fwn fcg']")
    return str(date_time_span.find_element_by_xpath(".//abbr").get_attribute("title"))

def get_post_time_epoch(this_post):
    date_time_span = this_post.find_element_by_xpath(".//span[@class='fsm fwn fcg']")
    return int(date_time_span.find_element_by_xpath(".//abbr").get_attribute("data-utime"))

def get_post_url(this_post):
    sub_url = this_post.find_element_by_xpath(".//div[@data-testid='post_message']//a[@class='see_more_link']").get_attribute("href")
    return str(sub_url)

def get_post_content(this_post):
    content_block = this_post.find_element_by_xpath(".//div[@data-testid='post_message']")
    return(content_block.text)

def get_post_like_num(this_post):
    try:
        like_block = this_post.find_element_by_xpath(".//div[@class='_66lg']").text
        return(int(re.sub("[^0-9]", "", like_block.split("其他",1)[0])))
    except:
        return 0

def get_post_comment_num(this_post):
    try:
        comment_block = this_post.find_element_by_xpath(".//a[@class='_3hg- _42ft']").text
        return(int(comment_block.replace('則留言', ' ')))
    except:
        return 0

def show_all_comments(this_post):
    to_click = this_post.find_elements_by_xpath(".//span[@class='_4sso _4ssp']")
    for click_each in to_click:
        try:
            click_each.click()    
        except:
            pass

    to_click = this_post.find_elements_by_xpath(".//a[@class='_4sxc _42ft']")
    for click_each in to_click:
        try:
            click_each.click()    
        except:
            pass

def get_comment_block_list(this_post):
    show_all_comments(this_post)
    try:
        all_comment_block = this_post.find_element_by_xpath(".//ul[@class='_7791']")
        comment_block_list = all_comment_block.find_elements_by_xpath(".//div[@class=' _6qw3']")
        if isinstance(comment_block_list, list):
            return(comment_block_list)
        else:
            return(list(comment_block_list))
    except:
        return("No_Comment")

def get_comment_user_name(each_comment_block):
    return(each_comment_block.find_element_by_xpath(".//a[@class='_6qw4']").text)

def get_comment_user_id(id_url):
    return id_url.split("id=",1)[1] 

def get_comment_user_url(each_comment_block):
    url = str(each_comment_block.find_element_by_xpath(".//a[@class='_6qw4']").get_attribute("href"))
    if "id=" in url: 
        return(url)
    else:
        url = str(each_comment_block.find_element_by_xpath(".//a[@class='_6qw4']").get_attribute("data-hovercard"))
        url = "https://www.facebook.com/profile.php?id=" + url.split("id=",1)[1]
        return(url)

def get_comment_content(each_comment_block):
    return(each_comment_block.find_element_by_xpath(".//span[@class='_3l3x']").text)

def check_directory(name):
    if not os.path.isdir(name):
        os.makedirs(name)
    return name

def validate_directory_name(name):
    name = name.replace("https://", "")
    name = name.replace("http://", "")
    name = name.replace("?", "")
    name = name.replace("/", "_")
    return(name)
    
path = os.getcwd()
df = pd.read_csv(path + '/dataset/fb_group_post.csv')
# Set first post
from_time = set_time()

#%%
for i in range(df.shape[0]):
    if df.iloc[i, 2] in ['Done!', 'Done! Not Yet Approved!']:
        continue

    # Set up chrome driver
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    url = "https://www.facebook.com"
    browser.get(url)

    # Create directory if not exist
    direc_name = '/FB_Post_' + validate_directory_name(str(df.iloc[i, 0])) + '_' + validate_directory_name(str(df.iloc[i, -1]))
    direc_name = check_directory(path + direc_name)
    
    # Login info
    if str(df.iloc[i, 3]) == 'X':
        if str(df.iloc[i, 0]) == 'public':
            account = ['s84053184@yahoo.com.tw','yabe0000']
        else:
            account = ['jamestan921@gmail.com','PUkai1101']
    else:
        account = df.iloc[i, 3].split(',')
        account = [str(account[0]), str(account[1])]
    
    # Login
    while True:
        try:
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'email')))
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'pass')))
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'loginbutton')))
            break
        except:
            continue
    browser.find_element_by_xpath("//input[@id='email']").send_keys(account[0])
    browser.find_element_by_xpath("//input[@id='pass']").send_keys(account[1])
    browser.find_element_by_xpath("//label[@id='loginbutton']").click()

    # Set target group
    target_url = df.iloc[i, 1]
    print('Now Getting ... ' + target_url)
    
    # To target group
    browser.get(target_url)

    # Check if is in a group
    approve_status = check_group_approved()
    print(approve_status)
    if approve_status == "未加入社團" or approve_status == "等待批准中":
        df.iloc[i, 2] = "Done! Not Yet Approved"
        browser.quit()
        continue

    # Sort posts
    sort_posts_by_time(target_url)

    # Browser loads at least one post in current page
    while True:
        try:
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, '_5pcr')))
            break
        except:
            continue

    # Scrolling down and get posts
    all_posts = get_all_posts_in_page()
    duplicate = 0
    while get_post_time_epoch(all_posts[-1]) > from_time:
        last_post = get_post_time_epoch(all_posts[-1])
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(3)
        all_posts = get_all_posts_in_page()
        new_post = get_post_time_epoch(all_posts[-1])
        print("Current post: " + str(new_post) + ", Target post: " + str(from_time))
        if last_post == new_post:
            duplicate += 1
            if duplicate >= 10:
                break
        else:
            duplicate = 0

    result = []
    all_posts_url = []
    for each_post in all_posts:
        try:
            each_post_url = get_post_url(each_post)
            if(((target_url + "/#") != each_post_url) and ((target_url + "#") != each_post_url) and (("sorting_setting" in each_post_url) == False)):
                all_posts_url.append(each_post_url)
                print("Getting post url: " + each_post_url)
        except:
            pass

    output_all_posts_url = pd.DataFrame(all_posts_url, columns=["PostUrl"])
    filename = os.path.join(direc_name, (validate_directory_name(str(df.iloc[i, 1])) + "$$All_Posts_Url.csv"))
    output_all_posts_url.to_csv(filename, sep=',', encoding='utf-8', index=False)

    for each_post_url in all_posts_url:
        browser.get(each_post_url)
        print("Getting information from post url: " + each_post_url)
        while True:
            try:
                element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, '_5pcr')))
                break
            except:
                continue
        this_post = get_this_post()
        # 以下七項為"貼文資訊"
        # 1. 發文用戶名稱
        post_user_name = get_post_user_name(this_post)
        # 2. 發文用戶連結
        post_user_url = get_post_user_url(this_post)
        # 3. 發文用戶ID
        post_user_id = get_post_user_id(post_user_url)
        # 4. 發佈貼文時間
        post_date_time = get_post_datetime(this_post)
        post_time_epoch = get_post_time_epoch(this_post)
        # 5. 貼文內文
        post_content = get_post_content(this_post)
        # 6. 貼文讚數
        like_count = get_post_like_num(this_post)
        # 7. 貼文留言數
        comment_count = get_post_comment_num(this_post)
        comment_list = get_comment_block_list(this_post)
        # 貼文沒有任何留言
        if comment_list == "No_Comment":
            post_info = {
                "PostUserName": post_user_name,
                "PostUserId": post_user_id,
                "PostUserUrl": post_user_url,
                "PostDateTime": post_date_time,
                "PostTimeEpoch": post_time_epoch,
                "PostContent": post_content,
                "LikeCount": like_count,
                "CommentCount": comment_count
            }
            result.append(post_info)
        # 貼文至少有一則留言
        else:
            comment_user_name_list = []
            comment_user_url_list = []
            comment_user_id_list = []
            comment_content_list = []
            for each_comment in comment_list:
                try:
                    # 以下四項為"留言資訊""
                    # 1. 留言用戶名稱
                    comment_user_name = get_comment_user_name(each_comment)
                    # 2. 留言用戶連結
                    comment_user_url = get_comment_user_url(each_comment)
                    # 3. 留言用戶ID
                    comment_user_id = get_comment_user_id(comment_user_url)
                    # 4. 留言內容
                    comment_content = get_comment_content(each_comment)

                    comment_user_name_list.append(comment_user_name)
                    comment_user_url_list.append(comment_user_url)
                    comment_user_id_list.append(comment_user_id)
                    comment_content_list.append(comment_content)
                except:
                    continue

            post_info = {
                "PostUserName": post_user_name,
                "PostUserId": post_user_id,
                "PostUserUrl": post_user_url,
                "PostDateTime": post_date_time,
                "PostTimeEpoch": post_time_epoch,
                "PostContent": post_content,
                "LikeCount": like_count,
                "CommentCount": comment_count,
                "CommentUserName": comment_user_name_list,
                "CommentUserId": comment_user_id_list,
                "CommentUserUrl": comment_user_url_list,
                "CommentContent": comment_content_list
            }
            result.append(post_info)

        # 每完成一篇貼文的搜尋存檔一次
        output_data = pd.DataFrame(result)
        filename = os.path.join(direc_name, (validate_directory_name(str(df.iloc[i, 1])) + "$$All_Posts_With_Comments.csv"))      
        output_data.to_csv(filename, sep=',', encoding='utf_8_sig', index=False)
        sleep(3)

    # output_data = pd.DataFrame(result)
    # filename = os.path.join(direc_name, "All_Posts_With_Comments.csv")
    # output_data.to_csv(filename, sep=',', encoding='utf_8_sig', index=False)
    df.iloc[i, 2] = "Done!"
    df.to_csv("./dataset/fb_group_post.csv", sep=',', encoding='utf_8_sig', index=False)
    browser.quit()
