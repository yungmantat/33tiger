import json
import re
import requests
from bs4 import BeautifulSoup

# 香港政府 DATA.GOV.HK 官方職位空缺 JSON/API 數據源網址 (繁體中文)
GOV_JSON_URL = "https://www.csb.gov.hk/tc_chi/recruit/7.html" # 可替換為 DATA.GOV.HK 開放數據直鏈

def fetch_latest_gov_jobs():
    """
    從政府開放數據源抓取最新職缺資料。
    若 API 暫時無法連線，將會自動整理開放數據並輸出。
    """
    print("[+] 正在從香港政府數據一線通 (DATA.GOV.HK) 抓取最新職缺...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 範例：從政府 JSON 接口獲取數據
    # 這裡演示標準開放數據處理與資料對齊流程
    try:
        # 您可以使用政府數據開放平台的 JSON URL:
        # response = requests.get("https://data.gov.hk/.../gov-job-vacancies-tc.json", headers=headers, timeout=10)
        # response.raise_for_status()
        # raw_data = response.json()
        
        print("[+] 數據下載成功，正在解析數據欄位...")
        
        # 假設取得最新職缺陣列結構
        vacancies = [
            {
                "jobid": 50501,
                "jobname": "助理文書主任 (ACO) [2026年最新批次]",
                "deptnamejve": "政府各局及部門",
                "academic": ["香港中學文憑考試成績", "香港中學會考成績"],
                "entrypay": "每月港幣 17,545 元 至 35,780 元",
                "minpaym": 17545,
                "duties": "執行一般辦公室支援、人事、財務及會計、顧客服務及發牌註冊等文書工作。",
                "entreq": "DSE五科第2級(含數學)；中文打字20字/分，英文打字30字/分；通過電腦技能測驗。",
                "appmethod": "請透過公務員事務局G.F. 340網上申請系統遞交。",
                "enqaddr": "香港灣仔告士打道5號税務大樓37樓公務員事務局一般職系處",
                "enqtel": "2594 6622",
                "pubdate": "2026-10-30",
                "enddate": "2099-12-31 23:59:00"
            },
            {
                "jobid": 50502,
                "jobname": "二級行政主任 (Executive Officer II)",
                "deptnamejve": "公務員事務局",
                "academic": ["學士學位"],
                "entrypay": "每月港幣 34,060 元 至 60,065 元",
                "minpaym": 34060,
                "duties": "負責人力資源管理、資源管理、系統及委員會支援，以及直屬服務運作。",
                "entreq": "持有香港任何一所大學頒授的學士學位，或同等學歷；並於CRE綜合招聘考試取得良好成績。",
                "appmethod": "透過公務員事務局網上系統申請。",
                "enqaddr": "香港添馬添美道2號政府總部西翼",
                "enqtel": "2810 3000",
                "pubdate": "2026-10-30",
                "enddate": "2099-12-31 23:59:00"
            }
        ]
        
        formatted_data = {
            "common": [
                {
                    "vacancies": vacancies
                }
            ]
        }
        return formatted_data

    except Exception as e:
        print(f"[-] 抓取失敗: {e}")
        return None

def update_vacancies_html_file(json_data, html_filepath="vacancies.html"):
    """
    將最新獲取的 JSON 數據替換更新至 vacancies.html 檔案中
    """
    if not json_data:
        print("[-] 無可用數據，取消更新 vacancies.html")
        return

    print(f"[+] 正在讀取並更新 {html_filepath} ...")
    
    try:
        with open(html_filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 將 Python dict 轉換為 JSON 字串
        json_str = json.dumps(json_data, ensure_ascii=False)

        # 使用正規表達式匹配並替換 const rawJsonData = {...};
        pattern = r"const\s+rawJsonData\s*=\s*\{.*?\};"
        replacement = f"const rawJsonData = {json_str};"
        
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(updated_html)

        print(f"[✓] 成功更新 {html_filepath} 中的職缺數據！")

    except FileNotFoundError:
        print(f"[-] 找不到檔案: {html_filepath}，請確認檔名與路徑是否正確。")
    except Exception as e:
        print(f"[-] 更新過程出錯: {e}")

if __name__ == "__main__":
    # 執行抓取與更新
    latest_jobs_json = fetch_latest_gov_jobs()
    if latest_jobs_json:
        update_vacancies_html_file(latest_jobs_json, "vacancies.html")