import requests
import json
import re
import os
from datetime import datetime

def fetch_latest_media():
    print("🚀 开始抓取全网最新日剧与日本电影资讯...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://movie.douban.com/"
    }
    
    # 抓取豆瓣最新热门日剧 & 日本电影
    urls = [
        "https://movie.douban.com/j/search_subjects?type=tv&tag=%text%E6%97%A5%E5%89%A7&page_limit=20&page_start=0", # 日剧
        "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%97%A5%E6%9C%AC&page_limit=20&page_start=0" # 日影
    ]
    
    items = []
    
    # 抓取日剧
    try:
        res = requests.get("https://movie.douban.com/j/search_subjects?type=tv&tag=%E6%97%A5%E5%89%A7&sort=time&page_limit=15&page_start=0", headers=headers, timeout=10)
        data = res.json().get("subjects", [])
        for item in data:
            items.append({
                "id": f"tv_{item['id']}",
                "db_id": item['id'],
                "title": item['title'],
                "poster_url": item['cover'],
                "score": str(item['rate']),
                "douban_url": item['url'],
                "category": "日剧",
                "release_year": "2026年",
                "quarter_group": "最新热播日剧",
                "summary": f"《{item['title']}》正在热播中，豆瓣实时评分 {item['rate']} 分。点击关注最新剧集动态。"
            })
    except Exception as e:
        print(f"抓取日剧失败: {e}")

    # 抓取日本电影
    try:
        res = requests.get("https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%97%A5%E6%9C%AC&sort=time&page_limit=15&page_start=0", headers=headers, timeout=10)
        data = res.json().get("subjects", [])
        for item in data:
            items.append({
                "id": f"movie_{item['id']}",
                "db_id": item['id'],
                "title": item['title'],
                "poster_url": item['cover'],
                "score": str(item['rate']),
                "douban_url": item['url'],
                "category": "日本电影",
                "release_year": "最新上映",
                "quarter_group": "最新日本电影",
                "summary": f"《{item['title']}》最新上映日本电影，豆瓣实时评分 {item['rate']} 分。"
            })
    except Exception as e:
        print(f"抓取日影失败: {e}")

    return items

