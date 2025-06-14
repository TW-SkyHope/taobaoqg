from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def precise_wait(target_time):
    """精确等待到目标时间
    Args:
        target_time (datetime): 需要等待到的目标时间
    """
    while True:
        current_time = datetime.now()
        if current_time >= target_time:
            break
        time.sleep(0.001)  # 毫秒级精度检查

def taobao_flash_sale(target_url):
    """淘宝抢购主函数
    Args:
        target_url (str): 淘宝抢购页面URL
    """
    # 设置抢购时间：2025年6月14日17点59分59秒600毫秒
    sale_time = datetime(2025, 6, 14, 17, 59, 59, 600000)
    
    # 初始化浏览器驱动
    driver_path = "msedgedriver.exe"  # Edge浏览器驱动路径
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)

    try:
        # 打开淘宝登录页面
        driver.get(target_url)
        print(f"[{datetime.now()}] 成功打开淘宝登录页面")

        # 等待用户手动登录
        input("请先完成淘宝登录，登录后按回车键继续...")

        # 记录当前页面URL（用于后续判断是否跳转）
        original_url = driver.current_url
        print(f"当前页面URL: {original_url}")

        # 等待到抢购时间
        print(f"正在等待抢购时间: {sale_time}")
        precise_wait(sale_time)
        print(f"[{datetime.now()}] 开始执行抢购操作")

        # 定位并点击抢购按钮
        buy_buttons = driver.find_elements(By.CSS_SELECTOR, '.btn--QDjHtErD')
        if not buy_buttons:
            raise Exception("未找到抢购按钮")
        
        buy_buttons[0].click()
        print(f"[{datetime.now()}] 已点击抢购按钮")

        # 等待页面跳转到订单确认页
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.current_url != original_url
            )
            print(f"跳转后URL: {driver.current_url}")
        except:
            raise Exception("页面跳转超时，可能抢购失败")

        # 定位并点击确认订单按钮
        try:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".btn--QDjHtErD"))
            )
            confirm_button.click()
            print(f"[{datetime.now()}] 已提交订单")
        except:
            raise Exception("确认订单超时")

        print("抢购流程完成！")
        input("按回车键关闭浏览器...")

    except Exception as e:
        print(f"抢购过程中出现错误: {str(e)}")
    finally:
        driver.quit()  # 确保浏览器被关闭

if __name__ == "__main__":
    # 淘宝登录页面URL
    login_url = "https://login.taobao.com/havanaone/login/login.htm"
    taobao_flash_sale(login_url)