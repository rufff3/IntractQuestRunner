import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
def load_cookies_from_file(file_path):
    
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            raw_content = file.read()
        
        cleaned_content = raw_content.replace('\n', '').replace(' ', '')
        separated_accounts = cleaned_content.replace("][", "]\n[")
        account_blocks = separated_accounts.split("\n")
        
        cookies_list = []
        for block in account_blocks:
            if block:
                cookies_list.append(json.loads(block))
        
        return cookies_list
    except Exception as e:
        print(f"❌ Gagal membaca atau parsing file cookies: {e}")
        return []
def inject_cookies(driver, cookies):
    driver.get("https://quest.intract.io")
    time.sleep(1)
    for cookie in cookies:
        if "sameSite" in cookie and cookie["sameSite"] is not None:
            if cookie["sameSite"].lower() == "no_restriction": cookie["sameSite"] = "None"
            elif cookie["sameSite"].lower() == "unspecified": cookie.pop("sameSite")
        if all(k in cookie for k in ("name", "value")):
            try: driver.add_cookie(cookie)
            except Exception:
                if 'domain' in cookie: cookie.pop('domain')
                try: driver.add_cookie(cookie)
                except Exception as e2: print(f"⚠️ Gagal menambahkan cookie: {cookie.get('name')} ({e2})")
    print("✅ Cookies berhasil ditambahkan.")
def setup_driver():

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
def safe_click(driver, element):
    
    try:
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(f"    -> Gagal klik via JavaScript: {e}")
        raise e
def shortcut_verification(driver, see_more_selector):
    print("\n--- Memulai Mode Verifikasi Jalan Pintas ---")
    
    time.sleep(3)
    try:
        see_more_buttons = driver.find_elements(By.CSS_SELECTOR, see_more_selector)
        if see_more_buttons:
            print(f"🔍 Ditemukan {len(see_more_buttons)} tombol 'See More', mengklik...")
            for button in see_more_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                    safe_click(driver, button)
                except Exception:
                    continue
            print("✅ Semua tombol 'See More' telah diklik.")
            time.sleep(2)
        else:
            print("🟡 Tombol 'See More' tidak ditemukan.")
    except Exception:
        print("🟡 Tombol 'See More' tidak ditemukan.")
    print("\n🔍 Memborong semua tombol 'Verify' di halaman ini...")
    try:
        verify_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Verify')]")
        if verify_buttons:
            count = 0
            for button in verify_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(0.5)
                    safe_click(driver, button)
                    count += 1
                except Exception:
                    continue
            print(f"✅ Total {count} tombol 'Verify' berhasil diklik.")
        else:
            print("🟡 Tidak ada tombol 'Verify' yang ditemukan di halaman ini.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mencari tombol 'Verify': {e}")
def main():
    print("==============================================")
    print("   Selamat Datang di Script Automasi Quest")
    print("==============================================")
    print("\nMasukkan link-link quest yang ingin dikerjakan.")
    print("Tekan ENTER setelah setiap link.")
    print("Ketik 'selesai' atau 'start' lalu tekan ENTER jika sudah semua.")
    QUEST_LINKS = []
    while True:
        link = input("> ")
        if link.lower() in ['selesai', 'start', 'done']:
            break
        if link.startswith('http'):
            QUEST_LINKS.append(link)
        elif link:
            print("(Input tidak valid, bukan link. Silakan coba lagi atau ketik 'selesai'.)")
    if not QUEST_LINKS:
        print("Tidak ada link yang dimasukkan. Program berhenti.")
        return
    print(f"\n✅ Siap mengerjakan {len(QUEST_LINKS)} link...")
    time.sleep(2)
    SEE_MORE_SELECTOR = "button._see_more_button_uw4u6_62"
    cookies_file = 'cookiesintract.txt'
    all_accounts = load_cookies_from_file(cookies_file)
    if not all_accounts: return
    for i, cookies_for_one_account in enumerate(all_accounts):
        print(f"\n🚀 Memproses Akun ke-{i+1} dari {len(all_accounts)}...")
        driver = None
        try:
            driver = setup_driver()
            inject_cookies(driver, cookies_for_one_account)
            
            for index, link in enumerate(QUEST_LINKS):
                print(f"\n🔗 Mengerjakan Link #{index+1}: {link[:70]}...")
                driver.get(link)
                
                shortcut_verification(driver, SEE_MORE_SELECTOR)

            print("\n🎉 Semua link untuk akun ini telah selesai diproses.")

        except Exception as e:
            print(f"❌ Terjadi error fatal pada akun ke-{i+1}: {e}")
            if driver: driver.save_screenshot("fatal_error.png")
        finally:
            if driver:
                print("✅ Menutup browser, jeda 10 detik sebelum lanjut ke akun berikutnya...")
                time.sleep(10) 
                driver.quit()
            print(f"--- Selesai Akun ke-{i+1} ---")

if __name__ == '__main__':
    main()
