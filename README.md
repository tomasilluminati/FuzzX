# FuzzX - Directory Bruteforce Tool

![GitHub License](https://img.shields.io/badge/License-MIT-green) ![FuzzX Tool](https://img.shields.io/badge/Tool-Fuzzing_Web-blue)

## Overview

FuzzX is a versatile directory bruteforce tool designed to help you discover hidden files and directories on web servers. It offers multi-threading, various HTTP methods, customizable request intervals, and the option to export scan results. This tool is intended for educational and ethical use only.

## Table of Contents

- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Disclaimer](#disclaimer)

## Usage

To use FuzzX, follow these simple steps:

1. Clone this repository to your local machine.

2. Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool with the following command:

   ```bash
   python fuzzX.py -u <target_url> [-w <wordlist>] [-oN <output_file>] [-t <threads>] [-hm <http_method>] [--data <data=data>] [-owc] [--files] [-ex] [--cookies <example=example>] [-d or --delay <int>] [-ch <example=example>] [--auth <username,password>] [-no-redirect] [--timeout <int>] [--ssl] [--basic-auth <username,password>] [--digest-auth <username,password>] [--proxy-auth <username,password>] [--domains <path>] [--proxy <ftp/http/https://proxy:port>] [--only <200,201,204,400,401,403,404,500,502,503/> or <all>][--robots]
   ```

   - `-w`: Path to the wordlist file (.txt). (If not provided, the default wordlist will be used.)
   - `-u`: Root URL (e.g., https://example.com).
   - `-oN`: Result File Name (optional).
   - `-t`: Quantity of Threads (optional, default is 10).
   - `-hm`: HTTP Method (optional, default is GET).
   - `--data`: Add the data for the (POST, PUT and PATCH) request (optional).
   - `-owc`: Show the status code in the output file (optional).
   - `--files`: Change the search from directories to files (optional).
   - `-ex`: Extensions separated by (,) (optional, required if --files is used).
   - `--cookies`: Add Cookies. Provides cookies for the HTTP request. You can specify multiple cookies as space-separated key-value pairs. (Optional).
   - `-d` or `--delay`: Delay between requests (in seconds). Introduces a delay between requests to avoid overloading the server. Recommended use it with `-t 1` (Optional).
   - `-ch`: Allows users to define and include personalized HTTP headers in their requests, enabling tailored requests for specific requirements like authentication and content negotiation (Optional).
   - `--no-redirect`: Disallow redirections. If set, the program will not follow redirects when it finds them (optional).
   - `--timeout`: Set a timeout in seconds for HTTP requests in seconds. This parameter allows you to specify a maximum waiting time for receiving a response before considering the request timed out (Optional).
   - `--ssl`: Check the authenticity of the SSL certificate on the server. Enabling this option will verify the SSL certificate when making requests (Optional).
   - `--proxy`: Add FTP/HTTP/HTTPS proxies in the format proxy:port separated by commas (,). You can specify up to one proxy of each type at most (Optional).
   - `--basic-auth`: Add credentials for authentication in the format user,password separated by commas (,). This argument is used for basic authentication (Optional).
   - `--digest-auth`: Add credentials for authentication in the format user,password separated by commas (,). This argument is used for authentication using the Digest method (Optional).
   - `--proxy-auth`: Add credentials for proxy authentication in the format user,password separated by commas (,) (Optional).
   - `--subdomains`: Allows fuzzing by subdomains. You can provide an optional path to the subdomains list file. If a path is provided, the program will use those subdomains for fuzzing (Optional).
   - `--only`: Specifies which status codes to display, by default all are activated except 404
   - `--robots`: Analyze the robots.txt file and fuzz it (The program adds the link to the file automatically, it is not necessary to add it to the url, duplicates will be generated)


4. Adjust the tool's settings to suit your needs and start the directory brute force attack.

## Features

- Directory, file and subdomain brute force attacks.
- Multi-threaded for speed and efficiency.
- Supports various HTTP methods (GET, POST, PUT, DELETE, PATCH).
- POST, PUT and PATCH support data addition.
- Customizable request time intervals.
- Export scan results to a file.
- Filter by status code
- Colorized output for easy readability.
- Analyze the robots.txt
- Option to add cookies to requests.
- Option to add Custom Headers to requests.
- Authentication support with username and password (HTTPBasicAuth, HTTPProxyAuth, HTTPDigestAuth).
- Allow or disallow redirections.
- Set a timeout for HTTP requests in seconds.
- Check the SSL certificate on the server.
- Simulates a random delay before each request to emulate more human behavior.
- Allows the setting of proxies to act as intermediaries between your client and the destination server you want to access.
  



## Disclaimer

This program is provided as-is, with no warranties of any kind. The author and the code provider assume ZERO responsibility for any direct or indirect damages that may arise from the use of this program.

By using this program, you acknowledge and accept this disclaimer of liability.

**Please ensure that you understand the code and its implications before using it. Always conduct thorough testing in a safe environment before implementing this code in a production setting.**


## License

**Copyright © 2023 Tomás Illuminati**

*This project is licensed under the [MIT License](LICENSE).*

*Visit our GitHub repository: [FuzzX](https://github.com/tomasilluminati/FuzzX)*
