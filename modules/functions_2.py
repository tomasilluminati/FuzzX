def count_lines_in_file(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 0
            else:
                return int(len(lines))
    except FileNotFoundError:
        pass


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
    elif url.startswith("ftp"):
        if url.endswith("/"):
            return url
        else:
            url = url+"/"
            return url
        
    elif url.startswith("ftps"):
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
        print(f"The file '{file_name}' was not found")
        return []

def generate_subdomain_combinations(url, txt_file):
    with open(txt_file, 'r') as file:
        subdomains = file.read().splitlines()

    if url.startswith("http://"):
        url_prefix = "http://"
        url = url[len(url_prefix):]
    elif url.startswith("https://"):
        url_prefix = "https://"
        url = url[len(url_prefix):]
    elif url.startswith("ftp://"):
        url_prefix = "ftp://"
        url = url[len(url_prefix):]
    elif url.startswith("ftps://"):
        url_prefix = "ftps://"
        url = url[len(url_prefix):]
    else:
        url_prefix = ""

    combinations = [f"{url_prefix}{subdomain}.{url}" for subdomain in subdomains]

    return combinations
