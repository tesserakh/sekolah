import requests
import urllib3
import pandas as pd
from bs4 import BeautifulSoup

csv_url_datasource = 'data/data1.csv'
csv_name_datastore = 'data/profile1.csv'

# Setting for disable warning about expired web certificate
urllib3.disable_warnings()

# Import url from data/data.csv
url_list = []
with open(csv_url_datasource) as urlfile:
    urltext = urlfile.read()
    urltext = urltext.split('\n')[1:]
    for row in urltext:
        url_list.append(row.split(',')[-1])

# Main function
def get_school_info(url):
    # Getting pagesource
    res = requests.get(url, verify = False)
    page = BeautifulSoup(res.content, 'lxml')
    
    # URL info as first field
    label = ['Link']
    value = [url]
    # Parsing informations
    try:
        # Akreditasi, kepala sekolah, operator
        operational = page.find('ul', class_ = 'list-group').find_all('li', class_ = 'list-group-item')
        for item in operational[1:]:
            i = item.text
            label.append(i.split(':')[0].strip())
            value.append(i.split(':')[1].strip())
        # Other school info
        information = page.find_all('div', class_ = 'text-left')
        for info in information:
            i = info.text.split('\n')
            for each in i:
                j = each.split(':')
                if len(j) == 2:
                    label.append(j[0].strip())
                    value.append(j[1].strip())
                else:
                    next
        # Store info as label and value in data slot
        data = { label[i] : value[i] for i in range(len(label)) }
    except:
        pass
    return data


# Main process
data_list = []
for url in url_list:
    print(f'Get data from {url}')
    data_list.append(get_school_info(url))

# Save data
df = pd.DataFrame(data_list)
df.to_csv(csv_name_datastore, index = False)
print(f'Data saved to {csv_name_datastore}')
