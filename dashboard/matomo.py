import requests

def get_matomo_daily(matomo_url, token_auth, idsite, start_date, end_date):

    endpoint = f"{matomo_url}/?module=API&method=VisitsSummary.get"

    params = {
        "idSite": idsite,
        "period": "day",
        "date": f"{start_date},{end_date}",
        "format": "JSON",
        "filter_limit": "-1"
    }

    data = {
        "token_auth": token_auth
    }

    response = requests.post(endpoint, params=params, data=data)
    response.raise_for_status()

    return response.json()


# MATOMO_URL = "https://matomo.webpoosh.org"
# TOKEN = "da99186bc9fa8c529d10688356a2ad3e"
# ID_SITE = 1
# start = "2025-11-01"
# end = "2025-11-10"

# result = get_matomo_daily(MATOMO_URL, TOKEN, ID_SITE, start, end)
# print(result)
