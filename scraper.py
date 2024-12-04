from playwright.sync_api import sync_playwright

def get_google_trends_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # 1. Buka halaman Google Trends
            page.goto(url)

            # 2. Tunggu sampai tombol dengan selector muncul
            page.wait_for_selector('.FOBRw-vQzf8d')

            # 3. Klik tombol
            page.click('.FOBRw-vQzf8d')

            # 4. Tunggu sampai dropdown list item kedua muncul
            page.wait_for_selector('.FOBRw-vQzf8d + .JPKJSGGbxEQ ul li:nth-child(2)')

            # 5. Klik list item kedua (opsi copy)
            page.click('.FOBRw-vQzf8d + .JPKJSGGbxEQ ul li:nth-child(2)')

            # 6. Ambil data dari clipboard
            data = page.evaluate("navigator.clipboard.readText()")

            # 7. Ekstrak kode negara dari URL
            kodenegara = url.split('geo=')[1]

            # 8. Simpan data ke file
            with open(f"{kodenegara}.txt", "w") as f:
                f.write(data)
            print(f"Data tersimpan di {kodenegara}.txt")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # 9. Tutup browser
            browser.close()

if __name__ == "__main__":
    import sys
    url = sys.argv[1]  # Ambil URL dari argument
    get_google_trends_data(url)
