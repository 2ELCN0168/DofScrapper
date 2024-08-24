import asyncio
import os

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from modules.images.scan_pages import fetch_page, normalize_string


async def download_image(session, url, save_path):
    async with session.get(url) as response:
        response.raise_for_status()
        async with aiofiles.open(save_path, "wb") as f:
            await f.write(await response.read())


async def process_url(session, url, sub_category_dir):
    save_path = None
    try:
        page_content = await fetch_page(session, url)
        soup = BeautifulSoup(page_content, "html.parser")

        # Extract the item ID and name for the filename
        item_id = url.split("/")[-1]

        # Filename construction
        image_name = f"{url.split('/')[-1]}.png"
        save_path = os.path.join(sub_category_dir, image_name)

        # Attempt to find and download the item's image
        image_div = soup.find("div", class_="ak-encyclo-detail-illu")
        if image_div:
            image_tag = image_div.find("img")
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]
                await download_image(session, image_url, save_path)
                print(f"Downloaded: {image_url} to {save_path}")
            else:
                raise aiohttp.ClientResponseError(
                    request_info=None,
                    history=None,
                    status=404,
                    message="No image tag found",
                    headers=None,
                )
        else:
            raise aiohttp.ClientResponseError(
                request_info=None,
                history=None,
                status=404,
                message="No image div found",
                headers=None,
            )

    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            print(f"Image not found, downloading default image for: {url}")
            if save_path is None:
                item_id = url.split("/")[-1]
                image_name = f"{item_id}.png"
                save_path = os.path.join(sub_category_dir, image_name)
            default_image_url = (
                "https://static.ankama.com/dofus/www/game/items/200/0.png"
            )
            await download_image(session, default_image_url, save_path)
            print(f"Downloaded default image to {save_path}")
        else:
            print(f"Error fetching {url}: {e}")


#
# async def download_images_for_category(session, category_name, urls):
#     for sub_category, links in urls.items():
#         sub_category_dir = os.path.join("encyclopedie", category_name, sub_category)
#         os.makedirs("encyclopedie", exist_ok=True)
#         os.makedirs(sub_category_dir, exist_ok=True)
#
#         # Run downloads concurrently
#         tasks = [process_url(session, url, sub_category_dir) for url in links]
#         await asyncio.gather(*tasks)


async def download_images_for_category(session, category_name, urls):
    semaphore = asyncio.Semaphore(1)  # Limit to 5 concurrent downloads

    async def sem_process_url(url, sub_category_dir):
        async with semaphore:
            await process_url(session, url, sub_category_dir)

    for sub_category, links in urls.items():
        sub_category_dir = os.path.join("encyclopedie", category_name, sub_category)
        os.makedirs("encyclopedie", exist_ok=True)
        os.makedirs(sub_category_dir, exist_ok=True)

        # Run downloads concurrently with a limit
        tasks = [sem_process_url(url, sub_category_dir) for url in links]
        await asyncio.gather(*tasks)
