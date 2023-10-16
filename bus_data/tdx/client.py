import httpx

from bus_data.tdx import access_token

STOP_OF_ROUTE_URL = (
    "https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei"
)


def get_stops_of_routes(top, skip):
    r = httpx.get(
        STOP_OF_ROUTE_URL,
        params={
            "$top": top,
            "$skip": skip,
            "format": "JSON",
        },
        headers={"authorization": f"Bearer {access_token.get()}"},
    )
    return r.json()
