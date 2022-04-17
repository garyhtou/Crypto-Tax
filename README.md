# Crypto Tax

<sub>⚠️ use at ur own risk. i've got no accounting/tax experience :)</sub>

## KuCoin Lending Export Tool

Koinly doesn't seem to be able to export lending data and KuCoin's Python SDK doesn't have a supported method for
exporting details on each individual loan. (oh yeah, and KuCoin doesn't given you an option to export it from their website 🙄)

This short python script uses the KuCoin API to export all **Settled Lending Orders** and saves it to a CSV file. It
will also create
another version which conforms to Koinly's CSV import
format ([Koinly's format](https://help.koinly.io/en/articles/3662999-how-to-create-a-custom-csv-file-with-your-data)).

The script uses the official KuCoin Python SDK to handle authentication and send API calls to this KuCoin API
endpoint: `/api/v1/margin/lend/trade/settled`. (https://docs.kucoin.com/#get-settled-lend-order-history)

KuCoin API keys are required. Create an API key with the "Trade" permission and add the API key, secret, and passphrase
to the `.env` file.<br/>
I've got no idea why Kuoin required Trade permission for this endpoint ¯\_(ツ)_/¯
<img width="737" alt="image" src="https://user-images.githubusercontent.com/20099646/163720276-8ab553ee-f858-4929-89c9-35a0949e2100.png">
