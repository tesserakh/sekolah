# Sekolah

Get schools data in Indonesia from Kemendikbud

## Pre-requisite

Need to install Python 3.x and some its modules:

- requests
- beautifulsoup4
- lxml
- urllib3
- pandas

Linux installation:

```
python -m pip install --upgrade pip
pip install requests beautifulsoup4 lxml urllib3 pandas
```

## Scripts

**Name** - **Function**

- `pagination.py` - Get number of available schools data to used by `page=` inside _payload.txt_
- `payload.py` - Generate endpoint (payload data) to supplay POST request by `main.py`
- `main.py` - Create request / getting data from "mainpage" with pagination
- `profile.py` - Get other information from school's "profile" pages for data completion
- `sekolah.py`

## Datasets

**Input** --> **Output** | **Script**

1. _levels.csv_ --> _levels.csv_ (update itself) | using `pagination.py` script
2. _levels.csv_ --> _payload.txt_ | using `payload.py` script
3. _payload.txt_ --> _data/data*.csv_ | using `main.py` script
4. _data/data*.csv_ --> _data/profile*.csv_ | using `profile.py` script
