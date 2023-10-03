from selenium.webdriver.common.by import By
from config import app_url
from time import sleep
from Main import *
from DatabaseInjector import *
from selenium.common.exceptions import TimeoutException


def login(driver, username):
    driver.get(app_url + '/logout')
    sleep(3)
    driver.get(app_url)
    webdriver_wait(driver, 30, (By.CSS_SELECTOR, 'input[name="username"]')).send_keys(username)
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, 'input[name="password"]')).send_keys('random')
    sleep(1)
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, 'button[type="submit"]')).click()

    try:
        webdriver_wait(driver, 10, (By.XPATH, '//*[contains(text(), "User telah login di 2 komputer atau lebih. Silahkan login kembali.")]'))
        print('FAILED : BOX CHART TIDAK KETEMU, MENCOBA KEMBALI')
        login(driver, username)

    except Exception as e:
        webdriver_wait(driver, 60, (By.CSS_SELECTOR, '.bg-dashboard.col-md-6.box-dashboard'))
        print('SUCCESS : BOX CHART KETEMU')     
        

def mulai_pleno(driver, model):
    try:
        driver.get(app_url + '/rekapitulasi')

        webdriver_wait(driver, 60, (By.CSS_SELECTOR, '#select2-filter_model-container')).click()
        sleep(1.5)
        webdriver_wait(driver, 5, (By.XPATH, '//li[contains(text(), "' +  model + '")]')).click()

        webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Apakah Anda akan memulai Rekapitulasi ?")]')).click()
        execute_script_click(driver, (By.CSS_SELECTOR, '#button_start'))
        sleep(1.5)
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
        webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Berhasil memulai pleno, operator sudah bisa melakukan edit entri")]'))

        print('SUCCESS : MEMULAI PLENO ' + model)

    except Exception as e:
        print('FAILED: MEMULAI PLENO ' + model + ', MENCOBA KEMBALI')

def ubah_pleno(driver, model):
    driver.get(app_url + '/rekapitulasi')

    webdriver_wait(driver, 60, (By.CSS_SELECTOR, '#select2-filter_model-container')).click()
    sleep(1.5)
    webdriver_wait(driver, 5, (By.XPATH, '//li[contains(text(), "' +  model + '")]')).click()

    tps_list = []
    expand_no = 0
    while not tps_list:
        webdriver_wait_many(driver, 30, (By.CSS_SELECTOR, '.showhide.cursor-hand'))[expand_no].click()
        try:
            tps_list = webdriver_wait_many(driver, 5, (By.XPATH, "//div[contains(@onclick, 'detailTps')]"))
        except TimeoutException:
            expand_no += 1
            continue

    for tps in tps_list:
        tps.click()
        sleep(2)
        webdriver_wait(driver, 10, (By.CSS_SELECTOR, '#btn-save-modal')).click()
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
        webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Data TPS berhasil Disimpan")]'))
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '.btn.btn-danger.alert-ok')).click()
        sleep(2)

        print('SUCCESS : MENYIMPAN PLENO ' + tps.text)

    print('SUCCESS : MENYIMPAN BEBERAPA PLENO TPS')

def finalisasi(driver, model):
    driver.get(app_url + '/rekapitulasi-finalisasi')
    
    webdriver_wait(driver, 60, (By.CSS_SELECTOR, '#select2-filter_model-container')).click()
    sleep(1.5)
    webdriver_wait(driver, 5, (By.XPATH, '//li[contains(text(), "' +  model + '")]')).click()

    webdriver_wait(driver, 30, (By.CSS_SELECTOR, '#finalisasi')).click()
    sleep(1.5)
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Berhasil Melakukan Finalisasi")]'))

    print('SUCCESS : FINALISASI ' + model)

def unggah_form(driver, model):
    driver.get(app_url + '/rekapitulasi-unggah')

    webdriver_wait(driver, 60, (By.CSS_SELECTOR, '#select2-filter_model-container')).click()
    sleep(1.5)
    webdriver_wait(driver, 5, (By.XPATH, '//li[contains(text(), "' +  model + '")]')).click()

    webdriver_wait_hidden(driver, 30, (By.CSS_SELECTOR, 'input[type="file"]')).send_keys('D:/TEST_PROJECT/Untitled1.pdf')
    sleep(1.5)
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#button_unggah')).click()
    webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Berhasil Melakukan Upload")]'))

    print('SUCCESS : UNGGAH FORM ' + model)

def bagikan_publikasi(driver, model):
    driver.get(app_url + '/rekapitulasi-verifikasi')

    webdriver_wait(driver, 60, (By.CSS_SELECTOR, '#select2-filter_model-container')).click()
    sleep(1.5)
    webdriver_wait(driver, 5, (By.XPATH, '//li[contains(text(), "' +  model + '")]')).click()

    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#tbsHasil-tab')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn_verified')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    webdriver_wait(driver, 60, (By.XPATH, '//*[contains(text(), "Berhasil mempublikasikan form D")]'))

    print('SUCCESS : PUBLIKASI FORM ' + model)

