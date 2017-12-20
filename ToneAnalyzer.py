import json
import requests
import pygal
import sys


class ToneAnalyzer:
    def __init__(self, text):
        self.username = '0283e965-ef1d-4737-ba70-c1eefcca4939'
        self.password = 'uJqpULCLFnjm'
        self.watson_url = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-18'
        self.headers = {"content-type": "text/plain"}
        self.text_limit = 10000

        while sys.getsizeof(text) > self.text_limit:
            text = text[:-1000]

        self.data = text[:]
        self.json_data = 0

    def analyze_tone(self):
        self.json_data = self.__analyze_tone()

        json_analyze = self.json_data[:]

        return self.__transform_results(json_analyze)

    def __analyze_tone(self):
        try:
            result = requests.post(self.watson_url, auth=(self.username, self.password),
                                   headers=self.headers, data=self.data.encode('utf8'))
            return result.text
        except():
            return False

    def plotting(self):
        data = json.loads(str(self.json_data[:]))

        for cathegory in data['document_tone']['tone_categories']:
            chart = pygal.Pie()

            chart.title = cathegory['category_name']
            tone_names = []
            number_data = []
            for tone in cathegory['tones']:
                tone_names.append(tone['tone_name'])
                number_data.append(int(round(tone['score'] * 100, 1)))

            summ = 1
            for tone_number in number_data:
                summ += tone_number

            for tone_number in number_data:
                tone_number /= summ

            i = 0
            while i < len(tone_names):
                chart.add(tone_names[i], number_data[i])
                i += 1

            chart.render_to_png(cathegory['category_name'] + '.png')

    def __transform_results(self, json_analyze):
        analyze = json.loads(str(json_analyze))
        text_answer = ''
        for cathegory in analyze['document_tone']['tone_categories']:
            text_answer += cathegory['category_name'] + '\n' + ("-" * len(cathegory['category_name'])) + '\n'
            for tone in cathegory['tones']:
                text_answer += tone['tone_name'].ljust(20) + (str(round(tone['score'] * 100, 1)) + "%").ljust(10) + '\n'
            text_answer += '\n'
        return text_answer

