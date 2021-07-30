#-*- coding:utf-8 -*-
# author: Anefuer_kpl
# Email: 374774222@qq.com
# datatime: 2021-07-29 16:48
# project: 爬虫学习

'''
Task: 使用selenium爬取pixiv，浏览器右键后按键盘的y 进行图片的复制，其他方式都会被pixiv服务器阻止
'''

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains  # 模拟鼠标操作，双击 右击 拖动等操作
from selenium.webdriver.support.wait import WebDriverWait as WDW # 加入 显示等待，只要检测到的元素被加载出来了，就进行下一步
import pyautogui, pyperclip  # pyautogui模拟鼠标的移动操作, pyperclip模拟电脑剪切板
import time
import os


def check_dir(dir):
    # 检测是否含有对应文件夹，没有则创建一个
    if not os.path.exists(dir):
        os.mkdir(dir)

def sign_in(id, code):
    # 实现登录
    # opt = Options()
    # opt.add_argument('--headless')  # 设置后端运行,不显示页面
    # opt.add_argument('--disable-gpu')
    # web = Chrome(options=opt)
    web = Chrome()
    actions = ActionChains(web)  # 创建鼠标动作实例
    web.get('https://www.pixiv.net/')

    # =============================1.进行登录===========================
    # 找到登录按钮并点击
    # 显示等待，WDW(web, 10, 0.5)参数分别为 浏览器驱动，最长等待间隔，扫描间隔
    # 匿名函数返回值为True时才执行下一步，说明对应元素被加载出来了， notwait为返回值，该命名方式自己随便定义
    # WDW(web, 10, 0.5).until(lambda notwait: web.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/a[2]'))
    web.implicitly_wait(20)
    web.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/a[2]').click()
    # 找到账号和密码输入框,并输入账号和密码
    web.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input').send_keys(id)
    web.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input').send_keys(code)
    # 再次点击登录按钮完成登录
    # WDW(web, 10, 0.5).until(lambda notwait: web.find_element_by_xpath('//*[@id="LoginComponent"]/form/button'))
    web.implicitly_wait(20)
    web.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').click()
    # ============================= end ==============================
    print('Have signed in Successfully!')
    return web, actions

def search(web, actions):
    # 检索图片
    # =============================2.检索图片===========================
    inp = input('Search whatever you want:')
    # inp = '美女'
    # 输入检索的内容，并按回车发起检索
    WDW(web, 10, 1).until(lambda notwait: web.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/form/div/input'))
    web.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/form/div/input').send_keys(inp, Keys.ENTER)
    # 获取检索到的图片列表
    # WDW(web, 10, 0.5).until(lambda notwait: web.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/div[5]/div/section[2]/div[2]/ul/li'))
    web.implicitly_wait(20)  # 等待整个页面加载完毕
    img_list = web.find_elements_by_xpath('//*[@id="root"]/div[2]/div[2]/div/div[5]/div/section[2]/div[2]/ul/li')

    check_dir('./image')
    for img in img_list:
        WDW(web, 10, 0.5).until(lambda notwait: img.find_element_by_xpath('./div/div[2]/a'))
        pic_name = img.find_element_by_xpath('./div/div[2]/a').text
        print(pic_name)
        # PS: 这里改成你自己的文件夹路径
        pic_saved_path = os.path.join('E:/Pycharm/爬虫学习/爬虫实战/pixiv/image', pic_name) # 从当前xpath向后接着找,找到图片名, 并拼接图片保存的路径，需要是绝对路径
        # img.click() # 点击图片的缩略图进入详细页面
        actions.context_click(img).perform() # 右键在新标签页打开图片详细页
        pyautogui.typewrite(['down', 'enter'])  # 进入新标签页
        web.switch_to.window(web.window_handles[-1]) # 切换到新标签页

        WDW(web, 10, 0.5).until(lambda notwait: web.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/div[1]/main/section/div[1]/div/figure/div/div[1]/div/a/img'))
        web.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/div[1]/main/section/div[1]/div/figure/div/div[1]/div/a/img').click() #点击页面内图片，获取高清图片
        web.implicitly_wait(20) # 设置隐式等待，直到整个页面的所有元素都被加载完毕，才继续执行下一步

        bigger_img = web.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/img')  # 定位大图
        actions.move_to_element(bigger_img)  # 将鼠标移动到图片处
        actions.context_click(bigger_img).perform()  # perform表示取执行该操作
        pyautogui.typewrite(['v'])  # 快捷键v，图片另存为
        time.sleep(1) # 网络延迟 等待1s

        pyperclip.copy(pic_saved_path) # 将图片路径复制到剪切板
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')  # 模拟电脑热键 ctrl+v 进行粘贴
        pyautogui.press('enter') # 输入回车
        time.sleep(2)

        print(f'Picture {pic_name} has been downloaded!')

        web.close()  # 下载完毕后关闭当前页面
        web.switch_to.window(web.window_handles[0]) # 重新切换回第一个页面


if __name__ == '__main__':
    #========个人账号===========
    id = ''
    code = ''
    #=========================
    web,actions = sign_in(id, code)
    search(web, actions)