import re
import requests
import base64
import os
import json
import asyncio
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Optional: ping3 might not be available in all environments, handle it
try:
    from ping3 import ping
except ImportError:
    def ping(target, timeout=2):
        return None

CONFIG_FILE = "config_rshoka.json"

# AES Key and IV from enc.py
KEY_HEX = "000102030405060708090a0b0c0d0e0f"
IV_HEX  = "101112131415161718191a1b1c1d1e1f"

# Color codes
g = "\033[1;32m" # Green
y = "\033[1;33m" # Yellow
r = "\033[1;31m" # Red
w = "\033[0m"    # Reset
c = "\033[1;36m" # Cyan
m = "\033[1;35m" # Magenta
b = "\033[1;34m" # Blue

# Global variables for auto loop
auto_loop_running = False
loop_interval = 60  # 1 minute in seconds

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    # ASCII Art for "TTAK" - Improved version matching the spirit of the screenshot
    print(c + "="*56)
    print(c + "  ████████╗████████╗ █████╗ ██╗  ██╗")
    print(c + "  ╚══██╔══╝╚══██╔══╝██╔══██╗██║ ██╔╝")
    print(c + "     ██║      ██║   ███████║█████╔╝ ")
    print(c + "     ██║      ██║   ██╔══██║██╔═██╗ ")
    print(c + "     ██║      ██║   ██║  ██║██║  ██╗")
    print(c + "     ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝")
    print(c + "="*56 + w)
    print(g + "          TTAK - WiFi Bypass Tool TTAK" + w)
    print(g + "             STAR LINK BYPASS TOOL" + w)
    print(y + "      STAR LINK ဝယ်ယူရန် ADMIN ACCOUNT @TTAK19" + w)
    print(b + "      Telegram Channel: https://t.me/TTAKVPN" + w)
    print(c + "="*56 + w)

def decrypt_url(encrypted_text):
    try:
        key = bytes.fromhex(KEY_HEX)
        iv  = bytes.fromhex(IV_HEX)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted_text = unpad(decrypted_padded, AES.block_size).decode("utf-8")
        return decrypted_text
    except Exception as e:
        return None

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(session_url, mac_address, voucher, gateway_ip):
    config = {
        "session_url": session_url,
        "mac_address": mac_address,
        "voucher": voucher,
        "gateway_ip": gateway_ip
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def replace_mac(url, new_mac):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)       
    return url

def get_session_id(session_url, mac_address):
    # Check if URL is encrypted (likely doesn't start with http)
    if not session_url.startswith("http"):
        decrypted = decrypt_url(session_url)
        if decrypted:
            session_url = decrypted
        else:
            print(f"{r}[-] Invalid URL or Decryption Failed!{w}")
            return None

    final_url = replace_mac(session_url, mac_address)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': final_url,
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    
    try:
        response = requests.get(final_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except Exception as e:
        print(f"{r}[-] Error Getting Session ID: {e}{w}")
        return None

def login_voucher(session_id, voucher):
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 1
    }
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": 'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            res_text = response.text
            
            if 'error' in res_text.lower() or 'invalid' in res_text.lower():
                return None, res_text
            
            token_match = re.search('token=(.*?)&', res_text)
            if token_match:
                return token_match.group(1), None
            else:
                return None, res_text
                
    except Exception as Error:
        print(f"{r}[-] Voucher Login Error: {Error}{w}")
        return None, str(Error)

async def get_smart_ping():
    """Ping စစ်ပြီး latency ကို အရောင်နဲ့ပြပေးမယ်"""
    targets = ["google.com", "8.8.8.8", "cloudflare.com"]
    
    print("\n" + c + "="*56 + w)
    print("  📶 Checking Internet Connection...")
    print(c + "="*56 + w)
    
    connected = False
    best_result = None
    
    for target in targets:
        try:
            ping_result = await asyncio.to_thread(ping, target, timeout=2)
            
            if ping_result is not None:
                ping_ms = int(ping_result * 1000)
                connected = True
                
                if ping_ms >= 150:
                    color = r
                    status = "🔴 Poor"
                elif ping_ms >= 80:
                    color = y
                    status = "🟡 Fair"
                else:
                    color = g
                    status = "🟢 Excellent"
                
                print(f"  {color}✓{w} {target:15} → {color}{ping_ms:>4} ms{w}  {status}")
                
                if best_result is None or ping_ms < int(re.search(r'\d+', best_result).group() if best_result else '999'):
                    best_result = f"{color}{ping_ms} ms ({target}){w}"
            else:
                print(f"  {r}✗{w} {target:15} → {r}Timeout{w}")
                
        except Exception as e:
            print(f"  {r}✗{w} {target:15} → {r}Error{w}")
            continue
    
    print(c + "="*56 + w)
    
    if connected:
        print(f"\n  {g}✅ Internet Connected!{w}")
        return best_result if best_result else f"{g}Connected{w}"
    else:
        print(f"\n  {r}❌ No Internet Connection (Offline){w}")
        return f"{r}Offline{w}"

