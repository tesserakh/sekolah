import requests
import urllib3
import pandas as pd
from bs4 import BeautifulSoup

txt_url_datasource = 'data/url/urls.txt'
csv_name_datastore = 'data/profile_sample.csv'

# Setting for disable warning about expired web certificate
urllib3.disable_warnings()

# Import url from url*.txt in data/url
url_list = []
with open(txt_url_datasource) as urlfile:
    urltext = urlfile.read()
    urltext = urltext.split('\n')
    for row in urltext:
        url_list.append(row)
urlfile.close()

# Main function
def get_school_info(url):
    try:
        # Getting pagesource
        res = requests.get(url, verify = False)
        page = BeautifulSoup(res.content, 'lxml')
        
        # URL info as first field
        label = ['Link']
        value = [url]
        # Parsing address
        try:
            title_header = page.find('h4', class_ = 'page-header')
            address = title_header.find('font').text.replace('(master referensi)', '').strip()
            label.append('Address')
            value.append(address)
        except:
            None
        # Parsing informations
        try:
            # Akreditasi, kepala sekolah, operator
            operational = page.find('ul', class_ = 'list-group').find_all('li', class_ = 'list-group-item')
            for item in operational[1:]:
                i = item.text
                label.append(i.split(':')[0].strip())
                value.append(i.split(':')[1].strip())
            # Other school info: building, etc.
            information = page.find_all('div', class_ = 'text-left')
            for info in information:
                i = info.text.split('\n')
                for each in i:
                    j = each.split(':')
                    if len(j) == 2:
                        label.append(j[0].strip())
                        value.append(j[1].strip())
                    else:
                        continue
            # Store info as label and value in data slot
            data = { label[i] : value[i] for i in range(len(label)) }
            return data
        except:
            pass
    except:
        pass
# end of function


# Main process
data_list = []
for url in url_list:
    print(f'Get data from {url}')
    newdata = get_school_info(url)
    if newdata:
        data_list.append(newdata)
    else:
        pass

# Save data
df = pd.DataFrame(data_list)
df.to_csv(csv_name_datastore, index = False)
print(f'Data saved to {csv_name_datastore}')
