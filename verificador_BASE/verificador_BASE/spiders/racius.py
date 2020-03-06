# -*- coding: utf-8 -*-
import pandas
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from verificador_BASE.items import RaciusItem
import re


DATA_AUTARQUICAS = '01/10/2017'
nif_pattern = re.compile('[0-9]{9}')

class RaciusSpider(CrawlSpider):
    name = 'racius'
    allowed_domains = ['www.racius.com']

    start_urls = ['http://www.racius.com/']



    # rules = (
    #     Rule(LinkExtractor(allow=(), restrict_css=('.title',),
    #          callback="parse_req",
    #          follow=True),)


    def parse(self,response):

        colnames = ['contract_url', 'flagged', 'poster_nif', 'winner_nif']
        try:
            data = pandas.read_csv('data.csv', names=colnames)

            contract_urls = data.contract_url.tolist()
            winner_nifs = data.winner_nif.tolist()


            first = True

            for numb in winner_nifs:

                if first:
                    ##Skip first line as it contains headers
                    first = False

                else:

                    prepared_query = 'https://www.racius.com/pesquisa/?q=' + numb +'&tipo=empresas'
                    #print(prepared_query + '\n')
                    yield Request(url=prepared_query, callback=self.parse_resp)


        except:
            pass



    def parse_resp(self, response):

        #print('Processing 1..' + response.url + '\n')

        ##Should only have one match therefore only the first is used

        try:
            #print(response.css('a.title::attr(href)').extract()[0])
            item = response.css('a.title::attr(href)').extract()[0]

            prepared_query = 'https://www.racius.com' + item
            #print(prepared_query)

            yield Request(url=prepared_query, callback=self.parse_creation)

        except:
            ##Nif was not found therefore out of bound exception

            #print("NIF NOT FOUND")

            contract = nif_pattern.findall(response.url)

            item = RaciusItem()
            item['nif'] = contract
            item['creation_date'] = 'NA'
            return item


            pass


    def parse_creation(self,response):

        #print('Processing 2..' + response.url + '\n')



        table_as_string = response.css('.company-table-block').css('.table').css('.company-table-content').extract()[0]

        matches = nif_pattern.findall(table_as_string)

        creation = response.css('.company-table-block').css('.table').css('tr')[2].css('td')[1].extract()

        #regex to remove td tags
        creation = re.sub(r'<\/?td>', '',creation)
        creation_stripped = re.sub(r'<.+?>', '',creation)



        #print("CREATION: " + creation_stripped + '\n')

        item = RaciusItem()
        item['nif'] = matches
        item['creation_date'] = creation_stripped
        return item
