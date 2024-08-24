import asyncio

import aiohttp


async def send_request(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            status = response.status
            return status
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None


async def test_server(url, headers, start_requests, step, max_requests):
    async with aiohttp.ClientSession() as session:
        current_requests = start_requests
        max_safe_requests = start_requests

        while current_requests <= max_requests:
            print(f"Testing with {current_requests} concurrent requests...")
            tasks = [
                send_request(session, url, headers) for _ in range(current_requests)
            ]
            responses = await asyncio.gather(*tasks)

            # Check if any of the responses returned a 403 status code
            if 403 in responses:
                print(
                    f"Server started returning 403 with {current_requests} concurrent requests."
                )
                break
            else:
                print(f"No 403 detected with {current_requests} concurrent requests.")
                max_safe_requests = current_requests

            current_requests += step
            await asyncio.sleep(
                1
            )  # small delay between tests to be gentle on the server

        return max_safe_requests


if __name__ == "__main__":
    # URL of the server you want to test
    url = "https://www.dofus.com/fr"  # Replace with the target URL

    # HTTP headers to include in the requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # Initial number of concurrent requests
    start_requests = 1

    # Step by which to increase the number of requests
    step = 5

    # Maximum number of concurrent requests to test
    max_requests = 100  # Adjust as needed

    # Run the test
    max_safe_requests = asyncio.run(
        test_server(url, headers, start_requests, step, max_requests)
    )

    print(
        f"\nThe maximum number of concurrent requests without triggering a 403 is: {max_safe_requests}"
    )
