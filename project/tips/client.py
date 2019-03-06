import aiohttp
import json
from database import AsyncDatabaseManager
from tips.db_schema import Category, Product, Tip, Query
from tips.helpers import price_parser


db_manager = AsyncDatabaseManager()


class TipsClient(object):

    def __init__(self, api_host, api_url, query_builder):

        self.api_host = api_host
        self.api_url = api_url
        self.query_builer = query_builder

    async def get_query_words(self):

        latest = await db_manager.get_latest(Tip)
        query_words_gen = self.query_builer.get_words_gen(latest=latest.text_query)

        return query_words_gen

    async def get_url(self):
        return self.api_host + self.api_url

    async def fetch(self, session, url, query_params):

        async with session.get(url, params=query_params) as response:
            return await response.text()

    async def main(self):
        url = await self.get_url()
        query_words = await self.get_query_words()

        for query_word in query_words:
            query_param = {'q': query_word}

            async with aiohttp.ClientSession() as session:
                response_data = await self.fetch(session, url, query_param)

                try:
                    response = json.loads(response_data)

                    if response:
                        categories = response.get('categories', [])
                        products = response.get('products', [])
                        queries = response.get('query', [])

                        tip = await self.create_tip(query_word, categories, products, queries)
                        print("Tip for query word \'%s\'successfully crated" % tip.text_query)

                    else:
                        print("Empty response for query \'%s\'" % query_word)

                except json.decoder.JSONDecodeError:
                    print("Response object \'%s \'is not serializable" % response_data)
        return

    @staticmethod
    async def create_tip(query_word,  categories, products, queries):

        category_instances = []
        for category in categories:
            category['external_id'] = category.pop('id')
            category_instance = await db_manager.get_or_create(Category, **category)
            if category_instance:
                category_instances.append(category_instance)

        product_instances = []
        for product in products:
            product['url'] = "https:" + product['url']

            price = price_parser.get_price(product.get('price', ''))
            special_price = price_parser.get_price(product.get('special_price', ''))

            product['price'] = price['price'] if price else None
            product['special_price'] = special_price['price'] if special_price else None
            product['currency'] = price['currency'] if price else None

            product_instance = await db_manager.get_or_create(Product, **product)

            if product_instance:
                product_instances.append(product_instance)

        query_instances = []
        for query in queries:
            query_instance = await db_manager.get_or_create(Query, text_query=query)

            if query_instance:
                query_instances.append(query_instance)

        tip_kwargs = {
            'category': category_instances,
            'product': product_instances,
            'query': query_instances,
            'text_query': query_word
        }

        tip = await db_manager.create(Tip, **tip_kwargs)

        return tip
