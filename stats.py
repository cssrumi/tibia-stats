import mechanicalsoup
import pandas as pd


EMAIL = 'uzupelnij_email'
PASSWORD = 'uzupelnij_haslo'
LOGIN_URL = 'https://www.tibia.com/account/?subtopic=accountmanagement'
STATS_URL_TEMPLATE = 'https://www.tibia.com/account/?subtopic=accountmanagement&page=tibiacoinshistory&currentpage='
NO_CONTENT = 'No entries yet.'

browser = mechanicalsoup.StatefulBrowser()
browser.open(LOGIN_URL)
browser.select_form('form[name="AccountLoginForm"]')
browser.get_current_form().print_summary()
browser['loginemail'] = EMAIL
browser['loginpassword'] = PASSWORD
browser.submit_selected()

headers = None
entire_content = []
page_number = 1
while True:
    response = browser.open(STATS_URL_TEMPLATE + str(page_number))
    print('Page:', page_number)
    page = browser.get_current_page()
    try:
        table = page.find_all('table', class_='Table3')[1]
    except IndexError:
        break
    table_content = table.find('table', class_='TableContent')
    content = table_content.find_all('tr')
    headers = [element.text for element in content[0].find_all('td')]
    rows = [
        [element.text.replace('\xa0', ' ') for element in row]
        for row in content[1:-1]
    ]

    if rows[0][0] == NO_CONTENT:
        break

    entire_content.extend(rows)
    page_number += 1

data_frame = pd.DataFrame(
    entire_content,
    columns=headers
)

data_frame.to_excel('staty.xlsx')
