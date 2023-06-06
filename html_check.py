import requests

class html_check:
    def load_html(self, url):
        session = requests.Session()
        response = session.get(url)
        self.text = response.text.split("\n")

    def detect_value(self,text, machine_num):
        for line in text:
            if "number%s" % machine_num in line:
                text = line

        value = text.split(">")[1].split("<")[0]
        return value

    def detect_time(self):
        text = self.text
        for i, line in enumerate(text):
            if "Current time" in line:
                sentence = text[i+1]

        value = sentence.split(">")[1].split("<")[0]
        date = value.split(" ")[0].replace("-","/")
        return date

    def check_text(self):
        # url = 'http://100.64.1.77/'
        # url = 'http://127.0.0.1:8000'
        # url = 'http://100.64.1.77/'
        text = self.text

        M1 = self.detect_value(text,1)
        M2 = self.detect_value(text,2)
        M3 = self.detect_value(text,3)


        print(M1,M2,M3)
        # print("a")
        return M1,M2,M3
    def check_time(self):
        pass
    
if __name__ == '__main__':
    check = html_check()
    url = "http://127.0.0.1:8000/"
    check.load_html(url)
    txt = check.check_text()
    date = check.detect_time()
    print(date)