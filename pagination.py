import requests
import urllib3
import pandas as pd
from bs4 import BeautifulSoup

# Setting for disable warning about expired web certificate
urllib3.disable_warnings()

# Headers parameters for request
url = "https://sekolah.data.kemdikbud.go.id/index.php/Chome/loadpaging"
headers = {
    "Cookie": "BNI_persistence=EFZ1jjGERRt-V5uk3OqI7TVjdbsLAW4pGf7-xUyYG8POphmoB3yfqfYIHdx6X9Af341TSB3OkzMoaqxvOW-67Q%3D%3D; ci_session=5stj8prbgdhvdlv4qm0cjh3vd7gnne4u",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# Get school's levels data from levels.csv, then generate payload data
payload = []
with open('levels.csv', 'r') as varfile:
    vartext = varfile.read()
    vartext = vartext.split('\n')
    for text in vartext[1:]:
        school = text.split(',')
        lv = school[0].replace(' ', '+') # levels 
        payload.append(f'page=1&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=NEGERI')
        payload.append(f'page=1&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=SWASTA')

# Define data storage
school_level = []
state_school = []
prive_school = []

# Get number of schools from pagination section
for req in payload:

    lv = req.split('&')[4].replace('bentuk_pendidikan=', '').replace('+',' ')
    st = req.split('&')[5].replace('status_sekolah=', '')
    school_level.append(lv)

    response = requests.request("POST", url, data = req, headers = headers, verify = False)
    page = BeautifulSoup(response.content, 'lxml')
    npages = page.find('ul', class_ = 'pagination').find('li', class_ = 'active').text

    print(f'Get number of pages for %s %s = %s' % (lv, st, npages))

    npages = int(npages.split(' ')[0].replace(',', ''))
    if st == 'NEGERI':
        state_school.append(npages)
    elif st == 'SWASTA':
        prive_school.append(npages)
    
school_level = school_level[::2]

# Save table to CSV
filename = 'levels.csv'
tb = {
    'school' : school_level,
    'negeri' : state_school,
    'swasta' : prive_school
}

tb = pd.DataFrame(tb)
tb.to_csv(filename, index = False)
print(f'Data saved to {filename}')
