import requests
import json
import os
import time
import re
from datetime import datetime
from urllib.parse import quote

THEATRICAL_KEYWORDS = ["劇場版", "剧场版", "电影版", "映画版", "Special", "SP", "篇"]

def classify_movie(title):
    for kw in THEATRICAL_KEYWORDS:
        if kw in title:
            return "日剧剧场版"
    return "日本电影"

def get_detail_summary(db_id):
    url = f"https://movie.douban.com/subject/{db_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://movie.douban.com/subject/{db_id}/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            match = re.search(r'<span property="v:summary"[^>]*>(.*?)</span>', res.text, re.DOTALL)
            if match:
                summary = match.group(1).replace('<br/>', '\n').replace('<br>', '\n').strip()
                summary = re.sub(r'<[^>]+>', '', summary)
                return summary.strip()
            
            # 折叠文本备用逻辑
            match_all = re.search(r'<span class="all hidden">(.*?)</span>', res.text, re.DOTALL)
            if match_all:
                summary = match_all.group(1).replace('<br/>', '\n').replace('<br>', '\n').strip()
                return re.sub(r'<[^>]+>', '', summary).strip()
    except Exception as e:
        print(f"获取 {db_id} 详情失败: {e}")
    return "暂无详细故事简介。"

def fetch_douban_subjects(tag_name, is_movie=False, max_pages=5):
    encoded_tag = quote(tag_name)
    media_type = "movie" if is_movie else "tv"
    items = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://movie.douban.com/"
    }
    
    page_limit = 20
    for page in range(max_pages):
        page_start = page * page_limit
        url = f"https://movie.douban.com/j/search_subjects?type={media_type}&tag={encoded_tag}&sort=time&page_limit={page_limit}&page_start={page_start}"
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json().get("subjects", [])
                if not data:
                    break
                    
                for sub in data:
                    title = sub.get("title", "")
                    db_id = sub.get("id")
                    
                    cover = sub.get("cover", "")
                    if "s_ratio_poster" in cover:
                        cover = cover.replace("s_ratio_poster", "l_ratio_poster")
                        
                    items.append({
                        "id": f"{media_type}_{db_id}",
                        "db_id": db_id,
                        "title": title,
                        "poster_url": cover,
                        "score": sub.get('rate', '暂无'),
                        "douban_url": f"https://movie.douban.com/subject/{db_id}/"
                    })
                time.sleep(0.3)
            else:
                break
        except Exception:
            break
            
    return items

def main():
    print("==========================================")
    print("🚀 正在抓取数据与完整剧情简介（请稍候 1-2 分钟）...")
    print("==========================================")
    
    output_file = os.path.expanduser("~/Downloads/japan_media_data.json")
    all_data = []
    seen_ids = set()

    # 1. 抓取日剧
    tv_raw = fetch_douban_subjects("日剧", is_movie=False, max_pages=6)
    quarter_names = ["冬季档 (1月)", "春季档 (4月)", "夏季档 (7月)", "秋季档 (10月)"]
    current_year = datetime.now().year
    
    for idx, item in enumerate(tv_raw):
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            q_idx = idx % 4
            item["category"] = "日剧"
            item["release_year"] = f"{current_year}年"
            item["quarter_group"] = f"{current_year}年{quarter_names[q_idx]}"
            
            print(f"[{idx+1}/{len(tv_raw)}] 获取简介: {item['title']}")
            item["summary"] = get_detail_summary(item["db_id"])
            time.sleep(0.8) # 减慢请求频率，防止被豆瓣屏蔽
                
            all_data.append(item)

    # 2. 抓取电影/剧场版
    movies_raw = fetch_douban_subjects("日本", is_movie=True, max_pages=4)
    for idx, item in enumerate(movies_raw):
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            item["category"] = classify_movie(item["title"])
            item["release_year"] = "最新上映"
            item["quarter_group"] = "最新电影/剧场版"
            
            print(f"电影 [{idx+1}/{len(movies_raw)}] 获取简介: {item['title']}")
            item["summary"] = get_detail_summary(item["db_id"])
            time.sleep(0.8)
                
            all_data.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(all_data),
            "items": all_data
        }, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 成功更新 {len(all_data)} 条数据！已写入 ~/Downloads/japan_media_data.json")

if __name__ == "__main__":
    main()
