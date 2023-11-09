# Import necessary modules
from modules.banners_and_style import colorize_text
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
import random
from time import sleep
from sys import stdout

# Define the main function 'fuzz' with various parameters
def fuzz(wordlist=None, url=None, output_file=None, method='GET', owc=False, print_lock=None, xcookies=None, delay=None, xcustom_headers=None, basic_auth=None, xdata=None, xredirect=True, tout=10, ssl=False, xproxies=None, digest_auth=None, proxy_auth=None, subdomains=False, only=None):
    # Define text formatting for display messages
    found_green = colorize_text("Found: ", "green", "bold")
    found_yellow = colorize_text("Found: ", "yellow", "bold")
    
    # Unpack authentication information
    if basic_auth is not None:
        username, password = basic_auth
    elif digest_auth is not None:
        username, password = digest_auth
    elif proxy_auth is not None:
        username, password = proxy_auth

    try:
        # Ensure 'method' is a valid HTTP method
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            method = 'GET'

        # Introduce random sleep to simulate human-like interaction
        random_sleep = random.uniform(0, 8)
        sleep(random_sleep)
        
        # Iterate through the wordlist
        for line in wordlist:

            if subdomains is False:
                url_2 = url + line  # Construct the URL by appending the line from the wordlist
            else:
                url_2 = line

            # Introduce a delay if specified
            if delay > 0:
                sleep(delay)

            # Initialize headers, cookies, and data
            headers = xcustom_headers if xcustom_headers else {}
            cookies = xcookies if xcookies else {}
            data = xdata if xdata else {}
            auth = None

            # Handle HTTP Basic, Digest and Proxy Authentication
            if basic_auth is not None:
                auth = HTTPBasicAuth(username, password)
            elif digest_auth is not None:
                auth = HTTPDigestAuth(username, password)
            elif proxy_auth is not None:
                auth = HTTPProxyAuth(username, password)

            # Perform an HTTP request based on the specified method
            if method == 'GET':
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r") 
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()      
                try:
                    if ssl == True:
                        req = requests.get(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, verify=ssl, proxies=xproxies)
                    else:
                        req = requests.get(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, proxies=xproxies)
                except TimeoutError:
                    break
            elif method == 'POST':
                try:
                    if ssl == True:
                        req = requests.post(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, verify=ssl, data=xdata, proxies=xproxies)
                    else:
                        req = requests.post(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, data=xdata, proxies=xproxies)
                except TimeoutError:
                    break
            elif method == 'PUT':
                try:
                    if ssl == True:
                        req = requests.put(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, verify=ssl, data=xdata, proxies=xproxies)
                    else:
                        req = requests.put(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, data=xdata, proxies=xproxies)
                except TimeoutError:
                    break
            elif method == 'DELETE':
                try:
                    if ssl == True:
                        req = requests.delete(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, verify=ssl, proxies=xproxies)
                    else:
                        req = requests.delete(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, proxies=xproxies)
                except TimeoutError:
                    break
            elif method == 'PATCH':
                try:
                    if ssl == True:
                        req = requests.patch(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, verify=ssl, data=xdata)
                    else:
                        req = requests.patch(url_2, cookies=cookies, headers=headers, auth=auth, allow_redirects=xredirect, timeout=tout, data=xdata)
                except TimeoutError:
                    break

                  

            if (req.status_code == 200 and only is None) or (req.status_code == 200 and str(req.status_code) in only):
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
                        file.write(f"\n{url_2} [200]")  # Append the found URL with status code to the output file

 # Similar blocks for other HTTP status codes (201, 204, 400, 401, 403, 404, 500, 502, 503)

            elif (req.status_code == 201 and only is None) or (req.status_code == 201 and str(req.status_code) in only):

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

            elif (req.status_code == 204 and only is None) or (req.status_code == 204 and str(req.status_code) in only):

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


            elif (req.status_code == 401 and only is None) or (req.status_code == 401 and str(req.status_code) in only):
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
            
            elif (req.status_code == 403 and only is None) or (req.status_code == 403 and str(req.status_code) in only):
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



            elif req.status_code == 404 and str(req.status_code) in only:
                num = colorize_text("404", "yellow")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")  # Clear the console line 
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Not Found','red','bold')}]\n")  # Display the found URL with status code
                    stdout.write("\n")  # Add an empty line
                    stdout.flush() 
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [404]")

            elif (req.status_code == 500 and only is None) or (req.status_code == 500 and str(req.status_code) in only):
                num = colorize_text("500", "red")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Internal Server Error','red','bold')}]\n")  # Display the found URL with status code
                    stdout.write("\n")  # Add an empty line
                    stdout.flush() 
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [500]")

            elif (req.status_code == 502 and only is None) or (req.status_code == 502 and str(req.status_code) in only):
                num = colorize_text("502", "red")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Bad Gateway','red','bold')}]\n")
                    stdout.write("\n")
                    stdout.flush()            
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} ")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [502]")


            elif (req.status_code == 503 and only is None) or (req.status_code == 503 and str(req.status_code) in only):
                num = colorize_text("503", "red")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}] [{colorize_text('Service Unavailable','red','bold')}]\n")
                    stdout.write("\n")
                    stdout.flush()
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [503]")

    except requests.exceptions.TooManyRedirects:
        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line
    except requests.exceptions.RequestException as e:
        stdout.write("\r" + " " * 70 + "\r")  # Clear the console line
    except ValueError as e:
        print("Error:", e)  # Display a general error message
