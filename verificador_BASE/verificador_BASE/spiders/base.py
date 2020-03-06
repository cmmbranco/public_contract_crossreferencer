from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re
from verificador_BASE.items import VerificadorBaseItem


nif_pattern = re.compile('[0-9]{9}')



class BaseSpider(CrawlSpider):
    name = 'base'
    allowed_domains = ['www.base.gov.pt']


    ##
    ## Add refined urls here
    ##
    start_urls = ['http://www.base.gov.pt/Base/pt/ResultadosPesquisa?type=contratos&query=texto%3D%26tipo%3D0%26tipocontrato%3D0%26cpv%3D%26numeroanuncio%3D%26aqinfo%3D%26adjudicante%3D%26adjudicataria%3D%26desdeprecocontrato_false%3D%26desdeprecocontrato%3D%26ateprecocontrato_false%3D%26ateprecocontrato%3D%26desdedatacontrato%3D%26atedatacontrato%3D%26desdedatapublicacao%3D2019-08-28%26atedatapublicacao%3D%26desdeprazoexecucao%3D%26ateprazoexecucao%3D%26desdedatafecho%3D%26atedatafecho%3D%26desdeprecoefectivo_false%3D%26desdeprecoefectivo%3D%26ateprecoefectivo_false%3D%26ateprecoefectivo%3D%26pais%3D0%26distrito%3D0%26concelho%3D0',

    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.prev',), restrict_text=('Próxima')),
             callback="parse_prox",
             follow=True),)



    def parse_prox(self, response):

        print('Processing..' + response.url + '\n')

        item_links = response.css('.plusSign > ::attr(href)').extract()
        for item in item_links:
            #yield Request(item, callback=self.parse_contract)
            yield Request(item, callback=self.parse_contract)
            #print(Request(item))

    def parse_contract(self,response):

        table = response.xpath('//*[@id="pesquisaInci"]//tbody').xpath('//tr')


        for row in table:
            if "Tipo de procedimento" in row.extract():
                contract_type = row.xpath('//td')[1].extract()
            if "Entidade adjudicatária - Nome, NIF" in row.extract():
                entity_nif = row.xpath('//td')[1].extract()
            if "Preço contratual" in row.extract()  :
                price = row.xpath('//td')[1].extract()

        print(contract_type)
        print(entity_nif)
        print(price)

        table_as_string = response.css('table').extract()[0]

        matches = nif_pattern.findall(table_as_string)


        #contract_type = response.css('[id="pesquisaInci"]').css('tr')[2].css('td')[1].extract()

        #regex to remove td tags
        contract_type = re.sub(r'<\/?td>', '',contract_type)
        contract_stripped = re.sub(r'<.+?>', '',contract_type)


        value = response.css('[id="pesquisaInci"]').css('tr')[12].css('td')[1].extract()
        #regex to remove td tags
        value = re.sub(r'<\/?td>', '',value)
        value_stripped = re.sub(r'<.+?>', '',value)


        #If more than one NIF shows up it's because contract was attributed
        if len(matches) >= 2:

            contract = response.url
            orig = matches[0]
            winner = matches[1]

            item = VerificadorBaseItem()
            item['contract_url'] = contract
            item['poster_nif'] = orig
            item['winner_nif'] = winner
            item['procedimento'] = contract_stripped
            item['contract_value'] = value_stripped
            return item


        else:

            item = VerificadorBaseItem()
            item['contract_url'] = contract
            item['poster_nif'] = 'NA'
            item['winner_nif'] = 'NA'
            item['procedimento'] = 'NA'
            item['contract_value'] = 'NA'
            return item
