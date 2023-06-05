import requests

class html_check:
    def detect_value(self,text, machine_num):
        for line in text:
            if "number%s" % machine_num in line:
                text = line

        value = text.split(">")[1].split("<")[0]
        return value

    def check_text(self, url):
        # url = 'http://100.64.1.77/'
        # url = 'http://127.0.0.1:8000'
        # url = 'http://100.64.1.77/'

        session = requests.Session()
        response = session.get(url)
        text = response.text.split("\n")

        M1 = self.detect_value(text,1)
        M2 = self.detect_value(text,2)
        M3 = self.detect_value(text,3)


        print(M1,M2,M3)
        # print("a")
        return M1,M2,M3
    
if __name__ == '__main__':
    check = html_check()
    check.check_text("http://127.0.0.1:8000/")