#!/usr/bin/env python3

# Import necessary libraries and modules
from os import path, remove, rename
from modules.functions import *
from modules.functions_2 import *
from modules.banners_and_style import *
from sys import exit, argv
from shutil import copy
from re import match
import datetime
import argparse
import threading


def is_valid_extension(extension):
    return match(r'^\.\w+$', extension)


# Function to delete an existing file if it exists and create a new empty file in its place
def delete_and_create_empty_file(fpath):
    try:
        # Delete the existing file if it exists
        if path.exists(fpath):
            remove(fpath)

        # Create a new empty file
        with open(fpath, 'w'):
            pass

    except Exception as e:
        print(f'Error: {e}')


# Main function
def main(wordlist=None, url=None, export=None, total_threads=None, http_method=None, owc=False, files=False, extensions=None, cookies=None, delay=None, custom_headers=None, auth=None, data=None, xredirect=False, tout=10, ssl=False):
    
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    xcookies = {}
    xcustom_headers = {}
    xdata = {}

    if tout is not None:
        if tout <=0:
            tout = 1
        flag_timeout = True
    else:
        tout = 10
        flag_timeout = False

    if cookies is not None:
        try:
            for e in cookies:
                key, value = e.split('=')
                xcookies[key] = value
        except ValueError:
            print(colorize_text("Error: --cookies needs some data in format (example=example) to work", "red"))
            exit()


    if custom_headers is not None:
        try:
            for ch in custom_headers:
                key_ch, value_ch = ch.split("=")
                xcustom_headers[key_ch] = value_ch
        except:
            print(colorize_text("Error: -ch needs some data in format (example=example) to work", "red"))
            exit()

    if auth is not None:
        try:
            auth = auth[0].split(",")
            if len(auth)>2:
                print(colorize_text("Error: --auth can only receive 2 parameters <username:password>", "red"))
                exit()
        except ValueError:
            print(colorize_text("Error: --auth needs some data in format <username:password> to work", "red"))
            exit()

    # Set default values if not provided
    if total_threads is None:
        total_threads = 10
    else:
        total_threads = int(total_threads)

    if total_threads < 1:
        print(colorize_text("Error: -t (Threads) must be greater than or equal to 1", "red"))
        exit()
    elif total_threads > 100:
        print(colorize_text("Error: -t (Threads) must be less than or equal to 100", "red"))
        exit()
    

    if delay is None or delay < 0:
        delay = 0


    if files != False:
        try:
            extensions = extensions.split(",")
        except:
            print(colorize_text("Error: You need to add the -ex parameter", "red"))
            exit()

    if (data is not None and http_method is not None and http_method.upper() not in ["PUT", "PATCH", "POST"]) or (data is not None and http_method is None):
        print(colorize_text("Error: --data is only valid with a valid HTTP method (PUT, PATCH, or POST)","red"))
        exit()


    if data is not None:
        try:
            for d in data:
                key, value = d.split('=')
                xdata[key] = value
        except ValueError:
            print(colorize_text("Error: --data needs some data in format (example=example) to work", "red"))
            exit()

    # Show Main Banner
    init_banner()

    if http_method is None:
        http_method = 'GET'
    else:
        http_method = http_method.upper()

    scanning_path = "./scanning/scanning.txt"

    # Check the provided URL or prompt for one
    if url is not None:
        url = check_url(url)
    else:
        url = input(colorize_text("\n[-] Insert the root URL (https://example.com/)\n\n>>> ", "cyan"))
        url = check_url(url)

    # Delete and create an empty file for scanning
    delete_and_create_empty_file("./scanning/scanning.txt")

    

    if files == False:
        # Split the wordlist file into parts if provided, or use the default one
        if wordlist is not None:
            wordlist_len = count_lines_in_file(wordlist)
            if total_threads > wordlist_len:
                parts = split_file_into_parts(wordlist, wordlist_len)
                total_threads = wordlist_len
            else:
                parts = split_file_into_parts(wordlist, total_threads)
        else:
            wordlist = "./wordlists/default.txt"
            wordlist_len = count_lines_in_file(wordlist)
            if total_threads > wordlist_len:
                parts = split_file_into_parts(wordlist, wordlist_len)
                total_threads = wordlist_len
            else:
                parts = split_file_into_parts(wordlist, total_threads)

    else:
        flag = 0
        
        for ex in extensions:
            ex.strip()
        
        for ex in extensions:
            if is_valid_extension(ex):
                flag = 1
                pass
            else:
                flag = 0
                
        if flag == 1:
            combined = combine_names_with_extensions("./wordlists/default.txt", extensions)

            if wordlist is not None:
                combined = combine_names_with_extensions(wordlist, extensions)
            else:
                wordlist = "./wordlists/default.txt"
                combined = combine_names_with_extensions(wordlist, extensions)

            write_list_to_file(combined, "./wordlists/f_dict_w_ex.txt")

            parts = split_file_into_parts("./wordlists/f_dict_w_ex.txt", total_threads)

            remove("./wordlists/f_dict_w_ex.txt")
        else:
            
            ex_file = read_file_to_list("./wordlists/extensions.txt")

            if wordlist is not None:
                combined = combine_names_with_extensions(wordlist, ex_file)
            else:
                wordlist = "./wordlists/default.txt"
                combined = combine_names_with_extensions(wordlist, ex_file)

            write_list_to_file(combined, "./wordlists/f_dict_w_ex.txt")

            parts = split_file_into_parts("./wordlists/f_dict_w_ex.txt", total_threads)

            remove("./wordlists/f_dict_w_ex.txt")

    print(colorize_text("\n                        [!] Information\n", "yellow", "bold"))
    print(colorize_text("\nSTART TIME: ", "cyan", "bold")+colorize_text(f"{formatted_datetime}","white","bold"))
    print(colorize_text("\nWORDLIST: ", "cyan", "bold")+colorize_text(f"{wordlist}","white","bold"))
    print(colorize_text("\nURL: ", "cyan", "bold")+colorize_text(f"{url}","white","bold"))

    if files == True:
        print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"FILES","white","bold"))
    else:
        print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"DIR","white","bold"))
    
    print(colorize_text("\nTHREADS: ", "cyan", "bold")+colorize_text(f"{total_threads}","white","bold"))
    if cookies is not None:
        print(colorize_text("\nCOOKIES: ", "cyan", "bold")+colorize_text(f"{xcookies}","white","bold"))

    if ssl:
        print(colorize_text("\nSSL: ", "cyan", "bold")+colorize_text(f"TRUE","white","bold"))

    if custom_headers is not None:
        print(colorize_text("\nCUSTOM HEADERS: ", "cyan", "bold")+colorize_text(f"{xcustom_headers}","white","bold"))
    
    if data is not None:
        print(colorize_text("\nDATA: ", "cyan", "bold")+colorize_text(f"{xdata}","white","bold"))

    if auth is not None:
        print(colorize_text("\nUSERNAME: ", "cyan", "bold")+colorize_text(f"{auth[0]}","white","bold"))
        print(colorize_text("\nPASSWORD: ", "cyan", "bold")+colorize_text(f"{auth[1]}","white","bold"))

    if delay is not None and delay != 0:
        if delay == 1:  
            print(colorize_text("\nDELAY: ", "cyan", "bold")+colorize_text(f"{delay} Second","white","bold"))
        else:
            print(colorize_text("\nDELAY: ", "cyan", "bold")+colorize_text(f"{delay} Seconds","white","bold"))
    


    if flag_timeout:
        print(colorize_text("\nTIMEOUT: ", "cyan", "bold")+colorize_text(f"{tout} Seconds","white","bold"))

    separator("cyan")

    print("\n")

    print_lock = threading.Lock()

    threads = [] # List to store threads

    for part in parts:
