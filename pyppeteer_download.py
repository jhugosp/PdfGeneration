from pyppeteer import launch
import os


async def save_page_as_pdf(url, n, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    browser = await launch(headless=True)
    page = await browser.newPage()

    for i in range(n):
        await page.goto(url, {'waitUntil': 'networkidle2'})  # Wait until the network is idle
        await page.evaluate('''() => {
            const images = Array.from(document.images);
            return Promise.all(images.map(img => {
                if (img.complete) {
                    return Promise.resolve();
                }
                return new Promise((resolve, reject) => {
                    img.onload = resolve;
                    img.onerror = reject;
                });
            }));
        }''')
        pdf_path = os.path.join(output_dir, f"extracts_{i+1}.pdf")
        await page.pdf({'path': pdf_path, 'format': 'A4', 'printBackground': True})
        print("Saved PDF {}".format(i))
        await page.reload()

    await browser.close()
