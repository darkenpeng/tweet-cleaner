import asyncio
from playwright.async_api import async_playwright


async def main():
    nick = 'nickname'
    email = 'asdf@asdf.com'
    phone = '01000000000'
    password = 'password'

    async with async_playwright() as p:
        # Works across chromium, firefox and webkit
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(f'https://twitter.com/{nick}')

        await page.get_by_role('link', name="로그인").click()
        await page.get_by_role('textbox').fill(email)
        await page.get_by_role('button', name="다음").click()
        await page.get_by_role('textbox').fill(phone)
        await page.get_by_role('button', name="다음").click()
        await page.locator('input[type="password"]').fill(password)
        await page.get_by_role('button', name="로그인").click()

        await page.wait_for_timeout(5000)
        await page.goto(f'https://twitter.com/{nick}')
        await page.wait_for_timeout(10000)
        await page.get_by_role('article').first.text_content(timeout=10000)
        tweet = page.get_by_role('article').first
        while await tweet.is_visible():
            tweet = page.get_by_role('article').first
            if '내가 리트윗함' in await tweet.text_content():
                await tweet.get_by_role('button', name='리트윗').click()
                try:
                    await page.get_by_role('menuitem', name='리트윗 취소').click(timeout=1000)
                except:
                    pass
            else:
                await tweet.get_by_role('button', name='더 보기').click()
                await page.get_by_role('menuitem', name='삭제하기', exact=True).click()
                await page.get_by_role('button', name='삭제하기', exact=True).click()
            await page.wait_for_timeout(1000)

asyncio.run(main())