def do_bypass(session_url, mac_address, voucher, gateway_ip):
    """Bypass လုပ်ငန်းစဉ်"""
    session_id = get_session_id(session_url, mac_address)
    
    if not session_id:
        return False
        
    print(f"[+] Inactive Session Id: {session_id}")
    
    active_session_id, error_msg = login_voucher(session_id, voucher)
    
    if not active_session_id:
        print(f"{r}[✗] Voucher code သက်တမ်းကုန်ဆုံးနေပါသည်{w}")
        return False
    
    print(f"[+] Active Session Id: {active_session_id}")

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': active_session_id,
        'phoneNumber': 'RshoKaUser',
    }
    
    try:
        final_req_url = f'http://{gateway_ip}:2060/wifidog/auth?'
        response_url = requests.get(final_req_url, params=params, headers=headers).url
        
        success_conditions = [
            "http://www.baidu.com", 
            "http://www.baidu.com/", 
            "http://portal-as.ruijienetworks.com/download/static/maccauth/src/success.html?",
            "success"
        ]
        
        if any(cond in response_url for cond in success_conditions):
            print(f"\n{g}[✓] Internet Bypass Successful! Enjoy your internet.{w}")
            return True
        else:
            print(f"\n{r}[-] Internet Bypass Failed or Unknown Response Route.{w}")
            return False
    except Exception as e:
        print(f"\n{r}[-] Auth Gateway connection error: {e}{w}")
        return False

async def auto_loop_bypass(session_url, mac_address, voucher, gateway_ip):
    """Auto loop bypass function"""
    global auto_loop_running
    auto_loop_running = True
    loop_count = 0
    
    print("\n" + c + "="*56 + w)
    print("  🔄 Auto Bypass Loop Started")
    print(f"  ⏱️  Interval: {loop_interval} seconds (1 minute)")
    print("  ⏹️  Press Ctrl+C to stop")
    print(c + "="*56 + w)
    
    while auto_loop_running:
        loop_count += 1
        print(f"\n{c}{'='*56}{w}")
        print(f"  🔄 Loop #{loop_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{c}{'='*56}{w}")
        
        # Run bypass
        success = do_bypass(session_url, mac_address, voucher, gateway_ip)
        
        if success:
            # Ping check
            result = await get_smart_ping()
            print(f"\n  📊 Ping Result: {result}")
        else:
            print(f"\n  {y}⚠️ Bypass failed, retrying in 1 minute...{w}")
        
        # Wait for 1 minute
        print(f"\n  ⏳ Waiting 60 seconds before next loop...")
        for i in range(loop_interval, 0, -5):
            if not auto_loop_running:
                break
            if i % 10 == 0:
                print(f"  ⏱️  {i} seconds remaining...")
            await asyncio.sleep(5)
    
    print(f"\n  {r}🛑 Auto loop stopped.{w}")

def start_bypass():
    clear_screen()
    banner()
    
    config = load_config()
    
    old_url = config.get("session_url", "")
    old_mac = config.get("mac_address", "")
    old_voucher = config.get("voucher", "")
    old_ip = config.get("gateway_ip", "")
    
    print(y + "[+] WiFi အချက်အလက်များထည့်သွင်းပါ (ထည့်သွင်းပြီးသားဖြစ်ပါက Enter နှိပ်ပါ)" + w + "\n")
    
    if old_url:
        print(f"{b}[ သိမ်းဆည်းထား​သော TOKEN KEY ]: {old_url[:50]}...{w}")
    session_url = input(g + "=> TOKEN KEY ထည့်ရန်: " + w).strip() or old_url
    
    if not session_url:
        print(f"{r}[-] TOKEN KEY ထည့်သွင်းပါ!{w}")
        input("\nPress Enter to exit...")
        return

    if old_mac:
        print(f"{b}[ သိမ်းဆည်းထားသော MAC ]: {old_mac}{w}")
    mac_address = input(g + "=> MAC Address ထည့်ပါ (နမူနာ=10:3f:44:9d:b8:e4): " + w).strip() or old_mac

    if old_voucher:
        print(f"{b}[ သိမ်းဆည်းထားသော Voucher ]: {old_voucher}{w}")
    voucher = input(g + "=> Voucher Code ထည့်ပါ: " + w).strip() or old_voucher

    if old_ip:
        print(f"{b}[ သိမ်းဆည်းထားသော Gateway ]: {old_ip}{w}")
    gateway_ip = input(g + "=> Gateway IP ထည့်ပါ (နမူနာ= 192.168.60.1): " + w).strip() or old_ip

    save_config(session_url, mac_address, voucher, gateway_ip)
    
    print(f"\n{y}[*] Internet Bypass စတင်နေပါပြီ (Bypass Fail ပြပြီး Ping ပေါ်ရင်လဲ သုံးလို့ရပါတယ်){w}")
    
    # First bypass
    success = do_bypass(session_url, mac_address, voucher, gateway_ip)
    
    # Ping check
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_smart_ping())
        loop.close()
        print(f"\n  📊 Ping Result: {result}")
    except Exception as e:
        print(f"\n{r}[-] Ping Error: {e}{w}")
    
    # ===== Auto Loop =====
    print("\n" + c + "="*56 + w)
    print("  🔄 Starting Auto Bypass Loop automatically...")
    print(c + "="*56 + w)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(auto_loop_bypass(session_url, mac_address, voucher, gateway_ip))
    except KeyboardInterrupt:
        global auto_loop_running
        auto_loop_running = False
        print(f"\n  {r}🛑 User stopped the auto loop.{w}")
    except Exception as e:
        print(f"\n{r}[-] Auto Loop Error: {e}{w}")

if __name__ == "__main__":
    try:
        start_bypass()
    except KeyboardInterrupt:
        print(f"\n\n  {r}👋 Exiting...{w}")
    except Exception as e:
        print(f"\n{r}[!] Fatal Error: {e}{w}")
