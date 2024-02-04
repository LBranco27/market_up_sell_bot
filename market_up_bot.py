from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys
import os
import random

if len(sys.argv) < 5:
    print("usage: python market_up_bot.py <number of sells> <login> <password> <store name> <user_data_folder>")
    print("using a existent user_data_folder is useful for keeping extensions while this program is running. Such as ublock.")
    print("names in names.txt / services in services.txt / products in products.txt")
    sys.exit(1)

# check if files present
dir = os.path.dirname(os.path.realpath(__file__))
name_file = os.path.join(dir, "names.txt")
services_file = os.path.join(dir, "services.txt")
products_file = os.path.join(dir, "products.txt")
print(dir)
if not os.path.exists(name_file):
    print("missing file: names.txt")
    sys.exit(4)
if not os.path.exists(services_file):
    print("missing file: services.txt")
    sys.exit(5)
if not os.path.exists(products_file):
    print("missing file: products.txt")
    sys.exit(6)

# open files
with open('names.txt', 'r') as file:
    names = file.readlines()
names = [linha.strip() for linha in names]
with open('services.txt', 'r') as file:
    services = file.readlines()
services = [linha.strip() for linha in services]
with open('products.txt', 'r') as file:
    products = file.readlines()
products = [linha.strip() for linha in products]

products_services = services + products

# check if empty
if not names:
    print("missing names")
    sys.exit(2)
if not products_services:
    print("missing products or services")
    sys.exit(3)

arg_number = sys.argv[1]
login = sys.argv[2]
password = sys.argv[3]
address = sys.argv[4]
user_data = sys.argv[5]

if user_data:
    options = Options()
    options.add_argument("user-data-dir=" + user_data)
# change to Firefox if you want to use gecko
    driver = webdriver.Chrome(options=options)

else:
    driver = webdriver.Chrome()

driver.get("https://" + address + ".marketup.com/index.html#/login")

time.sleep(5)

login_name = driver.find_element_by_id("login§ds_login")
login_name.send_keys(login)

password_input = driver.find_element_by_id("login§ds_password")
password_input.send_keys(password)

login_button = driver.find_element_by_id("login§bt_login")
login_button.click()

time.sleep(8)

for i in range(int(arg_number)):

    stupid_cookies_window = driver.find_element_by_class_name("banner-lgpd-consent.banner-lgpd-consent-show")
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", stupid_cookies_window)

    driver.get("https://" + address + ".marketup.com/index.html#/sale_order/new")

    time.sleep(6)
    stupid_unknown_div = driver.find_element_by_class_name("ads-free-wrapper.ng-scope")
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", stupid_unknown_div)
    name_input = driver.find_element_by_name("clientName")
    name_input.send_keys(random.choice(names))
    time.sleep(3)

    try:
        suggestion_name = driver.find_element(By.CLASS_NAME, 'uib-typeahead-match.ng-scope.active')
        suggestion_name.click()
    except NoSuchElementException as e:
        new_client_button = driver.find_element(By.CLASS_NAME, 'btn.btn-block.bt-new-client.ng-scope')
        new_client_button.click()
        print("new client")
    except Exception as e:
        print("unknown error!" + e)

    time.sleep(2)

    address_text = driver.find_element_by_xpath("//*[text()=' para informar o endereço depois']")
    address_text.click()

    item_number = random.randint(2, 4)
    for i in range(item_number):
        item_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[typeahead-on-select*='controller.setItem($item)']")))
        item_input.send_keys(random.choice(products_services))
        time.sleep(4)

        suggestion_item = driver.find_element(By.CLASS_NAME, "uib-typeahead-match.ng-scope.active")
        suggestion_item.click()
        time.sleep(3)

        suggestion_item = driver.find_element(By.CLASS_NAME, "glyphicon.glyphicon-plus-sign")
        random_item_qtd = random.randint(1, 4)
        for j in range(random_item_qtd):
            suggestion_item.click()

        add_item_button = driver.find_element(By.CLASS_NAME, "bt-add-item")
        add_item_button.click()
        time.sleep(1)
    
    payment_type = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select[ng-change*='controller.paymentTypeChange()']")))
    select = Select(payment_type)
    select.select_by_visible_text('DINHEIRO')

    time.sleep(2)
    create_accounts = driver.find_element_by_id("sale_order_new_gerar_contas")
    create_accounts.click()

    time.sleep(2)
    finish_sell = driver.find_element_by_id("sale_order_new_concluir_venda")
    finish_sell.click()

    time.sleep(5)
    ok = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[ng-click*='controller.close()']")))
    while 1:
        try:
            ok.click()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            continue

    time.sleep(1)
    deliver = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[ng-click*='controller.showDeliveryModal()']")))
    if deliver.get_attribute("disabled") == "disabled":
        print("only services")
    else:
        deliver.click()

        time.sleep(2)
        finish_deliver = driver.find_element_by_id("sale_order_detail_entregar_pedido")
        finish_deliver.click()

        time.sleep(6)
        ok = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[ng-click*='controller.close()']")))
        ok.click()

    stupid_unknown_div = driver.find_element_by_class_name("ads-free-wrapper.ng-scope")
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", stupid_unknown_div)

    receive = driver.find_element_by_xpath("//*[contains(text(), 'RECEBER')]")
    ActionChains(driver).move_to_element(receive).perform()
    time.sleep(1)
    receive.click()

    time.sleep(5)

    money_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[ng-model='controller.currentEntryEvent.Value']")))
    try:
        money_input.click()
    except Exception as e:
        print(e + "not clickable")
        money_input.send_keys("q")

    account_type = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select[ng-model*='controller.currentEntryEvent.Entry.Account']")))
    select = Select(account_type)
    select.select_by_visible_text('Caixa')

    receive_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary.btn-block.bt-confirm.ng-scope")
    receive_button.click()

    finish_receive = driver.find_element_by_id("receivable_new_pagar_receber")
    finish_receive.click()

    time.sleep(6)
    ok = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[ng-click*='controller.close()']")))
    ok.click()

# driver.quit()
