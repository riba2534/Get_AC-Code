import requests
from bs4 import BeautifulSoup
import lxml
CookieID = '10p8enos6apene2r0uhc1hre37'  # 全局cookie
username = '你的账号'
password = '你的密码'


def get_problem_list():  # 获取需要爬取的题号列表
    r = requests.get('http://acm.hdu.edu.cn/userstatus.php?user='+username)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    namelist = soup.findAll('p', {'align': 'left'})[0]  # 找到对应区域
    namelist = namelist.get_text().split(';')  # 按照分号切片
    problem_list = []
    for name in namelist:
        id = name[2:6]
        problem_list.append(id)
    return problem_list


def get_page_id(id):  # 利用题目号码，来获取代码页面号码
    id = str(id)
    r = requests.get(
        'http://acm.hdu.edu.cn/status.php?user='+username+'&pid='+id+'&status=5')
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    # 这些代码也可以找到，不过很繁杂
    # table_text = soup.find('table', {'class': 'table_text'})
    # for child in table_text.children:
    #     print(child)
    #     print('---------------')
    #     print(child.find)
    #     for cc in child.children:
    #         print(cc)
    table_text = soup.findAll('td', {'height': '22px'})
    page_id = ''
    for name in table_text:
        page_id = name.get_text()
        flag = False
        for sb in name.next_siblings:
            # print(sb.get_text())
            if sb.get_text() == 'G++' or sb.get_text() == 'C++':
                flag = True
        if flag == True:
            break
    return page_id


def get_ac_code(page_id, problem_id):  # 获取题目的ac代码，传入页面地址和题目编号
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=' + CookieID,
        'Host': 'acm.hdu.edu.cn',
        'Referer': 'http://acm.hdu.edu.cn/status.php?user='+username+'&pid='+problem_id+'&status=5',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    r = s.get('http://acm.hdu.edu.cn/viewcode.php?rid=' +
              page_id, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    usercode = soup.findAll('textarea', {'id': 'usercode'})[0]
    code = usercode.get_text()
    return code


def save_code(ac_code, problem_id):  # 利用题目编号命名，ac代码写入文件
    if os.path.exists('HDU-code') == False:
        os.mkdir('HDU-code')
    with open('HDU-code/'+problem_id+'.cpp', 'w') as f:
        f.write(ac_code)


def run():  # 主功能实现逻辑
    problem_list = get_problem_list()  # 获取ac题目列表
    print('题目列表获取成功!')
    cnt = 0
    for problem_id in problem_list:
        cnt += 1
        page_id = get_page_id(problem_id)
        ac_code = get_ac_code(page_id, problem_id)
        save_code(ac_code, problem_id)
        print('已经处理了 '+str(cnt)+' 道题目，当前成功保存:'+problem_id)


if __name__ == '__main__':
    post_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'  # 登录的post提交地址
    data = {
        'username': username,
        'userpass': password,
        'login': 'Sign In'
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '50',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=' + CookieID,
        'Host': 'acm.hdu.edu.cn',
        'Origin': 'http://acm.hdu.edu.cn',
        'Referer': 'http://acm.hdu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
        global s
        s = requests.Session()  # 用来维持cookie
        r = s.post(post_url, data=data, headers=headers)
        html = r.text
        if (html.find('No such user or wrong password.') != -1):
            print('用户名或密码错误')
            exit()
        else:
            print('登陆成功')
            #CookieID = r.cookies['PHPSESSID']
            # print('cookie='+CookieID)
    except:
        print('运行出错了')
        exit()
    run()
