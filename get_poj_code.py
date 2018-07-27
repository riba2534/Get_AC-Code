import requests
from bs4 import BeautifulSoup
import lxml
import re
import os
CookieID = '39926B677E07DD9CF0B08AA2ABCC7F63'  # 全局cookie
username = '你的账号'
password = '你的密码'


def get_problem_list():  # 获取需要爬取的题号列表
    r = requests.get('http://poj.org/userstatus?user_id='+username)
    soup = BeautifulSoup(r.text, 'lxml')
    html = soup.findAll('script', {'type': 'text/javascript'})[0]
    name_str = html.get_text().split()
    name_list = []
    for name in name_str:
        if(len(name) == 7):
            name_list.append(name[2:-1])
            # print(name,name[2:-1])
    name_list.remove('1000')
    return name_list


def get_page_id(id):  # 利用题目号码，来获取代码页面号码
    r = requests.get('http://poj.org/status?problem_id='+id +
                     '&user_id='+username+'&result=0&language=')
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.findAll('td')
    pattern = r'<td>\d+</td>'
    for name in text:
        jg = re.findall(pattern, str(name))
        if len(jg) > 0:
            return jg[0][4:-5]


def get_ac_code(page_id, problem_id):  # 获取题目的ac代码，传入页面地址和题目编号
    #print(page_id, problem_id)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID='+CookieID,
        'Host': 'poj.org',
        'Referer': 'http://poj.org/status?problem_id='+problem_id+'&user_id='+username+'&result=0&language=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    r = s.get('http://poj.org/showsource?solution_id=' +
              page_id, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())
    # a = input('1111111')
    pre = soup.find_all('pre', {'class': 'sh_cpp'})[0]
    code = pre.get_text()
    return code


def save_code(ac_code, problem_id):  # 利用题目编号命名，ac代码写入文件
    if os.path.exists('POJ') == False:
        os.mkdir('POJ')
    with open('POJ/'+problem_id+'.cpp', 'w') as f:
        f.write(ac_code)


def run():  # 主功能实现逻辑
    problem_list = get_problem_list()  # 获取ac题目列表
    print('题目列表获取成功!,一共{}道题目'.format(len(problem_list)))
    cnt = 0
    for problem_id in problem_list:
        cnt += 1
        page_id = get_page_id(problem_id)
        ac_code = get_ac_code(page_id, problem_id)
        save_code(ac_code, problem_id)
        print('已经处理了 '+str(cnt)+' 道题目，当前成功保存:'+problem_id)


if __name__ == '__main__':
    post_url = 'http://poj.org/login'  # 登录的post提交地址
    data = {
        'user_id1': username,
        'password1': password,
        'B1': 'login',
        'url': '/'
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID='+CookieID,
        'Host': 'poj.org',
        'Origin': 'http://poj.org',
        'Referer': 'http://poj.org/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    global s
    s = requests.session()
    r = s.post(post_url, data=data, headers=headers)
    print('登录成功!')
    run()
