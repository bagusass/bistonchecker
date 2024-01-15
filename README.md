# BistonChecker
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![requests](https://img.shields.io/badge/requests-2.25.1-orange)](https://pypi.org/project/requests/)
[![rich](https://img.shields.io/badge/rich-10.1.0-orange)](https://pypi.org/project/rich/)
[![pyfiglet](https://img.shields.io/badge/pyfiglet-0.8.post1-orange)](https://pypi.org/project/pyfiglet/)
[![ipscoop](https://img.shields.io/badge/ipscoop-1.0.0-orange)](https://pypi.org/project/ipscoop/)

BistonChecker is a Python script for checking the status of proxies. It supports multi-threading and can filter proxies by country. The script is designed to efficiently check large lists of proxies in a short amount of time. It can handle HTTP, SOCKS4, and SOCKS5 proxy protocols.

<p align="center">
  <img src="https://i.imgur.com/ZJ167UN.jpg" alt="gambar 1" width="400">
  <img src="https://i.imgur.com/qaMPt3A.jpg" alt="gambar 2" width="400">
</p>

## Features

- **Multi-threading support**: BistonChecker utilizes Python's ThreadPool for fast and efficient proxy checking. You can specify the number of threads to use, allowing you to balance speed and system resources according to your needs.

- **Live Proxy Checking**: With BistonChecker, you can monitor the status of proxies in real-time. The `--show` option allows you to view live proxies as they are being checked, enabling you to start using working proxies immediately without waiting for the entire list to be processed.

- **Country Filtering and JSON Output**: BistonChecker is not just a proxy checker, it's also a powerful filtering tool. With the `--filter` option, you can filter proxies by country. The results are then saved to a JSON file, providing you with a structured and easily accessible list of proxies. This feature is particularly useful when you need proxies from specific countries.

- **Result Management**: BistonChecker provides flexible options for managing your results. The `--move` option allows you to move the filtered results to a specified output folder. Moreover, BistonChecker goes a step further by splitting the results for each country into separate files. This makes it easier for you to organize and find proxies based on your specific needs.

- **Support for Multiple Proxy Protocols**: BistonChecker is designed to handle various proxy protocols including HTTP, SOCKS4, and SOCKS5. It automatically detects the proxy protocol and checks the status accordingly, saving you the hassle of having to sort your proxies by protocol.

- **Colorful Terminal Output**: BistonChecker uses the rich library to provide a colorful and interactive terminal output. This makes the process of checking proxies more enjoyable and easier to understand.

- **Customizable Output File**: You can specify the name of the output file where the working proxies will be saved. By default, the output file is named 'proxy-working.json'.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/bistonchecker.git
```

2. Navigate to the project directory:

```bash
cd bistonchecker
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 bistonchecker.py -i inputfile -t 500 -o outputfile.json --show --filter --move
```

- `-i, --input`: Input file (proxy list)
- `-t, --threads`: Number of threads (default is 500)
- `-o`: Output file (default is 'proxy-working.json')
- `--show`: Show live proxies
- `--filter`: Filter by country (json)
- `--move`: Move result filter to output folder (split each country)

#### example command use case
```bash
python3 bistonchecker.py -i inputfile -t 500 -o outputfile.json --show
```
```bash
python3 bistonchecker.py -i inputfile -t 500 -o outputfile.json --filter --move
```

## Authors

 <a href="https://github.com/bagusass">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&label=bagusass&link=https%3A%2F%2Fgithub.com%2Fbagusass"/>
 </a>


## References

This project was inspired by and learned from the following resources:

- [ipscoop by anbuhckr](https://github.com/anbuhckr/ipscoop)
- [Proxytool by NDM4](https://github.com/NDM4/ProxyTool)

##  License

[MIT](https://choosealicense.com/licenses/mit/)