def penetapan(driver):
    driver.get(app_url + '/penetapan/filter')

    webdriver_wait(driver, 10, (By.CSS_SELECTOR, '#mulai_penetapan')).click()
    try:
        webdriver_wait(driver, 10, (By.CSS_SELECTOR, '.btn.btn-danger.alert-ok')).click()
        sleep(1)
    except:
        pass

    webdriver_wait(driver, 10, (By.CSS_SELECTOR, '#btnPenetapanPerolehanSuara')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    webdriver_wait(driver, 10, (By.XPATH, '//*[contains(text(), "Penetapan keputusan rekapitulasi penghitungan suara sudah dilakukan")]'))

    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#profile-tab-fill')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btnDokSKTTD')).click()
    webdriver_wait_hidden(driver, 30, (By.CSS_SELECTOR, 'input[id="dokumenPenetapan"]')).send_keys('D:/TEST_PROJECT/Untitled1.pdf')
    webdriver_wait_hidden(driver, 5, (By.CSS_SELECTOR, '#form_dokumen_penetapan')).submit()
    webdriver_wait(driver, 10, (By.XPATH, '//*[contains(text(), "Berhasil melakukan unggah dokumen SK")]'))
    try:    
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '.btn.btn-danger.alert-ok')).click()
        sleep(1)
    except:
        pass
    webdriver_wait(driver, 10, (By.CSS_SELECTOR, '#btnPublikasis')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    sleep(2)
    driver.refresh()

    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#sepepes-tab-fill')).click()
    try:    
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '.btn.btn-danger.alert-ok')).click()
        sleep(1)
    except:
        pass
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btnSengketaPenetapanPerolehanSuara')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    webdriver_wait(driver, 10, (By.XPATH, '//*[contains(text(), "Pernyataan bebas sengketa perolehan suara sudah dilakukan")]'))    
    driver.refresh()

    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#pepat-tab-fill')).click()
    try:    
        webdriver_wait(driver, 5, (By.CSS_SELECTOR, '.btn.btn-danger.alert-ok')).click()
        sleep(1)
    except:
        pass
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btnPenetapanPaslonTerpilih')).click()
    webdriver_wait(driver, 5, (By.CSS_SELECTOR, '#btn-alert-approve')).click()
    webdriver_wait(driver, 10, (By.XPATH, '//*[contains(text(), "Penetapan keputusan calon terpilih sudah dilakukan")]'))   

    print('SUCCESS : PENETAPAN')


def main(driver):
    akun = {
        'komisioner': [
            {
                'username': 'test_ppk_kec',
                'model': 'D.Hasil Kec'
            },
            {
                'username': 'test_komisioner_kab',
                'model': 'D.Hasil Kab/Ko'
            },
            {
                'username': 'test_komisioner_prov',
                'model': 'D.Hasil Prov'
            },
            {
                'username': 'test_komisioner_nas',
                'model': 'D.Hasil Nas'
            }
        ],
        'operator': [
            {
                'username': 'test_operator_kec',
                'model': 'D.Hasil Kec'
            },
            {
                'username': 'test_operator_kab',
                'model': 'D.Hasil Kab/Ko'
            },
            {
                'username': 'test_operator_prov',
                'model': 'D.Hasil Prov'
            }
        ]
    }

    #mengosongkan table
    reset_rekapitulasi()
    reset_penetapan()

    #memulai pleno pada semua tingkat
    for komisioner in akun['komisioner']:
        username = komisioner['username']
        model = komisioner['model']

        login(driver, username)
        mulai_pleno(driver, model)
    
    #inject data ke table suara_d_tps agar tidak perlu buka tps satu persatu
    inject_suara_d_tps() 

    #login akun PPK dan melakukan finalisasi
    login(driver, akun['komisioner'][0]['username'])
    finalisasi(driver, akun['komisioner'][0]['model'])

    #login akun operator kab/ko untuk menyimpan beberapa data tps agar dapat finalisasi kab/ko
    login(driver, akun['operator'][1]['username'])
    ubah_pleno(driver, akun['operator'][1]['model'])

    #login komisioner kab/ko, lakukan finalisasi, unggah form dan bagian hasil
    login(driver, akun['komisioner'][1]['username'])
    finalisasi(driver, akun['komisioner'][1]['model'])
    unggah_form(driver, akun['komisioner'][1]['model'])
    bagikan_publikasi(driver, akun['komisioner'][1]['model'])

    #login komisioner prov dan melakukan finalisasi
    login(driver, akun['komisioner'][2]['username'])
    finalisasi(driver, akun['komisioner'][2]['model'])
    unggah_form(driver, akun['komisioner'][2]['model'])
    bagikan_publikasi(driver, akun['komisioner'][2]['model'])
    
    login(driver, akun['komisioner'][3]['username'])
    finalisasi(driver, akun['komisioner'][3]['model'])
    unggah_form(driver, akun['komisioner'][3]['model'])
    bagikan_publikasi(driver, akun['komisioner'][3]['model'])
    penetapan(driver)