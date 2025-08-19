from topics.market_overview import market_overview


def get_market_info(get_overview: bool):
    """
        Calls nodes
    """
    if get_overview:
        market_overview("India", "Rice")


{
    "market_overview": {
        "gdp": {
            "val": "10000 Deneg",
            "source": "mamy.net"
        }
    },
    "market_players": {
        "players": [
            {
                "name": "Sos uxuy inc.",
                "info": "info",
                "members": [
                    "..."
                ]
            }
        ],
    }
}
