import aiohttp
import config

animes_cache = []
fansubs_cache = []
entries_cache = []


async def fetch_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


def extract_items(data):
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    return data


async def fetch_animes():
    global animes_cache
    if animes_cache:
        return animes_cache
    animes_cache = await fetch_all_pages(config.ANIMES_URL)
    return animes_cache


async def fetch_fansubs():
    global fansubs_cache
    if fansubs_cache:
        return fansubs_cache
    fansubs_cache = await fetch_all_pages(config.FANSUBS_URL)
    return fansubs_cache


async def fetch_entries():
    global entries_cache
    if entries_cache:
        return entries_cache
    entries_cache = await fetch_all_pages(config.ENTRIES_URL)
    return entries_cache


async def fetch_all_pages(base_url: str, per_page: int = 100):
    all_items = []
    page = 1
    while True:
        url = f"{base_url}?page={page}&perPage={per_page}"
        data = await fetch_json(url)
        items = extract_items(data)
        if not items:
            break
        all_items.extend(items)
        if isinstance(data, dict):
            total_pages = data.get("totalPages", 1)
            if page >= total_pages:
                break
        else:
            break
        page += 1
    return all_items


async def fetch_anilist_data(anilist_id: int):
    query = """
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            startDate {
                year
            }
            coverImage {
                large
            }
        }
    }
    """
    variables = {"id": anilist_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(config.ANILIST_URL, json={"query": query, "variables": variables}) as resp:
            data = await resp.json()
            return data.get("data", {}).get("Media")


def generate_short_id(anime_id: str) -> str:
    hash_val = 0
    for c in anime_id:
        hash_val = (hash_val * 31 + ord(c)) % 100000
    return str(hash_val).zfill(5)


async def refresh_caches():
    global animes_cache, fansubs_cache, entries_cache
    print("Refrescando cachés de la API...")
    try:
        animes_cache = await fetch_all_pages(config.ANIMES_URL)
        fansubs_cache = await fetch_all_pages(config.FANSUBS_URL)
        entries_cache = await fetch_all_pages(config.ENTRIES_URL)
        print("Cachés actualizados correctamente.")
    except Exception as e:
        print(f"Error al refrescar cachés: {e}")