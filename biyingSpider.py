import requests
import re
import time

# 1. Standard headers to look like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

local = time.strftime("%Y.%m.%d")
url = 'https://cn.bing.com/' # Use https

try:
    con = requests.get(url, headers=headers)
    content = con.text

    # 2. Updated Regex to find the image path in the modern Bing layout
    reg = r"(/th\?id=OHR\..*?\.jpg)"
    
    matches = re.findall(reg, content)

    if matches:
        a = matches[0]
        # Remove backslashes if Bing escaped the URL (common in JSON/JS)
        a = a.replace('\\', '')
        
        # 3. Clean up the URL (Bing often adds '1920x1080' tags)
        picUrl = url + a if a.startswith('/') else a
        
        print(f"Downloading: {picUrl}")
        
        read = requests.get(picUrl, headers=headers)
        with open(f'{local}.jpg', 'wb') as f:
            f.write(read.content)
        print("Success!")
    else:
        print("Could not find the image URL. The page layout might have changed.")

except Exception as e:
    print(f"An error occurred: {e}")