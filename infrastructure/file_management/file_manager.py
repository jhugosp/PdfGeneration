from pyppeteer import launch
import asyncio
import os


def download_pdfs() -> None:
    """ Asynchronous method in charge of calling a local server in order to automatically browser-print PDF files
        based on input given from client, triggered from a flask endpoint.

        This input will point the amount of files to be downloaded.

        When storing said files, they fall under a common name scheme, and as of now, override previously stored files.

        x: Non overridden files
        y: Amount of files to download from server.
        z: Previously stored files

        x = | y - z |

    :return: Nothing
    """
    url = "http://localhost:5000/"
    output_dir = "application/data_generation/synthetic_pdfs"
    iterations = int(input("How many files will you download? "))

    asyncio.run(save_page_as_pdf(url, iterations, output_dir))
    asyncio.get_event_loop().run_until_complete(save_page_as_pdf(url, iterations, output_dir))


async def save_page_as_pdf(url, n, output_dir) -> None:
    """ Browser printing script which also checks image loading before printing.

    :param url:             Local server to be consumed in order to obtain PDF file.
    :param n:               Iterations pointed by user, which translated to PDFs to be downloaded.
    :param output_dir:      Output directory in which PDF files will be stored.
    :return:                Nothing
    """
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
        print("Saved PDF {}".format(i + 1))
        await page.reload()

    await browser.close()
