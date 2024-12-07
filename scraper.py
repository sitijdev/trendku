from xml.etree import ElementTree
import json
import requests

COUNTRY_LIST = [
    {"country": "UNITED_STATES", "code": "US", "p": "p1"},
    {"country": "ARGENTINA", "code": "AR", "p": "p30"},
    {"country": "AUSTRALIA", "code": "AU", "p": "p8"},
    {"country": "AUSTRIA", "code": "AT", "p": "p44"},
    {"country": "BELGIUM", "code": "BE", "p": "p41"},
    {"country": "BRAZIL", "code": "BR", "p": "p18"},
    {"country": "CANADA", "code": "CA", "p": "p13"},
    {"country": "CHILE", "code": "CL", "p": "p38"},
    {"country": "COLOMBIA", "code": "CO", "p": "p32"},
    {"country": "CZECHIA", "code": "CZ", "p": "p43"},
    {"country": "DENMARK", "code": "DK", "p": "p49"},
    {"country": "EGYPT", "code": "EG", "p": "p29"},
    {"country": "FINLAND", "code": "FI", "p": "p50"},
    {"country": "FRANCE", "code": "FR", "p": "p16"},
    {"country": "GERMANY", "code": "DE", "p": "p15"},
    {"country": "GREECE", "code": "GR", "p": "p48"},
    {"country": "HONG_KONG", "code": "HK", "p": "p10"},
    {"country": "HUNGARY", "code": "HU", "p": "p45"},
    {"country": "INDIA", "code": "IN", "p": "p3"},
    {"country": "INDONESIA", "code": "ID", "p": "p19"},
    {"country": "IRELAND", "code": "IE", "p": "p54"},
    {"country": "ISRAEL", "code": "IL", "p": "p6"},
    {"country": "ITALY", "code": "IT", "p": "p27"},
    {"country": "JAPAN", "code": "JP", "p": "p4"},
    {"country": "KENYA", "code": "KE", "p": "p37"},
    {"country": "MALAYSIA", "code": "MY", "p": "p34"},
    {"country": "MEXICO", "code": "MX", "p": "p21"},
    {"country": "NETHERLANDS", "code": "NL", "p": "p17"},
    {"country": "NEW_ZEALAND", "code": "NZ", "p": "p53"},
    {"country": "NIGERIA", "code": "NG", "p": "p52"},
    {"country": "NORWAY", "code": "NO", "p": "p51"},
    {"country": "PHILIPPINES", "code": "PH", "p": "p25"},
    {"country": "POLAND", "code": "PL", "p": "p31"},
    {"country": "PORTUGAL", "code": "PT", "p": "p47"},
    {"country": "ROMANIA", "code": "RO", "p": "p39"},
    {"country": "RUSSIA", "code": "RU", "p": "p14"},
    {"country": "SAUDI_ARABIA", "code": "SA", "p": "p36"},
    {"country": "SINGAPORE", "code": "SG", "p": "p5"},
    {"country": "SOUTH_AFRICA", "code": "ZA", "p": "p40"},
    {"country": "SOUTH_KOREA", "code": "KR", "p": "p23"},
    {"country": "SWEDEN", "code": "SE", "p": "p42"},
    {"country": "SWITZERLAND", "code": "CH", "p": "p46"},
    {"country": "TAIWAN", "code": "TW", "p": "p12"},
    {"country": "THAILAND", "code": "TH", "p": "p33"},
    {"country": "TURKEY", "code": "TR", "p": "p24"},
    {"country": "UKRAINE", "code": "UA", "p": "p35"},
    {"country": "UNITED_KINGDOM", "code": "GB", "p": "p9"},
    {"country": "VIETNAM", "code": "VN", "p": "p28"}
]

def scrape_data(code):
    try:
        url = f"https://trends.google.com/trends/hottrends/atom/feed?pn={code}"
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
        }

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        trends = []
        xml_data = resp.text
        root = ElementTree.fromstring(xml_data)
        for item in root.findall(".//item"):
            try:
                title = item.find("title").text
                approx_traffic = item.find("{https://trends.google.com/trends/trendingsearches/daily}approx_traffic").text
                pubDate = item.find("pubDate").text

                trends.append({
                    "title": title,
                    "approx_traffic": approx_traffic,
                    "pubDate": pubDate,
                })
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
        return trends

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {"error": "Failed to fetch data."}
    except Exception as e:
        print(f"Error scraping data: {e}")
        return {"error": "Failed to scrape data."}

def main():
    for country in COUNTRY_LIST:
        trends_data = scrape_data(country["p"])

        if "error" in trends_data:
            print(f"Error scraping data for {country['country']}: {trends_data['error']}")
            continue

        json_filename = f"data/{country['country'].replace(' ', '_')}.json"  # Pastikan file disimpan di folder data
        with open(json_filename, 'w') as json_file:
            json.dump(trends_data, json_file, indent=4)

        print(f"Google Trends data for {country['country']} saved to {json_filename}")

if __name__ == "__main__":
    main()
