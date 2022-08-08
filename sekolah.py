import requests
import pandas as pd
import urllib3
from bs4 import BeautifulSoup

# Setting for disable warning about expired web certificate
urllib3.disable_warnings()

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

# Variables: levels, status
levels_file = open("levels.txt", "r")
levels_txt = levels_file.read()
levels_txt = levels_txt.split('\n')
levels = []
for i in levels_txt:
    levels.append(i.replace(' ', '+'))
levels_file.close()
status = ['NEGERI', 'SWASTA'] # [ 'State', 'Private' ]
# There is 555,822 sekolah (schools) in total (all schools)
npages = round(55822/4)

# Create endpoint/link list to be requested
payload = []
for s in status:
    for l in levels:
        for n in range(1, npages+1):
            payload.append(f'page={n}&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={l}&status_sekolah={s}')

print(f'Link was created for: page 1-%s in level=%s & status=%s' % (npages, levels, status))

# Main process
for req in payload:
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
file_name = 'data.csv'
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