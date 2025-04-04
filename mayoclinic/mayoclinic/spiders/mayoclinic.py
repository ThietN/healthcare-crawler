
# python3 -m venv venvName ---> to create environment in python no need the 
# pip install scrapy create a venv and install required liberaries
# venv\scripts\activate.bat ---> to activate it 
# cd Mayoclinic ---> cd to the upper level folder of project
# scrapy  crawl --loglevel INFO -O output.json:json mayoclinic --> To run the program



from pathlib import Path
import urllib.parse 
import json

import scrapy


class MayoclinicSpider(scrapy.Spider):
    name = 'mayoclinic'

    def start_requests(self):
        base_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter=%s'
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#':
            yield scrapy.Request(url=base_url % urllib.parse.quote_plus(c), callback=self.parse)

    def parse(self, response):
        links = response.css('#cmp-skip-to-main__content a')
        yield from response.follow_all(links, callback=self.parse_disease)

    def parse_disease(self, response):
        title = response.css('h1 a::text').get()
        if title is None:
            title = response.css('h1::text').get()
        if title is None:
            with open('notitle.txt', 'a') as fp:
                fp.write(response.url + '\n')
            return
        # To open symptom tab for those pages with no symptom tag 
        if response.xpath('//h2[contains(text(), "Symptoms")] | //h3[contains(text(), "Symptoms")]').get() is None:
            symptoms_tab = response.css('a#et_genericNavigation_symptoms-causes')
            if symptoms_tab.get() is None:
                with open('nosymps.txt', 'a') as fp:
                    fp.write(f'{response.url}\n')
            yield from response.follow_all(symptoms_tab, callback=self.parse_disease)
            return

        content = response.xpath('//article//section[contains(*//h2/text() | *//h3/text(), "Symptoms")]').get()
        if not content:
            content = response.css('.content').get()

        yield {
            'url': response.url,
            'title': title,
            'content': content,
        }

