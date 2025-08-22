from topics.market_companies import MarketCompanies
from utils import MarketQuery
from loguru import logger

# TODO add logs retention/rotation, separate folder
logger.add("logs.txt")


def main():
    country = input("Country: ")
    category = input("Category: ")

    query = MarketQuery(country=country, category=category)

    companies = MarketCompanies()

    companies.retrieve(query)
    companies.to_json()


if __name__ == '__main__':
    main()
