from html.parser import HTMLParser
from itertools import product


class PriceParser(HTMLParser):
    def __init__(self):
        super(PriceParser, self).__init__()
        self.current_tag = None
        self.current_class = None
        self.current_id = None
        self.price = dict()

    def handle_starttag(self, tag, attrs):
        self.current_class = None
        self.current_id = None
        self.current_tag = tag

        for attr, value in attrs:
            if attr == 'class':
                self.current_class = value
            if attr == 'id':
                self.current_id = value

    def handle_endtag(self, tag):
        self.current_tag = "end" + tag

    def handle_data(self, data):
        if self.current_tag == 'span' and self.current_class == 'sum':
            self.price['price'] = data.replace("\xa0", "")

        if self.current_tag == 'span' and self.current_class == 'currency':
            self.price['currency'] = data

    def get_price(self, raw):
        self.feed(raw)
        return self.price


price_parser = PriceParser()


class QueryBuilder(object):
    def __init__(self, symbols_list, max_length):
        self.symbols_list = symbols_list
        self.max_length = max_length

    def get_all_words_gen(self):
        for unique_combination in product(self.symbols_list, repeat=self.max_length):
            yield "".join(unique_combination)

    def get_words_gen(self, latest=None):
        combinations = product(self.symbols_list, repeat=self.max_length)
        combinations_list = list(combinations)
        start_index = None
        if latest:
            latest = tuple(latest)
            start_index = combinations_list.index(latest) + 1

        for unique_combination in combinations_list[start_index: ]:
            yield "".join(unique_combination)
