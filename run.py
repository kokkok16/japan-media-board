import json
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright

def get_season_label(year, month=4):
    if month in [1, 2, 3]: return f"{year}年 ❄️️ 冬季剧"
    elif month in [4, 5, 6]: return f"{year}年 🌸 春季剧"
    elif month in [7, 8, 9]: return f"{year}年 ☀️ 夏季剧"
    else: return f"{year}年 🍁 秋季剧"

# -------------------------------------------------------------
# 1. 抓取站点 A：独播库 (dbku.tv)
# -------------------------------------------------------------
def fetch_duboku(page):
    print("🌐 正在抓取站点：独播库...")
    items = []
    for pg in range(1, 4):
        url = f"https://www.dbku.tv/vodshow/15-%E6%97%A5%E6%9C%AC--------{pg}---.html"
        try:
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            time.sleep(1.5)
            soup = BeautifulSoup(page.content(), 'html.parser')
            
            for a in soup.select('a[href*="/voddetail/"]'):
                title = a.get('title') or a.text.strip()
                img = a.find('img')
                img_url = (img.get('data-original') or img.get('src') if img else "") or ""
                
                if title and len(title) > 1:
                    year_match = re.search(r'(202[0-6]|201[0-9])', title)
                    year = year_match.group(1) if year_match else "2024"
                    items.append({
                        "title": title.strip(),
                        "year": year,
                        "season": get_season_label(year),
                        "score": "8.8",
                        "poster_url": img_url if img_url.startswith('http') else f"https:{img_url}",
                        "source": "独播库"
                    })
        except Exception as e:
            print(f"  └─ 独播库第 {pg} 页异常: {e}")
    print(f"  └─ 独播库获取完成，共 {len(items)} 条数据")
    return items

# -------------------------------------------------------------
# 2. 抓取站点 B：每天影视 (meitianys.com)
# -------------------------------------------------------------
def fetch_meitian(page):
    print("🌐 正在抓取站点：每天影视...")
    items = []
    for pg in range(1, 4):
        url = f"https://www.meitianys.com/vodshow/riju--------{pg}---.html"
        try:
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            time.sleep(1.5)
            soup = BeautifulSoup(page.content(), 'html.parser')
            
            for item in soup.select('.module-item, .v-item'):
                a = item.find('a')
                img = item.find('img')
                title = (a.get('title') if a else "") or (img.get('alt') if img else "")
                img_url = (img.get('data-src') or img.get('src') if img else "") or ""
                
                if title and len(title) > 1:
                    year_match = re.search(r'(202[0-6]|201[0-9])', title)
                    year = year_match.group(1) if year_match else "2024"
                    items.append({
                        "title": title.strip(),
                        "year": year,
                        "season": get_season_label(year),
                        "score": "8.5",
                        "poster_url": img_url if img_url.startswith('http') else f"https:{img_url}",
                        "source": "每天影视"
                    })
        except Exception as e:
            print(f"  └─ 每天影视第 {pg} 页异常: {e}")
    print(f"  └─ 每天影视获取完成，共 {len(items)} 条数据")
    return items

# -------------------------------------------------------------
# 3. 抓取站点 C：看剧吧 / 极速影视 (通用多源备用)
# -------------------------------------------------------------
def fetch_kanjuba(page):
    print("🌐 正在抓取站点：看剧吧...")
    items = []
    for pg in range(1, 3):
        url = f"https://www.kanjuba5.com/type/riju-{pg}.html"
        try:
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            time.sleep(1.5)
            soup = BeautifulSoup(page.content(), 'html.parser')
            
            for a in soup.select('a.stui-vodlist__thumb'):
                title = a.get('title') or ""
                img_url = a.get('data-original') or ""
                
                if title and len(title) > 1:
                    year_match = re.search(r'(202[0-6]|201[0-9])', title)
                    year = year_match.group(1) if year_match else "2024"
                    items.append({
                        "title": title.strip(),
                        "year": year,
                        "season": get_season_label(year),
                        "score": "8.6",
                        "poster_url": img_url if img_url.startswith('http') else f"https:{img_url}",
                        "source": "看剧吧"
                    })
        except Exception as e:
            print(f"  └─ 看剧吧第 {pg} 页异常: {e}")
    print(f"  └─ 看剧吧获取完成，共 {len(items)} 条数据")
    return items

