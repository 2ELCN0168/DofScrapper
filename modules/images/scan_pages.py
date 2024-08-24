import asyncio
import json
import os
import unicodedata

import aiohttp
from bs4 import BeautifulSoup

from modules.headers import get_headers


def normalize_string(input_str):
    normalized = input_str.lower()
    normalized = (
        unicodedata.normalize("NFKD", normalized)
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    normalized = normalized.replace(" ", "_").replace("'", "_")
    return normalized


async def fetch_page(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def scan_all_pages_for_filter(
    session, base_url, filter_id, category_name, sub_category_name, json_file
):
    page = 1
    items_found = True

    while items_found:
        paginated_url = f"{base_url}?type_id%5B%5D={filter_id}&page={page}"
        if base_url == "https://www.dofus.com/fr/mmorpg/encyclopedie/monstres":
            paginated_url = (
                f"{base_url}?text=&monster_category%5B%5D={filter_id}&page={page}"
            )
        elif base_url == "https://www.dofus.com/fr/mmorpg/encyclopedie/montures":
            paginated_url = f"{base_url}?&model_family_id%5B%5D={filter_id}&page={page}"

        print(f"Scanning URL: {paginated_url}")

        page_content = await fetch_page(session, paginated_url)
        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("table", class_="ak-table ak-responsivetable")
        items = table.find_all("span", class_="ak-linker") if table else []

        print(f"Found {len(items)} items on page {page} for {sub_category_name}")

        if len(items) == 0:
            items_found = False
            break

        data = load_existing_data(json_file)
        normalized_category_name = normalize_string(category_name)
        normalized_sub_category_name = normalize_string(sub_category_name)

        if normalized_category_name not in data:
            data[normalized_category_name] = {}
        if normalized_sub_category_name not in data[normalized_category_name]:
            data[normalized_category_name][normalized_sub_category_name] = []

        for item in items:
            link = item.find("a")
            if link:
                item_link = "https://www.dofus.com" + link["href"]
                if (
                    item_link
                    not in data[normalized_category_name][normalized_sub_category_name]
                ):
                    item_name = normalize_string(link.text.strip())
                    print(f"Found item: {item_name} -> {item_link}")
                    data[normalized_category_name][normalized_sub_category_name].append(
                        item_link
                    )

        save_data(json_file, data)
        page += 1

    print(f"Finished scanning for filter {sub_category_name}")


def load_existing_data(json_file):
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            print(f"Loading existing JSON data from {json_file}")
            return json.load(f)
    print("No existing JSON file found, creating new data structure")
    return {}


def save_data(json_file, data):
    # Trier les noms des familles dans chaque catégorie
    sorted_data = {}
    for category, sub_categories in data.items():
        if isinstance(sub_categories, dict):
            sorted_sub_categories = {
                key: sub_categories[key] for key in sorted(sub_categories)
            }
        elif isinstance(sub_categories, list):
            sorted_sub_categories = sorted(sub_categories)
        else:
            sorted_sub_categories = sub_categories

        sorted_data[category] = sorted_sub_categories

    # Enregistrer les données triées
    with open(json_file, "w") as f:
        print(f"Saving data to {json_file}")
        json.dump(sorted_data, f, indent=4)


async def scan_category_without_filters(
    session, category_url, category_name, json_file
):
    print(f"Scanning category without filters: {category_name}")
    print(f"URL: {category_url}")

    items_found = True
    page = 1
    data = load_existing_data(json_file)
    normalized_category_name = normalize_string(category_name)

    while items_found:
        paginated_url = f"{category_url}?page={page}"
        page_content = await fetch_page(session, paginated_url)
        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("table", class_="ak-table ak-responsivetable")
        items = table.find_all("a") if table else []

        print(f"Found {len(items)} rows on page {page} in {category_name}")

        if len(items) == 0:
            items_found = False
            break

        if normalized_category_name not in data:
            data[normalized_category_name] = []

        for item in items:
            item_link = "https://www.dofus.com" + item["href"]
            item_name = normalize_string(item.text.strip())
            print(f"Found item: {item_name} -> {item_link}")
            if item_link not in data[normalized_category_name]:
                data[normalized_category_name].append(item_link)

        page += 1

    save_data(json_file, data)
    print(f"Finished scanning for category {category_name}")


async def scan_category_with_pagination(category_url, category_name, json_file):
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        print(f"Scanning category: {category_name}")
        print(f"URL: {category_url}")

        page_content = await fetch_page(session, category_url)
        soup = BeautifulSoup(page_content, "html.parser")

        filters_section = soup.find("div", {"data-name": "item_type_id"})
        if category_name == "compagnons":
            await scan_category_without_filters(
                session, category_url, category_name, json_file
            )
            return

        if category_url == "https://www.dofus.com/fr/mmorpg/encyclopedie/monstres":
            filters_section = soup.find("div", {"data-name": "item_monster_category"})
        elif category_url == "https://www.dofus.com/fr/mmorpg/encyclopedie/montures":
            filters_section = soup.find("div", {"data-name": "item_model_family_id"})

        if not filters_section:
            print("No filters found!")
            return

        item_types = filters_section.find_all("label", class_="ak-label")
        print(f"Found {len(item_types)} filters in {category_name}")

        tasks = []
        for item_type in item_types:
            sub_category_name = (
                item_type.text.strip().lower().replace(" ", "_").replace("'", "_")
            )
            filter_value = item_type["for"].split("_")[-1]

            tasks.append(
                scan_all_pages_for_filter(
                    session,
                    category_url,
                    filter_value,
                    category_name,
                    sub_category_name,
                    json_file,
                )
            )

        await asyncio.gather(*tasks)
