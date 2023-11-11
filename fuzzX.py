#!/usr/bin/env python3

# Import necessary libraries and modules
from os import path, remove, rename
from modules.functions import *
from modules.functions_2 import *
from modules.banners_and_style import *
from sys import exit, argv
from shutil import copy
from re import match, findall
from requests import get
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
def main(wordlist=None, url=None, export=None, total_threads=None, http_method=None, owc=False, files=False, extensions=None, cookies=None, delay=None, custom_headers=None, basic_auth=None, data=None, xredirect=True, tout=10, ssl=False, proxies=None, digest_auth=None, proxy_auth=None, subdomains=False, only=None, robots=False):
    
    if xredirect is True:
        xredirect = False
    elif xredirect is False:
        xredirect = True

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    xcookies = {}
    xcustom_headers = {}
    xdata = {}
    xproxies = {}


    # Check the provided URL or prompt for one
    if url is not None:
        url = check_url(url)
    else:
        url = input(colorize_text("\n[-] Insert the root URL (https://example.com/)\n\n>>> ", "cyan"))
        url = check_url(url)


    if robots == True:
        
        try:
            delete_and_create_empty_file("./scanning/robots.txt")
            robots_txt = get(url+"robots.txt")
            
            robots_txt = robots_txt.text
            allow_lines = findall(r'Allow:\s*([^\s]+)', robots_txt)
            disallow_lines = findall(r'Disallow:\s*([^\s]+)', robots_txt)
            append_lines_to_file("./scanning/robots.txt", allow_lines)
            append_lines_to_file("./scanning/robots.txt", disallow_lines)
            remove_first_characters_inplace("./scanning/robots.txt")
            wordlist = "./scanning/robots.txt"

        except:
            print(colorize_text("Error: Error creating robots.txt file for scanning", "red"))
            exit()


    if only is not None:
        if len(only) > 0:

            if only[0].lower() == "all":
                only = ["200,201,204,400,401,403,404,500,502,503"]
            try:
                only = only[0].split(",")
            except:
                only = only

    if files is False and robots is False:
        if subdomains is not False:

            if subdomains is True:
                
                subdomains_list = generate_subdomain_combinations(url, "./wordlists/subdomains.txt")
                write_list_to_file(subdomains_list, "./scanning/sub_dom_tmp.txt")
            
            else:
                try:
                    subdomains_list = generate_subdomain_combinations(url, subdomains)
                    write_list_to_file(subdomains_list, "./scanning/sub_dom_tmp.txt")
                except:
                    print(colorize_text("Error: Invalid subdomains wordlist path", "red"))
                    exit()
    else:
        if subdomains is not False:
            print(colorize_text("Error: You can only use --files mode or --subdomains mode or --robots mode", "red"))
            exit()


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


    if basic_auth is not None:
        try:
            basic_auth = basic_auth[0].split(",")
            if len(basic_auth)>2:
                print(colorize_text("Error: --basic-auth can only receive 2 parameters <username,password>", "red"))
                exit()
        except ValueError:
            print(colorize_text("Error: --basic-auth needs some data in format <username,password> to work", "red"))
            exit()
    if digest_auth is not None:
        try:
            digest_auth = digest_auth[0].split(",")
            if len(digest_auth)>2:
                print(colorize_text("Error: --digest-auth can only receive 2 parameters <username,password>", "red"))
                exit()
        except ValueError:
            print(colorize_text("Error: --digest-auth needs some data in format <username,password> to work", "red"))
            exit()
    if proxy_auth is not None:
        try:
            proxy_auth = proxy_auth[0].split(",")
            if len(proxy_auth)>2:
                print(colorize_text("Error: --proxy-auth can only receive 2 parameters <username,password>", "red"))
                exit()
        except ValueError:
            print(colorize_text("Error: --proxy-auth needs some data in format <username,password> to work", "red"))
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

    if proxies is not None:
        if len(proxies) != 0:

            proxies_split = proxies[0].split(",")

            for x in proxies_split:
                if x[:7] == "http://":
                    if x[-1] == '/':
                        x = x[:-1]
                    xproxies["http"] = x

                elif x[:8] == "https://":
                    if x[-1] == '/':
                        x = x[:-1]
                    xproxies["https"] = x

                elif x[:6] == "ftp://":
                    if x[-1] == '/':
                        x = x[:-1]
                    xproxies["ftp"] = x

                else:
                    print(colorize_text("Error: The format must be ftp/http/https://proxy:port","red"))
                    exit()
        else:
            print(colorize_text("Error: --proxy needs some data in format ftp/http/https://proxy:port separated by (,) (One of each max.) to work", "red"))
            exit()

    
    

    if http_method is None:
        http_method = 'GET'
    else:
        http_method = http_method.upper()

    scanning_path = "./scanning/scanning.txt"


    # Delete and create an empty file for scanning
    delete_and_create_empty_file("./scanning/scanning.txt")

    
    if subdomains is False:
        if files == False:
            # Split the wordlist file into parts if provided, or use the default one
            if wordlist is not None:
                wordlist_len = count_lines_in_file(wordlist)
                if total_threads > wordlist_len:
                    try:
                        parts = split_file_into_parts(wordlist, wordlist_len)
                        total_threads = wordlist_len
                    except:
                        print(colorize_text("Error: 0 items in the wordlist","red"))
                        exit()
                else:
                    parts = split_file_into_parts(wordlist, total_threads)
            else:
                wordlist = "./wordlists/default.txt"
                wordlist_len = count_lines_in_file(wordlist)
                if total_threads > wordlist_len:
                    try:
                        parts = split_file_into_parts(wordlist, wordlist_len)
                        total_threads = wordlist_len
                    except:
                        print(colorize_text("Error: 0 items in the wordlist","red"))
                        exit()
                else:
                    try:
                        parts = split_file_into_parts(wordlist, total_threads)
                    except:
                        print(colorize_text("Error: 0 items in the wordlist","red"))
                        exit()

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

                try:
                    parts = split_file_into_parts("./wordlists/f_dict_w_ex.txt", total_threads)
                except:
                        print(colorize_text("Error: 0 items in the wordlist","red"))
                        exit()

                remove("./wordlists/f_dict_w_ex.txt")
            else:

                ex_file = read_file_to_list("./wordlists/extensions.txt")

                if wordlist is not None:
                    combined = combine_names_with_extensions(wordlist, ex_file)
                else:
                    wordlist = "./wordlists/default.txt"
                    combined = combine_names_with_extensions(wordlist, ex_file)

                write_list_to_file(combined, "./wordlists/f_dict_w_ex.txt")

                try:
                    parts = split_file_into_parts("./wordlists/f_dict_w_ex.txt", total_threads)
                except:
                        print(colorize_text("Error: 0 items in the wordlist","red"))
                        exit()


                remove("./wordlists/f_dict_w_ex.txt")

    else:
        
        wordlist = "./scanning/sub_dom_tmp.txt"
        wordlist_len = count_lines_in_file(wordlist)
        if total_threads > wordlist_len:
            parts = split_file_into_parts(wordlist, wordlist_len)
            total_threads = wordlist_len
        else:
            try:
                parts = split_file_into_parts(wordlist, total_threads)
            except:
                    print(colorize_text("Error: 0 items in the wordlist","red"))
                    exit()

            remove("./scanning/sub_dom_tmp.txt")

        wordlist = "./wordlists/subdomains.txt"

    
    # Show Main Banner
    init_banner()

    print(colorize_text("\n                        [!] Information\n", "yellow", "bold"))
    print(colorize_text("\nSTART TIME: ", "cyan", "bold")+colorize_text(f"{formatted_datetime}","white","bold"))
    print(colorize_text("\nWORDLIST: ", "cyan", "bold")+colorize_text(f"{wordlist}","white","bold"))
    print(colorize_text("\nURL: ", "cyan", "bold")+colorize_text(f"{url}","white","bold"))

    if files == True:
        if robots is True:
            print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"FILES (ROBOTS)","white","bold"))
        else:
            print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"FILES","white","bold"))
    elif files != True and subdomains is True:
        print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"SUBDOMAINS","white","bold"))
    else:
        if robots == True:
            print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"DIR (ROBOTS)","white","bold"))
        else:
            print(colorize_text("\nFUZZ TYPE: ", "cyan", "bold")+colorize_text(f"DIR","white","bold"))
    
    print(colorize_text("\nTHREADS: ", "cyan", "bold")+colorize_text(f"{total_threads}","white","bold"))
    if cookies is not None:
        print(colorize_text("\nCOOKIES: ", "cyan", "bold")+colorize_text(f"{xcookies[key]}","white","bold"))

    if xredirect == True:
        print(colorize_text("\nREDIRECTIONS: ", "cyan", "bold")+colorize_text(f"TRUE","green","bold"))
    else:
        print(colorize_text("\nREDIRECTIONS: ", "cyan", "bold")+colorize_text(f"FALSE","red","bold"))

    if ssl:
        print(colorize_text("\nSSL: ", "cyan", "bold")+colorize_text(f"TRUE","white","bold"))

    if custom_headers is not None:
        print(colorize_text("\nCUSTOM HEADERS: ", "cyan", "bold")+colorize_text(f"{xcustom_headers}","white","bold"))
    
    if data is not None:
        print(colorize_text("\nDATA: ", "cyan", "bold")+colorize_text(f"{xdata}","white","bold"))

    if basic_auth is not None:
        print(colorize_text("\nUSERNAME: ", "cyan", "bold")+colorize_text(f"{basic_auth[0]}","white","bold"))
        print(colorize_text("\nPASSWORD: ", "cyan", "bold")+colorize_text(f"{basic_auth[1]}","white","bold"))
    if digest_auth is not None:
        print(colorize_text("\nUSERNAME: ", "cyan", "bold")+colorize_text(f"{digest_auth[0]}","white","bold"))
        print(colorize_text("\nPASSWORD: ", "cyan", "bold")+colorize_text(f"{digest_auth[1]}","white","bold"))
    if proxy_auth is not None:
        print(colorize_text("\nUSERNAME: ", "cyan", "bold")+colorize_text(f"{proxy_auth[0]}","white","bold"))
        print(colorize_text("\nPASSWORD: ", "cyan", "bold")+colorize_text(f"{proxy_auth[1]}","white","bold"))

    if delay is not None and delay != 0:
        if delay == 1:  
            print(colorize_text("\nDELAY: ", "cyan", "bold")+colorize_text(f"{delay} Second","white","bold"))
        else:
            print(colorize_text("\nDELAY: ", "cyan", "bold")+colorize_text(f"{delay} Seconds","white","bold"))
    
    if proxies is not None and proxies != 0:
        print(colorize_text("\nPROXIES: ", "cyan", "bold")+colorize_text(f"{xproxies}","white","bold"))

    if flag_timeout:
        print(colorize_text("\nTIMEOUT: ", "cyan", "bold")+colorize_text(f"{tout} Seconds","white","bold"))

    separator("cyan")

    print("\n")

    print_lock = threading.Lock()

    threads = [] # List to store threads

    for part in parts:
        # Create a thread to perform URL fuzzing on a part of the word list
        thread = threading.Thread(target=fuzz, args=(part, url, scanning_path, http_method, owc, print_lock, xcookies, delay, xcustom_headers, basic_auth, xdata, xredirect, tout, ssl, xproxies, digest_auth, proxy_auth, subdomains, only))
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
    if robots is True:
        remove("./scanning/robots.txt")

    result = count_lines_in_file("./scanning/scanning.txt")
    

    if files is True:
        if result <= 0:
            stdout.write("\r" + " " * 70 + "\r")
            separator("cyan")
            print(colorize_text(f"\n                          {result} Files Found", "red", "bold"))
        else:
            stdout.write("\r" + " " * 70 + "\r")
            separator("cyan")
            print(colorize_text(f"\n                          {result} Files Found", "green", "bold"))
        
    else:
        if result <= 0:
            stdout.write("\r" + " " * 70 + "\r")
            separator("cyan")
            print(colorize_text(f"\n                          {result} Directories Found", "red", "bold"))
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
    parser.add_argument("--data", required=False, help="Add data for POST, PUT and PATCH requests", type=str, nargs="*")
    parser.add_argument('--no-redirect', action='store_true', default=False, help="Disallow redirections")
    parser.add_argument("--timeout", required=False, help="Set the timeout for the request", type=int)
    parser.add_argument('--ssl', action='store_false', default=False, help="Check the SSL certificate")
    parser.add_argument("--proxy", required=False, help="Add proxies ftp/http/https://proxy:port separated by (,) (One of each max.)", type=str, nargs="*")
    parser.add_argument("--basic-auth", required=False, help="Add credentials for authentication separated by (,) <user,password>", type=str, nargs="*")
    parser.add_argument("--digest-auth", required=False, help="Add credentials for authentication separated by (,) <user,password>", type=str, nargs="*")
    parser.add_argument("--proxy-auth", required=False, help="Add credentials for authentication separated by (,) <user,password>", type=str, nargs="*")
    parser.add_argument("--subdomains", nargs='?', const=True, type=str, default=False, help="Allows fuzzing by subdomains <Path to subdomains list (Optional)>")
    parser.add_argument("--only", required=False, help="Add the status codes you want to display separated by (,)", type=str, nargs="*")
    parser.add_argument('--robots', action='store_true', default=False, help="Analyze the robots.txt file and fuzz it")
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
    data = args.data
    xredirect = args.no_redirect
    tout = args.timeout
    ssl = args.ssl
    proxies = args.proxy
    basic_auth = args.basic_auth
    digest_auth = args.digest_auth
    proxy_auth = args.proxy_auth
    subdomains = args.subdomains
    only = args.only
    robots = args.robots
    

    main(wordlist, url, export, threads, http_method, owc, files, extensions, cookies, delay, custom_headers, basic_auth, data, xredirect, tout, ssl, proxies, digest_auth, proxy_auth, subdomains, only, robots)