def generate_html(all_data):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = json.dumps({
        "updated_at": update_time,
        "total_count": len(all_data),
        "items": all_data
    }, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>日剧 & 电影看板</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f5f7; color: #333; padding: 20px; }}
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
    h1 {{ font-size: 24px; font-weight: 700; }}
    .status-bar {{ font-size: 13px; color: #666; background: #eef0f3; padding: 6px 12px; border-radius: 12px; }}
    .controls {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
    .search-input {{ flex: 1; min-width: 200px; padding: 8px 16px; border: 1px solid #ddd; border-radius: 8px; outline: none; }}
    select {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; background: white; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; }}
    .card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); cursor: pointer; transition: transform 0.2s; }}
    .card:hover {{ transform: translateY(-4px); }}
    .poster-box {{ width: 100%; aspect-ratio: 2/3; background: #e0e0e0; position: relative; overflow: hidden; }}
    .poster-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .card-info {{ padding: 12px; }}
    .tag {{ font-size: 11px; color: #0066cc; background: #e8f2ff; padding: 2px 8px; border-radius: 10px; font-weight: 600; }}
    .title {{ font-size: 14px; font-weight: 700; margin: 6px 0; line-height: 1.3; height: 36px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }}
    .score {{ font-size: 12px; color: #f5a623; font-weight: bold; }}
    .modal-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000; }}
    .modal-overlay.active {{ display: flex; }}
    .modal-content {{ background: white; width: 90%; max-width: 600px; border-radius: 16px; padding: 24px; position: relative; display: flex; gap: 20px; }}
    .modal-close {{ position: absolute; top: 16px; right: 16px; background: #eee; border: none; width: 32px; height: 32px; border-radius: 50%; font-size: 18px; cursor: pointer; }}
    .modal-poster {{ width: 140px; aspect-ratio: 2/3; border-radius: 8px; object-fit: cover; background: #e0e0e0; }}
    .modal-details {{ flex: 1; }}
    .modal-title {{ font-size: 20px; font-weight: bold; margin: 8px 0; }}
    .modal-score {{ color: #f5a623; font-weight: bold; margin-bottom: 12px; }}
    .modal-summary-text {{ background: #f8f9fa; padding: 12px; border-radius: 8px; font-size: 13px; color: #555; line-height: 1.6; max-height: 200px; overflow-y: auto; white-space: pre-line; }}
  </style>
</head>
<body>
  <header>
    <h1>📺 日剧 & 电影看板</h1>
    <div class="status-bar" id="update-time">🔄 自动更新时间: {update_time} (共 {len(all_data)} 部)</div>
  </header>

  <div class="controls">
    <input type="text" id="search-input" class="search-input" placeholder="搜索片名...">
    <select id="category-filter"><option value="ALL">全部分类</option><option value="日剧">日剧</option><option value="日本电影">日本电影</option></select>
  </div>

  <div class="grid" id="media-grid"></div>

  <div class="modal-overlay" id="modal-overlay">
    <div class="modal-content">
      <button class="modal-close" id="modal-close">✕</button>
      <img src="" class="modal-poster" id="modal-poster" onerror="handleImgError(this)">
      <div class="modal-details">
        <span class="tag" id="modal-tag">--</span>
        <div class="modal-title" id="modal-title">--</div>
        <div class="modal-score" id="modal-score">⭐ 豆瓣评分: --</div>
        <div style="font-weight:bold; margin-bottom:6px;">📖 剧情简介</div>
        <div class="modal-summary-text" id="modal-summary">暂无故事简介。</div>
      </div>
    </div>
  </div>

  <script>
    const dataContainer = {json_data};
    let allData = dataContainer.items || [];

    function getPosterUrls(url) {{
      if (!url) return [];
      return [
        url,
        'https://images.weserv.nl/?url=' + encodeURIComponent(url),
        'https://api.allorigins.win/raw?url=' + encodeURIComponent(url)
      ];
    }}

    function handleImgError(img) {{
      const fallbackList = JSON.parse(img.dataset.fallbacks || '[]');
      const currentIndex = parseInt(img.dataset.failCount || '0', 10);
      
      if (currentIndex < fallbackList.length) {{
        img.dataset.failCount = currentIndex + 1;
        img.src = fallbackList[currentIndex];
      }} else {{
        img.src = "data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22200%22%20height%3D%22300%22%20viewBox%3D%220%200%20200%20300%22%3E%3Crect%20fill%3D%22%23e0e0e0%22%20width%3D%22200%22%20height%3D%22300%22%2F%3E%3Ctext%20fill%3D%22%23888888%22%20font-family%3D%22sans-serif%22%20font-size%3D%2216%22%20text-anchor%3D%22middle%22%20x%3D%22100%22%20y%3D%22150%22%3E🎬%20暂无海报%3C%2Ftext%3E%3C%2Fsvg%3E";
        img.onerror = null;
      }}
    }}

    function renderGrid(items) {{
      const grid = document.getElementById('media-grid');
      grid.innerHTML = '';
      items.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'card';
        const urls = getPosterUrls(item.poster_url);
        const primaryUrl = urls[0] || '';
        const fallbacks = JSON.stringify(urls.slice(1));

        card.innerHTML = `
          <div class="poster-box">
            <img src="${{primaryUrl}}" 
                 data-fallbacks='${{fallbacks}}' 
                 data-fail-count="0" 
                 onerror="handleImgError(this)" 
                 alt="${{item.title}}" 
                 loading="lazy">
          </div>
          <div class="card-info">
            <span class="tag">${{item.category || '日剧'}}</span>
            <div class="title">${{item.title}}</div>
            <div class="score">⭐ 评分: ${{item.score}}</div>
          </div>
        `;
        card.addEventListener('click', () => openModal(item, primaryUrl, fallbacks));
        grid.appendChild(card);
      }});
    }}

    function openModal(item, primaryUrl, fallbacks) {{
      const modalImg = document.getElementById('modal-poster');
      modalImg.dataset.fallbacks = fallbacks;
      modalImg.dataset.failCount = "0";
      modalImg.src = primaryUrl;

      document.getElementById('modal-tag').innerText = item.category || '';
      document.getElementById('modal-title').innerText = item.title;
      document.getElementById('modal-score').innerText = `⭐ 评分: ${{item.score}}`;
      document.getElementById('modal-summary').innerText = item.summary || '暂无详细故事简介。';
      document.getElementById('modal-overlay').classList.add('active');
    }}

    function filterData() {{
      const searchText = document.getElementById('search-input').value.toLowerCase();
      const catVal = document.getElementById('category-filter').value;

      const filtered = allData.filter(item => {{
        const matchSearch = item.title.toLowerCase().includes(searchText);
        const matchCat = catVal === 'ALL' || item.category === catVal;
        return matchSearch && matchCat;
      }});
      renderGrid(filtered);
    }}

    document.getElementById('search-input').addEventListener('input', filterData);
    document.getElementById('category-filter').addEventListener('change', filterData);
    document.getElementById('modal-close').addEventListener('click', () => document.getElementById('modal-overlay').classList.remove('active'));

    window.onload = () => {{
      renderGrid(allData);
    }};
  </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ 已生成最新的 index.html 文件！")

if __name__ == "__main__":
    data = fetch_latest_media()
    generate_html(data)
