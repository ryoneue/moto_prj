import requests

class html_check:
    def __init__(self, url):
        self.load_html(url)

    def load_html(self, url):
        session = requests.Session()
        response = session.get(url)
        self.text = response.text.split("\n")

    def detect_value(self,text, machine_num):
        for i, line in enumerate(text):
            if "number%s" % machine_num in line:
                value_text = text[i]
                name_text = text[i-1]



        value = value_text.split(">")[1].split("<")[0]
        name = name_text.split(">")[1].split("<")[0]
        return value, name

    def detect_time(self):
        text = self.text
        for i, line in enumerate(text):
            if "Current time" in line:
                sentence = text[i+1]

        value = sentence.split(">")[1].split("<")[0]
        date = value.split(" ")[0].replace("-","/")
        hour = value.split(" ")[1].split(":")[0]
        return date, hour

    def check_machine(self, machine_num):
        # url = 'http://100.64.1.77/'
        # url = 'http://127.0.0.1:8000'
        # url = 'http://100.64.1.77/'
        text = self.text

        date, hour = self.detect_time()
        info = {}
        for id in range(machine_num):
            # print(id)
            value, name = self.detect_value(text,id+1)
            info[name] = {hour:value}
        # M2 = self.detect_value(text,2)
        # M3 = self.detect_value(text,3)


        # print(M1,M2,M3)
        # print("a")
        return {date:info}
    def check_time(self):
        pass
    
if __name__ == '__main__':
    
    url = "http://127.0.0.1:8000/"
    check = html_check(url)
    check.load_html(url)
    txt = check.check_machine(machine_num=3)
    date = check.detect_time()
    print(txt)