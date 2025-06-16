import subprocess
import json
from datetime import datetime

def run_speedtest():
    result = subprocess.run(["speedtest", "--accept-license", "-f", "json"], capture_output=True)
    data = json.loads(result.stdout)

    return {
        "isp": data["isp"],
        "server": data["server"]["name"],
        "country_code": data["server"].get("country", "")[:2],
        "country": data["server"].get("country", "Unknown"),
        "ping": round(data["ping"]["latency"], 2),
        "download": round(data["download"]["bandwidth"] * 8 / 1e6, 2),  # Mbps換算
        "upload": round(data["upload"]["bandwidth"] * 8 / 1e6, 2),
        "timestamp": datetime.now().strftime("%Y年%m月%d日 %H:%M")
    }

def get_ping_status(ping):
    if ping < 30:
        return "🟢 (Low)"
    elif ping < 100:
        return "🟡 (Medium)"
    else:
        return "🔴 (High)"

def get_flag(country_code):
    try:
        if not country_code or len(country_code) != 2:
            return "🌐"  # 不明または無効なコードの場合は地球儀
        return chr(127397 + ord(country_code[0].upper())) + chr(127397 + ord(country_code[1].upper()))
    except Exception:
        return "🌐"
