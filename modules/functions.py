from modules.banners_and_style import colorize_text
import requests
import random
from time import sleep
from sys import stdout



def split_file_into_parts(file, num_parts):
    # Open the file and read all the lines into a list
    with open(file, 'r') as f:
        lines = f.readlines()

    # Calculate the number of lines in the file
    num_lines = len(lines)

    # Calculate the number of lines per part
    lines_per_part = num_lines // num_parts

    # Split the file into parts and remove newline characters
    parts = []
    for i in range(num_parts):
        start = i * lines_per_part
        end = (i + 1) * lines_per_part
        part = [line.strip() for line in lines[start:end]]
        parts.append(part)

    return parts

# Function to check and format a URL
def check_url(url):
    url = url.lower()
    if url.startswith("https"):
        if url.endswith("/"):
            return url
        else:
            url = url+"/"
            return url
    elif url.startswith("http"):
        if url.endswith("/"):
            return url
        else:
            url = url+"/"
            return url
    else:
        url = "https://"+url
        if url.endswith("/"):
            return url
        else:
            url = url+"/"
            return url



def fuzz(wordlist=None, url=None, output_file=None, method='GET', owc=False, print_lock=None):
    
    found_green = colorize_text("Found: ", "green", "bold")  # Formatting for "Found" in green
    found_yellow = colorize_text("Found: ", "yellow", "bold")  # Formatting for "Found" in yellow

    try:
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            method = 'GET'  # Default to 'GET' if an invalid HTTP method is provided

        random_sleep = random.uniform(0, 8)
        sleep(random_sleep) 
  
        for line in wordlist:
            url_2 = url + line  # Construct the URL by appending the line from the wordlist
            if method == 'GET':
                req = requests.get(url_2)  # Send a GET request to the URL
            elif method == 'POST':
                req = requests.post(url_2)  # Send a POST request to the URL
            elif method == 'PUT':
                req = requests.put(url_2)  # Send a PUT request to the URL
            elif method == 'DELETE':
                req = requests.delete(url_2)  # Send a DELETE request to the URL
            elif method == 'PATCH':
                req = requests.patch(url_2)  # Send a PATCH request to the URL

            if req.status_code == 200:
                num = colorize_text("200", "green")  # Format the status code "100" in green
                with print_lock:
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
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_green}{url_2} [{num}]\n")
                    stdout.write("\n")
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [201]")

            elif req.status_code == 204:

                num = colorize_text("204 (No Content)", "green")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_green}{url_2} [{num} ]\n")
                    stdout.write("\n")
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [204]")
                    
            elif req.status_code == 400:
                num = colorize_text("400 (Bad Request)", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()


            elif req.status_code == 401:
                num = colorize_text("401 (Unauthorized)", "yellow")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}]\n")
                    stdout.write("\n")
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [401]")
            
            elif req.status_code == 403:
                num = colorize_text("403 (Forbidden)", "yellow")
                
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{found_yellow}{url_2} [{num}]\n")
                    stdout.write("\n")
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
                num = colorize_text("500 (Internal Server Error)", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [500]")
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{url_2} [{num}]\n")
                    stdout.write("\n")

            elif req.status_code == 502:
                num = colorize_text("502 (Bad Gateway)", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()            
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [502]")
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{url_2} [{num}]\n")
                    stdout.write("\n")

            elif req.status_code == 503:
                num = colorize_text("503 (Service Unavailable)", "red")
                analysis = colorize_text("Analizing:", "cyan", "bold")
                with print_lock:
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{analysis} {url_2}")
                    stdout.flush()
                if owc == False:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2}")
                else:
                    with open(output_file, 'a') as file:
                        file.write(f"\n{url_2} [503]")
                    stdout.write("\r" + " " * 70 + "\r")
                    stdout.write(f"{url_2} [{num}]\n")
                    stdout.write("\n")


    except requests.exceptions.TooManyRedirects:
        stdout.write("\r" + " " * 100 + "\r")  # Clear the console line
    except requests.exceptions.RequestException as e:
        stdout.write("Connection Error:", e)  # Display a connection error message
        stdout.write("\r" + " " * 100 + "\r")  # Clear the console line
    except ValueError as e:
        print("Error:", e)  # Display a general error message

# Function to process the input file, adding newlines before URLs starting with "http"
def process_file_error(input_file, output_file):
    try:
        with open(input_file, 'r') as input_file:
            with open(output_file, 'w') as output_file:
                for line in input_file:
                    # Add a newline at the beginning of the line if the word "http" is found anywhere
                    line = line.replace('http', '\nhttp')
                    output_file.write(line)

    except FileNotFoundError:
        print("The input file was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to remove blank lines from the input file
def remove_blank_lines(input_file, output_file):
    try:
        with open(input_file, 'r') as input_file:
            lines = input_file.readlines()

        # Remove blank lines
        lines_without_blanks = [line.strip() for line in lines if line.strip()]

        with open(output_file, 'w') as output_file:
            output_file.write('\n'.join(lines_without_blanks))
                              
    except FileNotFoundError:
        print("The input file does not exist.")
    except Exception as e:
        print("An error occurred:", str(e))


def combine_names_with_extensions(txt_file, extensions):
    with open(txt_file, 'r') as file:
        names = [line.strip() for line in file.readlines()]

    combined_names = [f"{name}{ext}" for name in names for ext in extensions]

    return combined_names


def write_list_to_file(my_list, file_name):
    with open(file_name, 'w') as file:
        for item in my_list:
            file.write(str(item) + '\n')

def read_file_to_list(file_name):
    my_list = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                my_list.append(line.strip())  # strip() removes leading and trailing whitespace characters
        return my_list
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return []