#        ttime = random.randint(0, ttime)
        # Create a thread to perform URL fuzzing on a part of the word list
        thread = threading.Thread(target=fuzz, args=(part, url, scanning_path, http_method, owc, print_lock, xcookies, delay, xcustom_headers, auth, xdata, xredirect, tout, ssl))
        threads.append(thread) # Add the thread to the list of threads

    for thread in threads:
        thread.start() # Start each thread

    for thread in threads:
        thread.join() # Wait for each thread to finish its execution

    process_file_error("./scanning/scanning.txt", "./scanning/scanning_2.txt")
    remove_blank_lines("./scanning/scanning_2.txt", "./scanning/scanning_3.txt")
    remove("./scanning/scanning.txt")
    remove("./scanning/scanning_2.txt")
    rename("./scanning/scanning_3.txt", "./scanning/scanning.txt")

    result = count_lines_in_file("./scanning/scanning.txt")
    

    if result >= 0:
        if files is True:
            print(colorize_text(f"\n                          {result} Files Found", "red", "bold"))
        else:
            stdout.write("\r" + " " * 70 + "\r")
            separator("cyan")
            print(colorize_text(f"\n                          {result} Directories Found", "green", "bold"))

    # If an export file is provided, copy the result
    if export is not None:
        copy("./scanning/scanning.txt", f"./{export}")

    stdout.write("\r" + " " * 100 + "\r")
    stdout.flush()
    separator("cyan")
    print(colorize_text("\n[-] PROGRAM FINISHED", "yellow"))
    separator("cyan")

    # Delete and create an empty file for scanning
    delete_and_create_empty_file("./scanning/scanning.txt")

