import requests
from bs4 import BeautifulSoup
import lxml
import re
import os
CookieID = '9dndfb0mdslimr29k456v7k7r2'  # 全局cookie
username = '你的用户名'
password = '你的密码'


def get_problem_list():  # 获取需要爬取的题号列表
    r = requests.get(
        'http://acm.nyist.edu.cn/JudgeOnline/profile.php?userid='+username)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    html = soup.findAll('li', {'style': 'display:inline'})
    pattern = r'\d+'
    code_list = []
    for name in html:
        text = re.findall(pattern, str(name))[0]
        if text == '3':  # 我的代码3是"正在攻克的“，所以在这里停止
            break
        else:
            code_list.append(text)
    return code_list


def get_page_id(id):  # 利用题目号码，来获取代码页面号码
    r = requests.get('http://acm.nyist.edu.cn/JudgeOnline/status.php?do=search&pid=' +
                     id+'&userid='+username+'&language=C%2FC%2B%2B&result=Accepted')
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('td')
    pattern = r'<td>\d+</td>'
    for name in text:
        jg = re.findall(pattern, str(name))
        if len(jg) > 0:
            return jg[0][4:-5]
      #  print(name, ))


def get_ac_code(page_id, problem_id):  # 获取题目的ac代码，传入页面地址和题目编号
    headers = {
        'Cookie': 'PHPSESSID='+CookieID,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    r = s.get('http://acm.nyist.edu.cn/JudgeOnline/code.php?runid=' +
              page_id, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('pre', {'class': r'brush: cpp; '})
    return text[0].get_text()


def save_code(ac_code, problem_id):  # 利用题目编号命名，ac代码写入文件
    if os.path.exists('NYOJ-Code') == False:
        os.mkdir('NYOJ-Code')
    with open('NYOJ-Code/'+problem_id+'.cpp', 'w') as f:
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
    post_url = 'http://acm.nyist.edu.cn/JudgeOnline/dologin.php?url=http%3A%2F%2Facm.nyist.edu.cn%2FJudgeOnline%2Fproblemset.php'  # 登录的post提交地址
    data = {
        'userid': username,
        'password': password,
        'btn_submit': '登录',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '64',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID='+CookieID,
        'Host': 'acm.nyist.edu.cn',
        'Origin': 'http://acm.nyist.edu.cn',
        'Referer': 'http://acm.nyist.edu.cn/JudgeOnline/login.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    global s
    s = requests.session()
    r = s.post(post_url, data=data, headers=headers)
    r.encoding = r.apparent_encoding
    run()
