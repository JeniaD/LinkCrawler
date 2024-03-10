import argparse
import requests
from bs4 import BeautifulSoup

RESULTS = set()

def CheckURL(url, topDomain=None):
    if not url.split('/')[0] or url.split('/')[0] == '.' or '.' not in url or "mailto:" in url or '%' in url or "javascript:" in url or len(url) < 3: return False
    if topDomain and topDomain not in url: return False

    return True

def CleanURL(url):
    url = url.replace("www.", '') # WARNING: might fail opening some sites without redirect

    if "http" not in url:
        return url.split('/')[0].split('?')[0]
    else:
        if "https" in url:
            return "https://" + url.replace("https://", '').split('/')[0].split('?')[0]
        else:
            return "http://" + url.replace("http://", '').split('/')[0].split('?')[0]

def Parse(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Fatal:", e)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Simple link web crawler")
    parser.add_argument("target", help="your target URL")
    parser.add_argument("--output", help="output directory path")
    parser.add_argument("--filter", help="domain allowed to crawl (like .com)")
    args = parser.parse_args()

    RESULTS.add(args.target)
    toScan = [args.target]
    newLinks = []
    
    try:
        while True:
            for link in toScan:
                try:
                    soup = BeautifulSoup(Parse(link).content, "html.parser")

                    linkElements = soup.select("a[href]")
                    for elem in linkElements:
                        url = CleanURL(elem["href"])
                        if CheckURL(url, args.filter) and url not in newLinks and url not in toScan and url not in RESULTS:
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
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        print(RESULTS)

    if args.output:
        with open(args.output, 'w') as file:
            for link in RESULTS:
                file.write(link + '\n')
