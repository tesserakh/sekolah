# Parsing CSV file and create endpoints/links

varfile = open('levels.csv', 'r')
vartext = varfile.read()
vartext = vartext.split('\n')

payload = []

for text in vartext[1:]:
    school = text.split(',')
    lv = school[0].replace(' ', '+') # level
    nst = round(int(school[1])/4) # n pages of state school
    npr = round(int(school[2])/4) # n pages of private school
    for n in range(1, nst+1):
        payload.append(f'page={n}&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=NEGERI')
    for n in range(1, npr+1):
        payload.append(f'page={n}&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=SWASTA')

varfile.close()

# Save to a TXT file
filename = 'payload.txt'
payloadfile = open(filename, 'w')
for i in payload:
    payloadfile.write(i + '\n')
payloadfile.close()

print(f'{filename} has been created from levels.csv!')