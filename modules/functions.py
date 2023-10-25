from modules.banners_and_style import colorize_text
import requests
from requests.auth import HTTPBasicAuth
import random
from time import sleep
from sys import stdout

def fuzz(wordlist=None, url=None, output_file=None, method='GET', owc=False, print_lock=None, xcookies=None, delay=None, xcustom_headers=None, auth=None, xdata=None):
    found_green = colorize_text("Found: ", "green", "bold")
    found_yellow = colorize_text("Found: ", "yellow", "bold")
    if auth is not None:
        username, password = auth  # Unpack auth tuple

    try:
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            method = 'GET'

        random_sleep = random.uniform(0, 8)
        sleep(random_sleep)

        for line in wordlist:
            url_2 = url + line  # Construct the URL by appending the line from the wordlist
            if delay > 0:
                sleep(delay)

            headers = xcustom_headers if xcustom_headers else {}
            cookies = xcookies if xcookies else {}
            data = xdata if xdata else {}

            if auth is not None:
                auth = HTTPBasicAuth(username, password)

            if method == 'GET':
                req = requests.get(url_2, cookies=cookies, headers=headers, auth=auth)
            elif method == 'POST':
                req = requests.post(url_2, cookies=cookies, headers=headers, data=data, auth=auth)
            elif method == 'PUT':
                req = requests.put(url_2, cookies=cookies, headers=headers, data=data, auth=auth)
            elif method == 'DELETE':
                req = requests.delete(url_2, cookies=cookies, headers=headers, auth=auth)
            elif method == 'PATCH':
                req = requests.patch(url_2, cookies=cookies, headers=headers, data=data, auth=auth)


            if req.status_code == 200:
                num = colorize_text("200", "green")  # Format the status code "200" in green
                with print_lock:

                    if auth is not None:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_green}{url_2} [{num}] {colorize_text('[Valid Authentication]', 'green', 'bold')}\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                    else:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_green}{url_2} [{num}]\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                if not owc:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")  # Append the found URL to the output file
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [100]")  # Append the found URL with status code to the output file

 # Similar blocks for other HTTP status codes (201, 204, 400, 401, 403, 404, 500, 502, 503)

            elif req.status_code == 201:

                num = colorize_text("201", "green")
                with print_lock:
                    if auth is not None:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_green}{url_2} [{num}] {colorize_text('[Created][Valid Authentication]', 'green', 'bold')}\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                    else:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Created','red','bold')}]\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [201]")

            elif req.status_code == 204:

                num = colorize_text("204", "green")
                with print_lock:
                    if auth is not None:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_green}{url_2} [{num}] {colorize_text('[No Content][Valid Authentication]', 'green', 'bold')}\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                    else:
                        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                        stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('No Content','green','bold')}]\n")  # Display the found URL with status code
                        stdout.write("\n")  # Add an empty line
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [204]")
                    
            elif req.status_code == 400:
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()


            elif req.status_code == 401:
                num = colorize_text("401", "yellow")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Unauthorized','red','bold')}]\n")  # Display the found URL with status code
                    stdout.write("\n")  # Add an empty line
                    stdout.flush() 
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [401]")
            
            elif req.status_code == 403:
                num = colorize_text("403", "yellow")
                
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Forbidden','red','bold')}]\n")  # Display the found URL with status code
                    stdout.write("\n")  # Add an empty line
                    stdout.flush() 
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [403]")

            elif req.status_code == 404:
                num = colorize_text("404", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r") 
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()

            elif req.status_code == 500:
                num = colorize_text("500", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Internal Server Error','red','bold')}]\n")  # Display the found URL with status code
                    stdout.write("\n")  # Add an empty line
                    stdout.flush() 
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")

            elif req.status_code == 502:
                num = colorize_text("502", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Bad Gateway','red','bold')}]\n")
                    stdout.write("\n")
                    stdout.flush()            
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")


            elif req.status_code == 503:
                num = colorize_text("503", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Service Unavailable','red','bold')}]\n")
                    stdout.write("\n")
                    stdout.flush()
                if owc == True:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")

    except requests.exceptions.TooManyRedirects:
        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line
    except requests.exceptions.RequestException as e:
        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line
    except ValueError as e:
        print("Error:", e)  # Display a general error message
