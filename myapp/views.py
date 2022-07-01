from cmath import log
from multiprocessing import context
from tokenize import group
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Create your views here.


def index(request):
    if request.POST:
        global p, m, ph, ex, c, ch, va
        p, m, ph, ex, c, ch, va = "", "", "", "", "", "", ""
        url = request.POST.get("url")
    # url = "file:///C:/Users/Michael_Narh/Desktop/imprint-download-project/imprint-html.html"
        # url = "https://www.bechtle.com/de-en/legal-notice"
        # print(url)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # print(text)
        # print('...........................................')

        # mo1 = heroRegex.search(text)
        pro = re.search(r'Provider:|Anbieter:\n.*', text)
        mail = re.search(r'E-mail:|\n.*', text)
        phone = re.search(r'Phone:|Telefon:\n.*', text)
        exec = re.search(r'Execu.*|Vorstand:.*\n.*', text)
        chairman = re.search(r'Chairman of.*|Vorsitzender des.*\n.*', text)
        com = re.search(r'Commercial.*|HRB-Nr.*\n.*', text)
        vat = re.search(r'VAT.*|VAT number.*\n.*', text)
        try:
            p = pro.group()
        except:
            print("cannot group")
        try:
            m = mail.group
        except:
            print("cannot group")
        try:
            ph = phone.group
        except:
            print("cannot group")
        try:
            ex = exec.group
        except:
            print("cannot group")
        try:
            c = com.group
        except:
            print("cannot group")
        try:
            ch = chairman.group
        except:
            print("cannot group")
        try:
            va = vat.group
        except:
            print("cannot group")
        context = {
            "email": m,
            "phone": ph,
            "exec": ex,
            "com": c,
            "chairman": ch,
            "vat": ch,
        }
        return render(request, "imprint.html", context)
    return render(request, "imprint.html", {})
