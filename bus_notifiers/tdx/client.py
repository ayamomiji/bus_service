import httpx

from . import access_token


def get_route(route_name, top=30, skip=0):
    url = (
        f"https://tdx.transportdata.tw/api/basic/v2/Bus/Route/City/Taipei/{route_name}"
    )
    return _get(url, top, skip)


def get_stop_of_route(route_name, top=30, skip=0):
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{route_name}"
    return _get(url, top, skip)


def get_route_near_stop(route_name, top, skip):
    return _get(url, top, skip)


def _get(url, top=30, skip=0, filter=None):
    params = {
        "$top": top,
        "$skip": skip,
        "format": "JSON",
    }
    if filter is not None:
        params["$filter"] = filter
    r = httpx.get(
        url,
        params=params,
        headers={"authorization": f"Bearer {access_token.get()}"},
    )
    if r.status_code == 429:
        raise TooManyRequests
    return r.json()


class TooManyRequests(Exception):
    pass
