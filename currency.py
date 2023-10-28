import aiohttp
import asyncio
import argparse
import datetime

class CurrencyConverter:
    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch_exchange_rates(self, days, currencies):
        async with aiohttp.ClientSession() as session:
            exchange_rates = []
            for day in range(1, min(days, 10) + 1):
                current_date = (datetime.datetime.now() - datetime.timedelta(days=day)).date()
                current_date_str = current_date.strftime('%d.%m.%Y')
                url = f"{self.api_url}/p24api/exchange_rates?json&date={current_date_str}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        exchangeRate = data.get('exchangeRate')
                        rates = {}
                        for rate in exchangeRate:
                            currency = rate.get("currency")
                            if currency in currencies:
                                rates[currency] = f"SALE {rate.get('saleRateNB')} BUY {rate.get('purchaseRateNB')}"
                        exchange_rates.append({current_date_str: rates})
            return exchange_rates

def main():
    parser = argparse.ArgumentParser(description="Retrieve exchange rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to retrieve exchange rates for")
    parser.add_argument("--currencies", nargs="+", default=["EUR", "USD"], help="Additional currencies to retrieve")

    args = parser.parse_args()
    days = args.days
    currencies = args.currencies

    api_url = "https://api.privatbank.ua"

    converter = CurrencyConverter(api_url)

    loop = asyncio.get_event_loop()
    exchange_rates = loop.run_until_complete(converter.fetch_exchange_rates(days, currencies))

    for rate in exchange_rates:
        print(rate)

if __name__ == "__main__":
    main()