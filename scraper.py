import bs4.element
import requests
from bs4 import BeautifulSoup



# URL = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
URL = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
r = requests.get(URL)
soup = BeautifulSoup(r.content,
                     'html5lib')
divTag = soup.find("div", attrs={"class": "price"}).find(attrs={"class": "flbuts"})
print(divTag)
if divTag.find("a", attrs={"class": "cart-buy"}) or divTag.find("a", "Buy Now"):
    print("Available")
else:
    print("Not Available")
