from cmath import log
from multiprocessing import context
from tokenize import group
from urllib import response
import requests
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Create your views here.


def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def getFile(request):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './files/hello.txt')
    # filename = os.path.basename(url)
    r = requests.get("http://127.0.0.1:8000", stream=True)
    r = requests.get(
        "https://media.istockphoto.com/photos/group-of-unrecognisable-international-students-having-online-meeting-picture-id1300822108?b=1&k=20&m=1300822108&s=170667a&w=0&h=CPtbj-Ax8p0oHcxhk30uhQEXc05Yg1LrfEdpxN1p2rc=", stream=True)

    resp = StreamingHttpResponse(streaming_content=r.raw)
    response = StreamingHttpResponse(streaming_content=r)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def index(request):
    if request.POST:
        global p, m, ph, ex, c, ch, va
        p, m, ph, ex, c, ch, va, text = "", "", "", "", "", "", "", ""
        url = request.POST.get("url")
        type = is_valid_url(url)
        if type == None:
            context = {
                "error": "The url is not valid"
            }
            return render(request, "imprint.html", context)

    # url = "file:///C:/Users/Michael_Narh/Desktop/imprint-download-project/imprint-html.html"
        # url = "https://www.bechtle.com/de-en/legal-notice"
        # print(url)
        try:

            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()
            print(text)

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip()
                      for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
        except:
            context = {
                "error": "Unable to open url or timeout, Try again"
            }
            return render(request, "imprint.html", context)

        # print(text)
        # print('...........................................')

        # mo1 = heroRegex.search(text)
        pro = re.search(r'(Provider.*:|Anbieter.*:).*\n.*', text)
        mail = re.search(r'E-mail.*:|E-Mail.*:.*\n.*', text)
        phone = re.search(r'(Phone:|Telefon:).*\n.*', text)
        exec = re.search(r'(Execu.*:|Vorstand.*:).*\n.*', text)
        chairman = re.search(
            r'(Chairman of.*:|Vorsitzender des.*:).*\n.*', text)
        com = re.search(r'(Commercial.*:|HRB-Nr.*:).*\n.*', text)
        vat = re.search(r'(VAT.*:|USt.*:).*\n.*', text)
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
            "pro": p,
            "email": m,
            "phone": ph,
            "exec": ex,
            "com": c,
            "chairman": ch,
            "vat": va,
        }
        return render(request, "imprint.html", context)
    return render(request, "imprint.html", {})
