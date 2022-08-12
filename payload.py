# Parsing CSV file and create endpoints/links
import math

input_file = 'levels.csv'
output_file = 'payload.txt'

varfile = open(input_file, 'r')
vartext = varfile.read()
vartext = vartext.split('\n')
for line in vartext[::-1]:
	if len(line.split(',')) == 1:
		vartext = vartext[:-1]

payload = []

for text in vartext[1:]:
    school = text.split(',')
    lv = school[0].replace(' ', '+') # level
    nst = math.ceil(int(school[1])/4) # n pages of state school
    npr = math.ceil(int(school[2])/4) # n pages of private school
    for n in range(1, nst+1):
        payload.append(f'page={n}&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=NEGERI')
    for n in range(1, npr+1):
        payload.append(f'page={n}&nama=&kode_kabupaten=&kode_kecamatan=&bentuk_pendidikan={lv}&status_sekolah=SWASTA')

varfile.close()

# Save to a TXT file
payloadfile = open(output_file, 'w')
for i in payload:
    payloadfile.write(i + '\n')
payloadfile.close()

print(f'{output_file} has been created from levels.csv')
