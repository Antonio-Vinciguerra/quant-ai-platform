import os
import requests

# ===== SETTINGS =====
pair = "EURUSD"
start_year = 2001
end_year = 2020  # they have around 2001–2020
output_folder = "eurusd_forextester"
# ====================

os.makedirs(output_folder, exist_ok=True)

for year in range(start_year, end_year + 1):
    file_name = f"{pair}_{year}.zip"
    url = f"https://www.forextester.com/data/{file_name}"
    file_path = os.path.join(output_folder, file_name)

    print(f"⏳ Downloading {file_name} ...")
    response = requests.get(url, stream=True)
    if response.status_code == 200 and int(response.headers.get('Content-Length', 0)) > 0:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Saved {file_name}")
    else:
        print(f"⚠️ No data for {year}")

print("✅ Finished downloading ForexTester data!")