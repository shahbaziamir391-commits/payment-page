import urllib.request
import urllib.error
import json
import os
import ssl
import sys

RIALIT_API_KEY = os.environ.get('RIALIT_API_KEY')
GIST_TOKEN = os.environ.get('GIST_TOKEN')
GIST_ID = os.environ.get('GIST_ID')
CALLBACK_URL = os.environ.get('CALLBACK_URL')
AMOUNT = int(os.environ.get('AMOUNT', 100000))

def create_new_link():
    url = "https://api.rialit.org/api/v1/send"
    data = json.dumps({"amount": AMOUNT, "callback_url": CALLBACK_URL, "description": "پرداخت"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {RIALIT_API_KEY}", "Content-Type": "application/json"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            result = json.loads(response.read().decode('utf-8'))
            token = result.get('token')
            if token:
                return f"https://api.rialit.org/api/v1/redirect/{token}"
            else:
                print("⚠️ توکن پیدا نشد:", result)
                return None
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        sys.stdout.flush()
        return None
    except Exception as e:
        print(f"❌ خطا: {e}")
        sys.stdout.flush()
        return None

def update_gist(link):
    url = f"https://api.github.com/gists/{GIST_ID}"
    data = json.dumps({"files": {"link.txt": {"content": link}}}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH', headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            return True
    except Exception as e:
        print(f"❌ خطا در به‌روزرسانی Gist: {e}")
        sys.stdout.flush()
        return False

def main():
    print("⏳ در حال ساخت لینک جدید...")
    sys.stdout.flush()
    new_link = create_new_link()
    if new_link:
        print("✅ لینک ساخته شد:", new_link)
        sys.stdout.flush()
        if update_gist(new_link):
            print("✅ لینک در Gist ذخیره شد")
        else:
            print("❌ لینک در Gist ذخیره نشد")
    else:
        print("❌ لینک ساخته نشد")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
