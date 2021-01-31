"""
华东理工大学信息门户>抗疫服务>返校前健康日报>自动打卡

【除python外的其他软件】
需要用到谷歌浏览器, 以及浏览器相应的版本驱动

查看谷歌浏览器版本：谷歌浏览器->设置->关于Chrome
谷歌浏览器镜像下载网站: http://npm.taobao.org/mirrors/chromedriver/

驱动放置：
1.将驱动放到python安装目录下的Script目录下, 并且复制一份到谷歌浏览器的安装目录下
2.将驱动放到该脚本同一目录下
; 其实就是python解释器能通过环境变量找到的目录
; 亦可以使用火狐浏览器, 但也要下载相应版本的驱动, 如上

【配置文件】
在同一目录下下创建'config.ini'文件，格式如下：
```
[SafetyJournal]
username=用户名
password=密码
province=省
city=市
address=地址
temperature=体温
```
; 学号 密码 为必填项目
; 非必要项填不填或错会填写默认值
; 默认编码 utf8

注意：
1. 若是其他目录，但是请注意路径
"""
import time
from selenium import webdriver
import configparser
import traceback


class SafetyJournal:
    not_null_colname = ['username', 'password']  # 必填项目
    null_colname = {'province': '四川省', 'city': '泸州市',
                    'address': '家', 'temperature': '37'}  # 非必填项目
    login_url = 'https://sso.ecust.edu.cn/authserver/login'
    submit_url = 'http://workflow.ecust.edu.cn/default/work/uust/xxfxqxxtb/xxfxqxxtbqz.jsp'
    delayTime = 2  # 每次打开网页的间隔时间(单位: 秒), 如果网络状况不好请加长
    minDelayTime = 0.001  # 每次操作的间隔时间(单位: 秒), 如果网络状况不好请加长

    def __init__(self, *args, **kwargs):
        """
        方法一：`sj = SafetyJournal(config=路径)`

        建议在同一目录下下创建`config.ini`文件，格式如下：
        ```
        [SafetyJournal]
        username=用户名
        password=密码
        province=省
        city=市
        address=地址
        temperature=体温
        ; 学号 密码 为必填项目
        ; 非必要项填不填或错会填写默认值
        ; 默认编码 utf8
        ```
        注意：
        1. 若是其他目录，但是请注意路径

        ----

        方法二：`sj = SafetyJournal(username=用户名,...)`

        在程序SafetyJournal对象的创建中直接添加参数
        """
        if kwargs.get('config'):
            try:
                cp = configparser.ConfigParser()
                cp.read(kwargs['config'], encoding=kwargs['encoding']
                        if kwargs.get('encoding') else "utf8")
                for i in self.not_null_colname:
                    self.__dict__[i] = cp.get("SafetyJournal", i)  # 完全不填写会报错
                    # 填写空字符报错 bool('') == bool(None) == False
                    if not self.__dict__[i]:
                        raise KeyError(i)
                for i in self.null_colname:
                    try:
                        self.__dict__[i] = cp.get("SafetyJournal", i)
                        # 填写空字符/空报错 bool('') == bool(None) == False
                        if not self.__dict__[i]:
                            raise KeyError(i)
                    except:
                        self.__dict__[i] = self.null_colname[i]
            except configparser.Error as e:
                # traceback.print_exc()
                raise e
            except KeyError as e:
                # traceback.print_exc()
                raise e
        else:
            try:
                for i in self.not_null_colname:
                    self.__dict__[i] = kwargs[i]
                    # 填写空字符/空报错 bool('') == bool(None) == False
                    if not self.__dict__[i]:
                        raise KeyError(i)
                for i in self.null_colname:
                    try:
                        self.__dict__[i] = kwargs[i]
                        # 填写空字符/空报错 bool('') == bool(None) == False
                        if not self.__dict__[i]:
                            raise KeyError(i)
                    except:
                        self.__dict__[i] = self.null_colname[i]
            except KeyError as e:
                # traceback.print_exc()
                raise e

        print(*[self.__dict__[i] for i in self.not_null_colname],
              *[self.__dict__[i] for i in self.null_colname])

    def login(self):
        """
        打开"华东理工大学统一身份认证网站", 有可能已登录,导致无法找到输入框

        若报错则默认已登录
        """
        self.driver = webdriver.Chrome()  # 这里的路径是你的谷歌驱动程序所放置的路径(需要设置)
        self.driver.get(self.login_url)
        print('打开网站')
        time.sleep(self.delayTime)
        try:
            login_input = self.driver.find_element_by_xpath(
                "//input[@placeholder='用户名']")  # 利用xpath选中text用户框
            login_input.send_keys(self.username)
            time.sleep(self.minDelayTime)

            pw_input = self.driver.find_element_by_xpath(
                "//input[@placeholder='密码']")  # 利用xpath选中text密码框
            pw_input.send_keys(self.password)
            time.sleep(self.minDelayTime)

            self.driver.find_element_by_xpath(
                "//button[contains(@class,'auth_login_btn primary full_width')]").click()  # 登录

            print('提交网站')
            time.sleep(self.delayTime)
        except:
            pass  # 默认已登录

    def submit(self) -> bool:
        self.driver.get(self.submit_url)
        print('打开网站')
        time.sleep(self.delayTime)

        self.driver.find_element_by_xpath(
            "//ins[@class='iCheck-helper']").click()  # 个人承诺
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath(
            "//button[text()='下一步']").click()  # 登录
        print('打开网站')
        time.sleep(self.delayTime)

        self.driver.find_element_by_xpath(
            '//*[@id="radio_xszd7"]/div/ins').click()  # 在上海及其他省市
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath("//div[@name='jgshen']").click() # 省
        self.driver.find_element_by_xpath(
            "//li[contains(@id, 'select2-select_jgshen-result') and contains(@id, '{}')]".format(self.province)).click()
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath("//div[@name='jgshi']").click() # 市
        self.driver.find_element_by_xpath(
            "//li[contains(@id, 'select2-select_jgshi-result') and contains(@id, '{}')]".format(self.city)).click()
        time.sleep(self.minDelayTime)

        address_input = self.driver.find_element_by_xpath(
            '//*[@id="input_jgjtdzinput"]') # 地址
        address_input.send_keys(self.address)
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath(
            '//*[@id="radio_jkzk19"]/div/ins').click()  # 健康
        time.sleep(self.minDelayTime)

        temperature_input = self.driver.find_element_by_xpath(
            "//input[@placeholder='请填写体温']")  # 输入度数
        temperature_input.send_keys(self.temperature)
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath(
            '//*[@id="radio_sfyyxqk37"]/div/ins').click()  # 是否有以下情况
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath(
            '//*[@id="radio_jkmsflm15"]/div/ins').click() # 健康码是否绿码
            
        self.driver.find_element_by_xpath('//*[@id="post"]').click()  # 提交
        time.sleep(self.minDelayTime)

        self.driver.find_element_by_xpath(
            '//a[text()="确定"]').click()  # 确认提交无误
        time.sleep(self.delayTime)

        success = self.driver.find_elements_by_xpath('//*[@id="layui-layer2"]/div[text()="提交成功！"]')
        
        self.driver.quit()  # 关闭浏览器`

        return bool(success)


def main() -> bool:
    sj = SafetyJournal(config='./config.ini', encoding="utf8")
    sj.login()
    return sj.submit()


if __name__ == '__main__':
    main()