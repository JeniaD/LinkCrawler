import argparse
import requests
from bs4 import BeautifulSoup

RESULTS = set()

def Parse(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Fatal:", e)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Simple link web crawler")
    parser.add_argument("target", help="your target URL")
    # parser.add_argument("--output", help="output directory path")
    # parser.add_argument("--filter", help="domain allowed to crawl (like .com)")
    args = parser.parse_args()

    # root = Parse(args.target)
    # if not root: exit(0)
    RESULTS.add(args.target)
    toScan = [args.target]
    newLinks = []
    
    while True:
        for link in toScan:
            try:
                soup = BeautifulSoup(Parse(link).content, "html.parser")

                linkElements = soup.select("a[href]")
                for elem in linkElements:
                    url = elem["href"]
                    if url not in newLinks and url not in toScan and url not in RESULTS:
                        newLinks += [url]
                        print(url)
                    
                    RESULTS.add(url)
            except AttributeError as e:
                continue
        
        if not newLinks: break
        else:
            for elem in toScan: RESULTS.add(elem)
            toScan = newLinks
            newLinks = []
