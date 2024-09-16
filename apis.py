import logging
import aiohttp

logger = logging.getLogger("main")

wows_warship_stat_ru = "https://api.worldofwarships.ru/wows/ships/stats/"
wows_warship_stat_eu = "https://api.worldofwarships.eu/wows/ships/stats/"
wows_warship_stat_na = "https://api.worldofwarships.com/wows/ships/stats/"
wows_warship_stat_asia = "https://api.worldofwarships.asia/wows/ships/stats/"

wows_clan_detail_ru = "https://api.worldofwarships.ru/wows/clans/info/"
wows_clan_detail_eu = "https://api.worldofwarships.eu/wows/clans/info/"
wows_clan_detail_na = "https://api.worldofwarships.na/wows/clans/info/"
wows_clan_detail_asia = "https://api.worldofwarships.asia/wows/clans/info/"

wows_account_player_personal_data_ru = (
    "https://api.worldofwarships.ru/wows/account/info/"
)
wows_account_player_personal_data_eu = (
    "https://api.worldofwarships.eu/wows/account/info/"
)
wows_account_player_personal_data_na = (
    "https://api.worldofwarships.com/wows/account/info/"
)
wows_account_player_personal_data_asia = (
    "https://api.worldofwarships.asia/wows/account/info/"
)


async def api_get_player_ship_data(
    session: aiohttp.ClientSession,
    account_id: str,
    server: int,
    application_id: str,
) -> dict:
    """
    :param session: aiohttp ClientSession
    :param account_id: account_id
    :param server: 服务器 0-3 依次是 亚服 毛服 欧服 美服
    :param application_id
    :return resp.json: json
    """
    API = ""
    match server:
        case 0:
            API = wows_warship_stat_asia
        case 1:
            API = wows_warship_stat_ru
        case 2:
            API = wows_warship_stat_eu
        case 3:
            API = wows_warship_stat_na
    params = [("application_id", application_id), ("account_id", account_id)]
    async with session.get(API, params=params) as resp:
        if 200 == resp.status:
            data = await resp.json()
            if data["status"] == "ok":
                return data["data"]
            else:
                logging.error(
                    f"wargaming status not ok, parmas: {params}", stack_info=True
                )
                logging.error(f"respons data: {data}", stack_info=True)
        else:
            logging.error(f"http code not 200 OK, parmas: {params}", stack_info=True)
            logging.error(f"http code == {resp.status}", stack_info=True)


async def api_get_clan_detail(
    session: aiohttp.ClientSession,
    clan_id: str,
    server: int,
    application_id: str,
) -> dict:
    """
    :param session: aiohttp ClientSession
    :param clan_id: clan_id or ids
    :param server: 服务器 0-3 依次是 亚服 毛服 欧服 美服
    :param application_id
    :return resp.json: json
    """
    API = ""
    match server:
        case 0:
            API = wows_clan_detail_asia
        case 1:
            API = wows_clan_detail_ru
        case 2:
            API = wows_clan_detail_eu
        case 3:
            API = wows_clan_detail_na
    params = [("application_id", application_id), ("clan_id", clan_id)]
    async with session.get(API, params=params) as resp:
        if 200 == resp.status:
            data = await resp.json()
            if data["status"] == "ok":
                return data["data"]
            else:
                logging.error(
                    f"wargaming status not ok, parmas: {params}", stack_info=True
                )
                logging.error(f"respons data: {data}", stack_info=True)
        else:
            logging.error(f"http code not 200 OK, parmas: {params}", stack_info=True)
            logging.error(f"http code == {resp.status}", stack_info=True)


async def api_get_play_personal_data(
    session: aiohttp.ClientSession,
    account_id: str,
    server: int,
    application_id: str,
) -> dict:
    """
    :param session: aiohttp 的 ClientSession
    :param account_id: 用户的 account_id
    :param server: 服务器 0-3 依次是 亚服 毛服 欧服 美服
    :param application_id
    :return resp.json: json
    """
    API = ""
    match server:
        case 0:
            API = wows_account_player_personal_data_asia
        case 1:
            API = wows_account_player_personal_data_ru
        case 2:
            API = wows_account_player_personal_data_eu
        case 3:
            API = wows_account_player_personal_data_na

    params = [("application_id", application_id), ("account_id", account_id)]

    async with session.get(API, params=params) as resp:
        if 200 == resp.status:
            data = await resp.json()
            if data["status"] == "ok":
                return data["data"]
            else:
                logging.error(
                    f"wargaming status not ok, parmas: {params}", stack_info=True
                )
                logging.error(f"respons data: {data}", stack_info=True)
        else:
            logging.error(f"http code not 200 OK, parmas: {params}", stack_info=True)
            logging.error(f"http code == {resp.status}", stack_info=True)
