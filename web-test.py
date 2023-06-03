import subprocess as sp
import time
import socket
import sys
from bs4 import BeautifulSoup
import requests
import psutil
import requests
from html_check import html_check
import json

# from requests.adapters import HTTPAdapter, Retry


class TestCase:
    def test_true(self):
        cmd = "test.bat"

        # p = sp.Popen(cmd, stdout=sp.PIPE, shell=True, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
        p = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        time.sleep(3)
        func = html_check()
        M1,M2,M3 = func.check_text('http://127.0.0.1:8000')

        parent = psutil.Process(p.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        assert [M1,M2,M3]==["10000","20000","30000"]

    def test_false(self):
        cmd = "test.bat"
        # p = sp.Popen(cmd, stdout=sp.PIPE, shell=True, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
        p = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        time.sleep(3)
        func = html_check()
        M1,M2,M3 = func.check_text('http://127.0.0.1:8000')

        parent = psutil.Process(p.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        assert [M1,M2,M3]!=["1000","2000","3000"]