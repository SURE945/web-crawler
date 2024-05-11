import os,json,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()

def print_url_to_pdf(url, save_root,
                     file_name='demo.pdf'):
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,

        # "customMargins": {},
        # "marginsType": 2,
        # "scaling": 100,
        # "scalingType": 3,
        # "scalingTypePdf": 3,
        "isLandscapeEnabled":True,#landscape横向，portrait 纵向，若不设置该参数，默认纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4 210 x 297 mm"
        },
    }

    chrome_options.add_argument('--enable-print-browser')
    #chrome_options.add_argument('--headless') #headless模式下，浏览器窗口不可见，可提高效率

    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': save_root #此处填写你希望文件保存的路径
    }
    chrome_options.add_argument('--kiosk-printing') #静默打印，无需用户点击打印页面的确定按钮
    chrome_options.add_experimental_option('prefs', prefs)


    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    # time.sleep(7)
    execute_command = f'document.title = "{file_name}.pdf"; window.print();'
    driver.execute_script(execute_command) #利用js修改网页的title，该title最终就是PDF文件名，利用js的window.print可以快速调出浏览器打印窗口，避免使用热键ctrl+P
    driver.close()