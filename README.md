# FuzzX - Directory Bruteforce Tool

![GitHub License](https://img.shields.io/badge/License-MIT-green) ![FuzzX Tool](https://img.shields.io/badge/Tool-Fuzzing-blue)

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
   python fuzzX.py -u <target_url> [-w <wordlist>] [-oN <output_file>] [-t <threads>] [-hm <http_method>] [-owc] [--files] [-ex]
   ```

   - `-w`: Path to the wordlist file (.txt). (If not provided, the default wordlist will be used.)
   - `-u`: Root URL (e.g., https://example.com).
   - `-oN`: Result File Name (optional).
   - `-t`: Quantity of Threads (optional, default is 4).
   - `-hm`: HTTP Method (optional, default is GET).
   - `-owc`: Show the status code in the output file (optional).
   - `--files`: Change the search from directories to files (optional).
   - `-ex`: Extensions separated by (,) (optional, required if --files is used).
   - `--cookies`: Add Cookies. Provides cookies for the HTTP request. You can specify multiple cookies as space-separated key-value pairs. (Optional)
   - `-d` or `--delay`:Delay between requests (in seconds). Introduces a delay between requests to avoid overloading the server. Recommended use it with `-t 1` (Optional)

4. Adjust the tool's settings to suit your needs and start the directory brute force attack.

## Features

- Directory or file brute force attacks.
- Multi-threaded for speed and efficiency.
- Supports various HTTP methods (GET, POST, PUT, DELETE, PATCH).
- Export scan results to a file.
- Colorized output for easy readability


## Disclaimer

This program is provided as-is, with no warranties of any kind. The author and the code provider assume ZERO responsibility for any direct or indirect damages that may arise from the use of this program.

By using this program, you acknowledge and accept this disclaimer of liability.

**Please ensure that you understand the code and its implications before using it. Always conduct thorough testing in a safe environment before implementing this code in a production setting.**


## License

**Copyright © 2023 Tomás Illuminati**

*This project is licensed under the [MIT License](LICENSE).*

*Visit our GitHub repository: [FuzzX](https://github.com/yourusername/FuzzX)*
