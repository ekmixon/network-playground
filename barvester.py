import time
import urllib3
import sys
import re
import threading


class Barvester():

    poolManager = urllib3.PoolManager()

    def __init__(self):
        query = sys.argv[1]
        print(f"Googling... {query}")
        searchResults = self.getSearchResults(query.replace(" ", "%20"))
        urls = self.extractUrlsFromBody(searchResults)
        self.startCrawling(urls)

    def startCrawling(self, urls):
        extractedUrls = []

        for url in urls:
            htmlBody = self.retrieveHtmlBody(url)
            extractedUrls += self.extractUrlsFromBody(htmlBody)
            self.hasAnythingInteresting(htmlBody)
        self.startCrawling(extractedUrls)

    def threadedCrawling(self, urls):
        t = threading.Thread(target=self.startCrawling, args=[urls])
        t.start()

    def hasAnythingInteresting(self, htmlBody):
        emailPattern = '([a-zA-Z0-9.]+@[a-zA-Z0-9].\B.[a-zA-Z0-9.]+)'
        regexp = re.compile(emailPattern)
        if emailsList := regexp.findall(htmlBody):
            print(f"[<<] Goodies: {str(emailsList)}")

    def getSearchResults(self, searchQuery):
        baseUrl = "http://www.google.com/search?num=1000&q="
        searchUrl = baseUrl + searchQuery
        return self.retrieveHtmlBody(searchUrl)

    def retrieveHtmlBody(self, url):
        headers = {'User-Agent': "Googlebot"}
        try:
            response = self.poolManager.request('GET', url, headers=headers)
            htmlBody = response.data
        except:
            print(f"{url} down")
            htmlBody = "Website down"
        print(f"[>] Crawling {url}")

        return htmlBody

    def extractUrlsFromBody(self, htmlBody):
        urlPattern = '(href[":\/\+?_a-zA-Z=&0-9%.-]+)'
        regexp = re.compile(urlPattern)
        rawUrlsList = regexp.findall(htmlBody)
        urls = []

        for url in rawUrlsList:
            url = url.split('"')

            if len(url) >= 2:
                url = url[1].replace("/url?q=", "")
                if url.__contains__("http") \
                        and not url.__contains__("google") \
                        and not url.__contains__("https") \
                        and not url.__contains__("webmention") \
                        and not url.__contains__("mozilla.org") \
                        and not url.__contains__("facebook") \
                        and not url.__contains__("blogger"):
                    urls.append(url)
        return urls

Barvester()