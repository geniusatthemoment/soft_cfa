import asyncio
import re
from playwright.async_api import async_playwright

async def get_debank_balance(page, address: str) -> str:
    url = f"https://debank.com/profile/{address}"
    await page.goto(url)
    await page.wait_for_selector('.HeaderInfo_totalAssetInner__HyrdC')
    await asyncio.sleep(2)
    element = await page.query_selector('.HeaderInfo_totalAssetInner__HyrdC')
    text = await element.inner_text() if element else "Не найдено"
    return text.strip()

async def main():
    total = 0
    with open("adresses.txt", "r") as f:
        addresses = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []
        for address in addresses:
            balance = await get_debank_balance(page, address)
            balance = int(re.search(r"\$+\s*([^\+\-]+)", balance).group(1).strip())
            total+=balance
            print(f"{address}: ${balance}")
            results.append(f"{address}: ${balance}")
        print(f"Total: ${total}")
        await browser.close()

    with open("balances.txt", "w") as f:
        f.write("\n".join(results))
        f.write(f"\nTotal: ${total}")

if __name__ == "__main__":
    asyncio.run(main())

