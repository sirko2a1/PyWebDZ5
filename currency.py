import aiohttp
import asyncio
import argparse
import datetime

class CurrencyConverter:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    async def fetch_exchange_rates(self, days, currencies):
        async with aiohttp.ClientSession() as session:
            exchange_rates = []
            for day in range(1, min(days, 10) + 1):
                current_date = (datetime.datetime.now() - datetime.timedelta(days=day)).date()
                url = f"{self.api_url}/p24api/exchange_rates?json&date={current_date}"
                async with session.get(url, headers={"Authorization": f"Bearer {self.api_key}"}) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates = {
                            current_date.strftime('%d.%m.%Y'): {currency: data[currency] for currency in currencies}
                        }
                        exchange_rates.append(rates)
            return exchange_rates

def main():
    parser = argparse.ArgumentParser(description="Retrieve exchange rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to retrieve exchange rates for")
    parser.add_argument("--currencies", nargs="+", default=["EUR", "USD"], help="Additional currencies to retrieve")

    args = parser.parse_args()
    days = args.days
    currencies = args.currencies

    api_url = "https://api.privatbank.ua/#p24/exchangeArchive"
    api_key = "YOUR_API_KEY"

    converter = CurrencyConverter(api_url, api_key)

    loop = asyncio.get_event_loop()
    exchange_rates = loop.run_until_complete(converter.fetch_exchange_rates(days, currencies))

    for rate in exchange_rates:
        print(rate)

if __name__ == "__main__":
    main()