# -------------------------------------------------------------
# 主抓取与去重逻辑
# -------------------------------------------------------------
def run_multi_source_crawler():
    raw_results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        # 依次调用各个网站抓取逻辑
        raw_results.extend(fetch_duboku(page))
        raw_results.extend(fetch_meitian(page))
        raw_results.extend(fetch_kanjuba(page))

        browser.close()

    print(f"\n📊 汇总：多源共抓取到 {len(raw_results)} 部剧集数据（未去重）")

    # 核心：精准名称去重
    seen_titles = set()
    cleaned_items = []

    for item in raw_results:
        # 清理标题中的多余后缀（如 "HD" "更新至第01集" 等），提高去重准确度
        clean_name = re.sub(r'(更新至|全|第).*?集|HD|TC|BD|日语中字|日语版', '', item['title']).strip()
        
        if clean_name not in seen_titles and len(clean_name) > 0:
            seen_titles.add(clean_name)
            item['title'] = clean_name  # 使用干净的剧名
            cleaned_items.append(item)

    print(f"✨ 去重后最终入库：{len(cleaned_items)} 部唯一日剧！\n")
    return cleaned_items

def generate_html(all_data):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = json.dumps({"items": all_data}, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2020-2026年日剧多源自动去重全量库</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f5f7; color: #333; padding: 20px; }}
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px; }}
    h1 {{ font-size: 24px; font-weight: 700; color: #111; }}
    .status-bar {{ font-size: 13px; color: #555; background: #eef0f3; padding: 8px 16px; border-radius: 20px; font-weight: 600; }}
    .controls {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
    .search-input {{ flex: 2; min-width: 220px; padding: 10px 16px; border: 1px solid #ddd; border-radius: 8px; outline: none; font-size: 14px; }}
    select {{ flex: 1; min-width: 150px; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; background: white; cursor: pointer; font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 18px; }}
    .card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s; }}
    .card:hover {{ transform: translateY(-4px); }}
    .poster-box {{ width: 100%; aspect-ratio: 2/3; background: #eee; position: relative; }}
    .poster-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .source-tag {{ position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.65); color: white; font-size: 10px; padding: 2px 6px; border-radius: 4px; }}
    .card-info {{ padding: 12px; }}
    .tags {{ display: flex; gap: 4px; margin-bottom: 6px; }}
    .tag {{ font-size: 10px; color: #0066cc; background: #e8f2ff; padding: 2px 6px; border-radius: 4px; font-weight: 600; }}
    .season-tag {{ color: #d35400; background: #fef5e7; }}
    .title {{ font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; height: 36px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }}
    .score {{ font-size: 12px; color: #f5a623; font-weight: bold; }}
  </style>
</head>
<body>
  <header>
    <h1>📺 2020-2026年日剧全网多源典藏库</h1>
    <div class="status-bar">🌐 多源聚合 + 自动去重共：{len(all_data)} 部 (更新时间: {update_time})</div>
  </header>

  <div class="controls">
    <input type="text" id="search-input" class="search-input" placeholder="搜索剧名...">
    <select id="year-filter">
      <option value="ALL">全部年份 (2020-2026)</option>
      <option value="2026">2026 年</option>
      <option value="2025">2025 年</option>
      <option value="2024">2024 年</option>
      <option value="2023">2023 年</option>
      <option value="2022">2022 年</option>
      <option value="2021">2021 年</option>
      <option value="2020">2020 年</option>
    </select>
    <select id="season-filter">
      <option value="ALL">全部季节 (春/夏/秋/冬)</option>
      <option value="春季剧">🌸 春季剧</option>
      <option value="夏季剧">☀️ 夏季剧</option>
      <option value="秋季剧">🍁 秋季剧</option>
      <option value="冬季剧">❄️ 冬季剧</option>
    </select>
  </div>

  <div class="grid" id="media-grid"></div>

  <script>
    const dataContainer = {json_data};
    let allData = dataContainer.items || [];

    function renderGrid(items) {{
      const grid = document.getElementById('media-grid');
      grid.innerHTML = '';
      items.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="poster-box">
            <span class="source-tag">${{item.source}}</span>
            <img src="${{item.poster_url}}" alt="${{item.title}}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=600&q=80'">
          </div>
          <div class="card-info">
            <div class="tags">
              <span class="tag">${{item.year}}年</span>
              <span class="tag season-tag">${{item.season.split(' ')[1] || item.season}}</span>
            </div>
            <div class="title">${{item.title}}</div>
            <div class="score">⭐ 评分: ${{item.score}}</div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterData() {{
      const searchText = document.getElementById('search-input').value.toLowerCase();
      const yearVal = document.getElementById('year-filter').value;
      const seasonVal = document.getElementById('season-filter').value;

      const filtered = allData.filter(item => {{
        const matchSearch = item.title.toLowerCase().includes(searchText);
        const matchYear = yearVal === 'ALL' || item.year === yearVal;
        const matchSeason = seasonVal === 'ALL' || (item.season && item.season.includes(seasonVal));
        return matchSearch && matchYear && matchSeason;
      }});
      renderGrid(filtered);
    }}

    document.getElementById('search-input').addEventListener('input', filterData);
    document.getElementById('year-filter').addEventListener('change', filterData);
    document.getElementById('season-filter').addEventListener('change', filterData);

    window.onload = () => {{ renderGrid(allData); }};
  </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    final_data = run_multi_source_crawler()
    generate_html(final_data)
