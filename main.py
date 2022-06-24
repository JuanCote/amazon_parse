import requests
from bs4 import BeautifulSoup
import lxml
import csv

# product categories with the necessary parameters to build a query
categories = [
    {
        'rh': 'i:specialty-aps,n:16225007011,n:172456',
        'ref': 'nav_em__nav_desktop_sa_intl_computer_accessories_and_peripherals_0_2_6_2'
    },
    {
        'rh': 'i:specialty-aps,n:16225007011,n:193870011',
        'ref': 'nav_em__nav_desktop_sa_intl_computer_components_0_2_6_3'
    },
    {
        'rh': 'i:specialty-aps,n:16225007011,n:13896617011',
        'ref': 'nav_em__nav_desktop_sa_intl_computers_tablets_0_2_6_4'
    }
]

# user selects a category
while True:
    selected_category = int(input('Choose a category for pars\n0 - Computer Accessories & Peripherals\n1 - Computer Components\n2 - Computer Tablets\n'))
    if selected_category not in [0, 1, 2]:
        print('Invalid number, must be 0, 1 or 2')
        continue
    break

cookies = {
    'session-id': '141-5467531-5483862',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:UA"',
    'skin': 'noskin',
    'ubid-main': '130-6439338-9997843',
    'AMCVS_7742037254C95E840A4C98A6%40AdobeOrg': '1',
    'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C19168%7CMCMID%7C02199907222703114482662181843301166165%7CMCAAMLH-1656689379%7C6%7CMCAAMB-1656689379%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1656091779s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
    's_cc': 'true',
    'regStatus': 'pre-register',
    '_msuuid_jniwozxj70': 'F2B41FD3-6323-455A-9E35-32D5CDF42E51',
    'session-token': '7JmWbssrtQVpB3DEx77sWJkG+jwg1SWaBVMYnF/wEmNQQVXCFW12Owi/48Xk+xy4KVvgsIcjtaTeqMIYRbQ2rOja34hnHIo4+R0Qx9t7LzAVDxFSm1ebAeKF1hsntMEslVNh+Jdm7XvSzifcn+g0vgxjzXU1HRcGW9QfXOM0tigJTF3EzV4hp17QCa0HnEdl2RloxO0/QhMyFt8bpCpOyA==',
    'csm-hit': 'tb:s-5SHYGRVCBJSCFZZQN2KB|1656086071863&t:1656086072142&adb:adblk_yes',
}

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,uk;q=0.5',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'session-id=141-5467531-5483862; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:UA"; skin=noskin; ubid-main=130-6439338-9997843; AMCVS_7742037254C95E840A4C98A6%40AdobeOrg=1; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19168%7CMCMID%7C02199907222703114482662181843301166165%7CMCAAMLH-1656689379%7C6%7CMCAAMB-1656689379%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1656091779s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; s_cc=true; regStatus=pre-register; _msuuid_jniwozxj70=F2B41FD3-6323-455A-9E35-32D5CDF42E51; session-token=7JmWbssrtQVpB3DEx77sWJkG+jwg1SWaBVMYnF/wEmNQQVXCFW12Owi/48Xk+xy4KVvgsIcjtaTeqMIYRbQ2rOja34hnHIo4+R0Qx9t7LzAVDxFSm1ebAeKF1hsntMEslVNh+Jdm7XvSzifcn+g0vgxjzXU1HRcGW9QfXOM0tigJTF3EzV4hp17QCa0HnEdl2RloxO0/QhMyFt8bpCpOyA==; csm-hit=tb:s-5SHYGRVCBJSCFZZQN2KB|1656086071863&t:1656086072142&adb:adblk_yes',
    'device-memory': '8',
    'dnt': '1',
    'downlink': '2.4',
    'dpr': '1',
    'ect': '4g',
    'referer': 'https://www.amazon.com/gp/browse.html?node=21217035011&ref_=nav_em_sh_lighting_0_2_7_3',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-width': '1920',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'viewport-width': '1920',
}

params = {
    'i': 'specialty-aps',
    'bbn': '16225007011',
    'rh': categories[selected_category]['rh'],
    'ref': categories[selected_category]['ref'],
    'page': 1
}

response = requests.get('https://www.amazon.com/s', params=params, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

count_of_pages = int(soup.find('span', class_='s-pagination-item s-pagination-disabled').text)

with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Name', 'Rate', 'Price'])

for i in range(1, count_of_pages + 1):
    params['page'] = i

    response = requests.get('https://www.amazon.com/s', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all('div', class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')

    for card in cards:
        name = card.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
        try:
            rate = card.find('span', class_='a-icon-alt').text
        except:
            rate = 'No rate'
        try:
            price_dollars = card.find('span', class_='a-price-whole').text[:-1]
            price_pen = card.find('span', class_='a-price-fraction').text
            price = price_dollars + ',' + price_pen
        except:
            price = 'No price'

        with open('result.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([name, rate, price])

    print(f'{i} page out of {count_of_pages} completed')
