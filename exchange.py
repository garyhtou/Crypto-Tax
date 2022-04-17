from kucoin.base_request.base_request import KucoinBaseRestApi
import pandas as pd


class KuCoinExchange:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = KucoinBaseRestApi(api_key, api_secret, api_passphrase)

    def get_settled_lend_order_history(self, cached=True):
        if cached:
            return pd.read_csv('kucoin_lending.csv')

        # Get data from KuCoin API
        json = self._api_get_settled_lend_order_history()
        df = pd.json_normalize(json)

        # Cache as CSV
        df.to_csv('kucoin_lending.csv', encoding='utf-8', index=False)
        return df

    def _api_get_settled_lend_order_history(self):
        """
        Get data from KuCoin API
        https://docs.kucoin.com/#get-settled-lend-order-history
        """
        page = 1
        per_page = 50
        total_pages = 0

        items = []

        while page <= total_pages or not total_pages:
            if total_pages:
                print(f'Fetching page {page} of {total_pages}')
            else:
                print(f'Fetching page {page}')

            res = self.client._request('GET',
                                       '/api/v1/margin/lend/trade/settled',
                                       params={'currentPage': page,
                                               'pageSize': per_page})
            print(res, '\n')
            items.extend(res['items'])

            total_pages = res['totalPage']
            page += 1

        return items
