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
import numpy as np
import pytest
import os
import numpy as np

# from requests.adapters import HTTPAdapter, Retry


class TestCase:
    @pytest.mark.parametrize("expected", 
        (["10000", "20000", "30000"],["1000","2000","3000"], ["100","200","300"])
        # 追加のテストケースをここに追記
    )
    def test_true(self,expected):
        cmd = "test.bat"
        # np.savetxt("data_sample.txt", np.array(expected),fmt="%s")
        np.savetxt("./data_sample.txt", expected, fmt="%s")
        time.sleep(1)
        # p = sp.Popen(cmd, stdout=sp.PIPE, shell=True, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
        p = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        time.sleep(3)
        func = html_check()
        M1,M2,M3 = func.check_text('http://127.0.0.1:8000')

        
        parent = psutil.Process(p.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        os.remove("data_sample.txt")
        # assert [M1,M2,M3]==["10000","20000","30000"]
        assert [M1,M2,M3]==expected

if __name__ == '__main__':
    test = TestCase()
    test.test_true(["10000", "20000", "30000"])