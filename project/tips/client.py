import aiohttp
import json
from database import DatabaseManager
from tips.db_schema import Category, Product, Tip, Query
from tips.helpers import price_parser


db_manager = DatabaseManager()


class TipsClient(object):

    def __init__(self, api_host, api_url, query_builder):
        self.api_host = api_host
        self.api_url = api_url
        self.query_builder = query_builder

    async def get_url(self):
        return self.api_host + self.api_url

    async def fetch(self, session, url, query_params):
        async with session.get(url, params=query_params) as response:
            return await response.text()

    async def main(self):
        url = await self.get_url()

        for query_word in self.query_builder.get_words():
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
                    else:
                        print("Empty response")
                        continue

                except json.decoder.JSONDecodeError:
                    print("Response object \'%s \'is not serializable" % response_data)

                else:
                    print("Created Tip", tip)
        print("success")

    async def create_tip(self, query_word,  categories, products, queries):

        category_instances = []
        for category in categories:
            category['external_id'] = category.pop('id')
            instance = await db_manager.get_or_create(Category, **category)
            if instance:
                category_instances.append(instance)

        product_instances = []
        for product in products:
            product['url'] = "https:" + product['url']

            price = price_parser.get_price(product.get('price', ''))
            special_price = price_parser.get_price(product.get('special_price', ''))

            product['price'] = price['price'] if price else None
            product['special_price'] = special_price['price'] if special_price else None
            product['currency'] = price['currency'] if price else None

            instance = await db_manager.get_or_create(Product, **product)
            if instance:
                product_instances.append(instance)

        query_instances = []
        for query in queries:
            instance = await db_manager.get_or_create(Query, text_query=query)
            if instance:
                query_instances.append(instance)

        tip_kwargs = {
            'category': category_instances,
            'product': product_instances,
            'query': query_instances,
            'text_query': query_word
        }

        tip = Tip(**tip_kwargs)
        return tip
