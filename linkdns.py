import requests
from bs4 import BeautifulSoup
import socket
import random
import sys
import time
from tabulate import tabulate

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
NC = '\033[0m'  # No Color

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Ubuntu; X11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def print_banner():
    print(f"{CYAN}#############################################")
    print(f"{GREEN}   Link Extractor and DNS Checker Script    ")
    print(f"{CYAN}#############################################")
    print(f"{WHITE}                Version 1.0                 ")
    print(f"{CYAN}#############################################")

def random_user_agent():
    return random.choice(user_agents)

def extract_links_and_dns(input_url):
    # Validate URL
    if not input_url.startswith(("http://", "https://")):
        print(f"{RED}Invalid URL. Please provide a valid HTTP or HTTPS URL.{NC}")
        sys.exit(1)

    # Extract links from the input URL
    print(f"Extracting links from {input_url}...")

    try:
        response = requests.get(input_url, headers={'User-Agent': random_user_agent()})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{RED}Error fetching the URL: {e}{NC}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set(a.get('href') for a in soup.find_all('a', href=True))

    # Prepare for output
    output_data = []
    
    print("\nExtracted Links:\n")
    print(tabulate([["Link", "DNS Info", "HTTP Response"]], headers="firstrow", tablefmt="grid"))

    for link in links:
        # Check if the link is a relative URL
        if not link.startswith(("http://", "https://")):
            link = f"{input_url.rstrip('/')}/{link.lstrip('/')}"

        print(f"Checking link: {link}")

        # Try to get the hostname and DNS info
        try:
            host = link.split("/")[2]
            dns_info = socket.gethostbyname(host)
        except Exception as e:
            dns_info = "No DNS info"
            print(f"{YELLOW}{dns_info} for {host}{NC}")

        # Get HTTP response code
        try:
            curl_response = requests.get(link, headers={'User-Agent': random_user_agent()}, allow_redirects=True)
            curl_output = f"{curl_response.status_code} {link}"
        except requests.RequestException as e:
            curl_output = f"Error: {e}"

        # Prepare the output for the current link
        output_data.append([link, dns_info, curl_output])
    
    # Print the output in a formatted table
    print(tabulate(output_data, headers=["Link", "DNS Info", "HTTP Response"], tablefmt="pretty"))
    print("Finished processing links.")

if __name__ == "__main__":
    print_banner()
    time.sleep(3)
    
    if len(sys.argv) != 2:
        print(f"{YELLOW}Usage: python {sys.argv[0]} <URL>{NC}")
        sys.exit(1)

    # Call the function with the provided URL argument
    extract_links_and_dns(sys.argv[1])
