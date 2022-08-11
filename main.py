import requests
import pandas as pd
import urllib3
from bs4 import BeautifulSoup

# Setting for disable warning about expired web certificate
urllib3.disable_warnings()

file_name = 'data/data24.csv'
print(f'Data will be saved to {file_name}.')

# Empty list data slots
npsn_data = []
name_data = []
location_data = []
subdistrict_data = []
city_data = []
province_data = []
link_data = []
level_data = []
status_data = []

# Headers parameters for request
url = "https://sekolah.data.kemdikbud.go.id/index.php/Chome/pagingpencarian"
cookie = "BNI_persistence=EFZ1jjGERRt-V5uk3OqI7TVjdbsLAW4pGf7-xUyYG8POphmoB3yfqfYIHdx6X9Af341TSB3OkzMoaqxvOW-67Q%3D%3D; ci_session=g5v6adsnfv3nmotm7h8dgo6ovehql2ii"
headers = {
    "Cookie": cookie,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# There are 555,822 sekolah (schools) in total (all schools)
# Import endpoint/link list from payload.txt
payloadfile = open('payload.txt', 'r')
payload = payloadfile.read()
payload = payload.split('\n')
payloadfile.close()


# Main process (process #24)
for req in payload[115000:120000]:
    # Give some informations about process
    pg = req.split('&')[0].replace('page=', '')
    lv = req.split('&')[4].replace('bentuk_pendidikan=', '').replace('+',' ')
    st = req.split('&')[5].replace('status_sekolah=', '')
    print(f'Crawling page=%s, level=%s, status=%s' % (pg, lv, st))
    
    # Pages request section
    response = requests.request("POST", url, data = req, headers = headers, verify = False)    
    page = BeautifulSoup(response.content, 'lxml')
    cards = page.find_all('ul', class_ = 'list-group')
    
    # Parsing data process
    for card in cards:
        item = card.find_all('li', class_ = 'list-group-item')
        del item[-1]
        link = item[0].find('a')['href']
        name_number = item[0].find('a').text
        name = name_number.split(') ')[1]
        npsn = name_number.split(') ')[0].replace('(', '')
        
        address = []
        for i in item[1:]:
            address.append(i.text.strip())
        location = address[0]
        subdistrict = address[1]
        try:
            city = address[2].split(' Prov. ')[0]
            province = address[2].split(' Prov. ')[1]
        except:
            city = address[2]
            province = None

        # Attach new data to saved data (in memory)
        npsn_data.append(npsn)
        name_data.append(name)
        location_data.append(location)
        subdistrict_data.append(subdistrict)
        city_data.append(city)
        province_data.append(province)
        link_data.append(link)
        level_data.append(lv)
        status_data.append(st)


# Save table to CSV
tbl_data = {
  'NPSN' : npsn_data,
  'Name' : name_data,
  'Level': level_data,
  'Status' : status_data,
  'Location' : location_data,
  'Subdistrict' : subdistrict_data,
  'City' : city_data,
  'Province' : province_data,
  'Link' : link_data
}

tbl_data = pd.DataFrame(tbl_data)
tbl_data.to_csv(file_name, index = False)
print(f'Data saved to {file_name} with {len(tbl_data.index)} rows')