if __name__ == "__main__":

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="FuzzX - Directory Bruteforce Tool")
    # Add the arguments
    parser.add_argument("-w", required=False, help="Path to the wordlist file (.txt)", type=str)
    parser.add_argument("-u", required=True, help="Root URL (e.g., https://example.com)", type=str)
    parser.add_argument("-oN", required=False, help="Result File Name", type=str)
    parser.add_argument("-t", required=False, help="Quantity of Threads", type=int)
    parser.add_argument("-hm", required=False, help="Http Method", type=str)
    parser.add_argument('-owc', action='store_true', default=False, help="Show the status code in the output file")
    parser.add_argument('--files', action='store_true', default=False, help="Change the search from dir to files, (Needed -ex parameter)")
    parser.add_argument('-ex', type=str, nargs='?' if '--files' in argv else 1, help="Extensions separated by (,)")
    parser.add_argument("--cookies", required=False, help="Add Cookies", type=str, nargs="*")
    parser.add_argument("-d", "--delay", required=False, type=int, default=0, help="Delay between requests (in seconds)")
    parser.add_argument("-ch", required=False, help="Add Custom Headers", type=str, nargs="*")
    parser.add_argument("--auth", required=False, help="Add credentials for authentication separated by (,) <user,password>", type=str, nargs="*")
    parser.add_argument("--data", required=False, help="Add data for POST, PUT and PATCH requests", type=str, nargs="*")
    parser.add_argument('--redirect', action='store_true', default=False, help="Allow redirections")
    parser.add_argument("--timeout", required=False, help="Set the timeout for the request", type=int)
    parser.add_argument('--ssl', action='store_true', default=False, help="Check the SSL certificate")
    args = parser.parse_args()

    # Get argument values and run the main function
    wordlist = args.w
    export = args.oN
    url = args.u
    threads = args.t
    http_method = args.hm
    owc = args.owc
    files = args.files
    extensions = args.ex
    cookies = args.cookies
    delay = args.delay
    custom_headers = args.ch
    auth = args.auth
    data = args.data
    xredirect = args.redirect
    tout = args.timeout
    ssl = args.ssl

    main(wordlist, url, export, threads, http_method, owc, files, extensions, cookies, delay, custom_headers, auth, data, xredirect, tout, ssl)
