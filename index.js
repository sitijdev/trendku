const puppeteer = require('puppeteer');

async function getGoogleTrendsData(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    // 1. Buka halaman Google Trends (gunakan URL dari argument)
    await page.goto(url);

    // 2. Tunggu sampai tombol dengan selector muncul
    await page.waitForSelector('.FOBRw-vQzf8d');

    // 3. Klik tombol 
    await page.click('.FOBRw-vQzf8d');

    // 4. Tunggu sampai dropdown list item kedua muncul
    await page.waitForSelector('.FOBRw-vQzf8d + .JPKJSGGbxEQ ul li:nth-child(2)'); 

    // 5. Klik list item kedua (opsi copy)
    await page.click('.FOBRw-vQzf8d + .JPKJSGGbxEQ ul li:nth-child(2)');

    // 6. Ambil data dari clipboard
    const data = await page.evaluate(() => navigator.clipboard.readText());

    // 7. Ekstrak kode negara dari URL
    const kodenegara = url.split('geo=')[1]; 

    // 8. Simpan data ke file
    const fs = require('fs');
    fs.writeFileSync(`${kodenegara}.txt`, data);
    console.log(`Data tersimpan di ${kodenegara}.txt`);

  } catch (error) {
    console.error('Error:', error);
  } finally {
    // 9. Tutup browser
    await browser.close();
  }
}

// Ambil URL dari argument
const url = process.argv[2];

getGoogleTrendsData(url);
