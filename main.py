import os
from dotenv import load_dotenv
from exchange import KuCoinExchange
import pandas as pd
import datetime as dt
from decimal import Decimal

load_dotenv()
KUCOIN_API_KEY = os.getenv('KUCOIN_API_KEY')
KUCOIN_API_SECRET = os.getenv('KUCOIN_API_SECRET')
KUCOIN_API_PASSPHRASE = os.getenv('KUCOIN_API_PASSPHRASE')


def koinly_format(lending):
    # REQUIRED: Koinly Date, Amount, Currency
    # OPTIONAL: Net Worth Amount, Net Worth Currency, Label, Description, TxHash
    arr = lending.to_numpy()

    size_sum = Decimal(0)
    interest_sum = Decimal(0)
    repaid_sum = Decimal(0)

    data = []
    for row in arr:
        trade_id, currency, size, interest, repaid, daily_int_rate, term, settled_at, note = row
        data.append(
            {
                'Koinly Date': dt.datetime.utcfromtimestamp(
                    settled_at / 1000.0).isoformat(),
                'Amount': float(Decimal(repaid) - Decimal(size)),
                'Currency': currency,
                'Label': 'Loan interest',
                'Description': f'Trade ID: {trade_id}, Interest: {interest}, Daily Interest Rate: {daily_int_rate}, Term: {term}, Note: {note}',
            }
        )
        size_sum += Decimal(size)
        interest_sum += Decimal(interest)
        repaid_sum += Decimal(repaid)

    print(f'Total size: {size_sum}')
    print(f'Total interest: {interest_sum}')
    print(f'Total repaid: {repaid_sum}')
    print(f'Total amount: {repaid_sum - size_sum}')

    return pd.DataFrame(data)


if __name__ == '__main__':
    kce = KuCoinExchange(KUCOIN_API_KEY, KUCOIN_API_SECRET,
                         KUCOIN_API_PASSPHRASE)
    lending = kce.get_settled_lend_order_history(cached=False)
    print(lending)

    # Converting to Koinly format
    koinly_df = koinly_format(lending)
    print(koinly_df)

    # Saving to CSV
    koinly_df.to_csv('koinly_kucoin_lending.csv', index=False)
