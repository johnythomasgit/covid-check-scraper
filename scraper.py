import bs4.element
import requests
from bs4 import BeautifulSoup
from mailer import send_mail

if __name__ == "__main__":
    # URL = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
    URL = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,
                         'html5lib')
    divTag = soup.find("div", attrs={"class": "price"}).find(attrs={"class": "flbuts"})
    print(divTag)
    if divTag.find("a", attrs={"class": "cart-buy"}) or divTag.find("a", "Buy Now"):
        print("Available")
        send_mail("Your watch is now available", "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                                                 "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")
    else:
        print("Not Available")
        send_mail("Out of stock", "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                                                 "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")
