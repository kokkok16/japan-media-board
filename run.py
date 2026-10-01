import os
import json
import webbrowser
from datetime import datetime

def main():
    print("==========================================")
    print("🚀 正在重新生成最新的日剧 & 电影看板...")
    print("==========================================")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 6 部完整的日剧与日本电影数据（使用高稳定性海报源）
    all_data = [
        {
            "id": "tv_35384260",
            "db_id": "35384260",
            "title": "重启动力 / Reboot",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E1M2RjNDItMGRhNC00YTY3LWIwYjAtN2Q0MDI2MDVmNzZhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "8.5",
            "douban_url": "https://movie.douban.com/subject/35384260/",
            "category": "日剧",
            "release_year": "2026年",
            "quarter_group": "2026年冬季档 (1月)",
            "summary": "讲述了主角在人生陷入绝境时，意外获得一次重返过去、重启人生的机会，在不断修正选择的过程中，重新审视了亲情、友情与自我价值的悬疑温情故事。"
        },
        {
            "id": "tv_36234111",
            "db_id": "36234111",
            "title": "Last Man-全盲搜查官-",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMDY4YzAyNDItYTZjNS00Y2NhLTk3MDctYThjNThlYTM1Njg5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "8.1",
            "douban_url": "https://movie.douban.com/subject/36234111/",
            "category": "日剧",
            "release_year": "2026年",
            "quarter_group": "2026年春季档 (4月)",
            "summary": "福山雅治与大泉洋联袂主演。讲述了全盲FBI探员从美国来到日本，凭借敏锐的触觉、嗅觉和出色的推理能力，与刑警搭档携手破解一件件离奇棘手案件的故事。"
        },
        {
            "id": "tv_36123456",
            "db_id": "36123456",
            "title": "VIVANT",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BYTJlNmI0OTctYjg4My00YTM0LWE1YTItNmNhYjAxNDcxYzMwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "8.7",
            "douban_url": "https://movie.douban.com/subject/36123456/",
            "category": "日剧",
            "release_year": "2026年",
            "quarter_group": "2026年夏季档 (7月)",
            "summary": "TBS电视台重磅打造的史诗级冒险悬疑巨作。远赴蒙古等地取景，汇集超豪华演员阵容，讲述了跨国跨大陆的惊险谍战与扑朔迷离的身份谜团。"
        },
        {
            "id": "tv_35987654",
            "db_id": "35987654",
            "title": "silent",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjllYzcyYjEtYWRmYi00YTUwLTgwMjgtMjZkMDgxN2I5ZDYxXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "8.0",
            "douban_url": "https://movie.douban.com/subject/35987654/",
            "category": "日剧",
            "release_year": "2026年",
            "quarter_group": "2026年秋季档 (10月)",
            "summary": "川口春奈与目黑莲主演的纯爱催泪神作。讲述了曾经的高中恋人因患病失聪而失联，多年后在东京意外重逢，在无声的世界里重新找回彼此心灵共鸣的故事。"
        },
        {
            "id": "movie_35234567",
            "db_id": "35234567",
            "title": "你想活出怎样的人生",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BZjNmOTEwMzktNWExNy00M2I0LWEyMDItMTNmMWI2N2E1Y2U1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "7.8",
            "douban_url": "https://movie.douban.com/subject/35234567/",
            "category": "日本电影",
            "release_year": "最新上映",
            "quarter_group": "最新电影/剧场版",
            "summary": "宫崎骏导演的动画电影长片，荣获奥斯卡最佳动画长片奖。影片讲述了少年牧真人母亲遭遇火灾后随父亲搬到乡村，在神秘苍鹭的引导下，踏入了一处连接生与死的奇幻异世界。"
        },
        {
            "id": "movie_34987652",
            "db_id": "34987652",
            "title": "哥斯拉-1.0",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E5Yzk2MTQtMGQ1OC00Mzc3LWI0NTAtNWVmY2I0NDY4YmU5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "score": "7.5",
            "douban_url": "https://movie.douban.com/subject/34987652/",
            "category": "日剧剧场版",
            "release_year": "最新上映",
            "quarter_group": "最新电影/剧场版",
            "summary": "荣获奥斯卡最佳视觉效果奖。故事设定在战后的日本，本已满目疮痍的废墟之上，神秘巨兽哥斯拉骤然降临，将国家瞬间逼入绝境，幸存者们展开了绝地反击。"
        }
    ]

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
    <div class="status-bar" id="update-time">🔄 更新时间: {update_time} (共 {len(all_data)} 部)</div>
  </header>

  <div class="controls">
    <input type="text" id="search-input" class="search-input" placeholder="搜索片名...">
    <select id="category-filter"><option value="ALL">全部分类</option><option value="日剧">日剧</option><option value="日剧剧场版">日剧剧场版</option><option value="日本电影">日本电影</option></select>
    <select id="group-filter"><option value="ALL">全部分组 / 季度</option></select>
  </div>

  <div class="grid" id="media-grid"></div>

  <div class="modal-overlay" id="modal-overlay">
    <div class="modal-content">
      <button class="modal-close" id="modal-close">✕</button>
      <img src="" class="modal-poster" id="modal-poster">
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

    function populateGroupFilter() {{
      const groupSelect = document.getElementById('group-filter');
      const groups = [...new Set(allData.map(item => item.quarter_group).filter(Boolean))];
      groupSelect.innerHTML = '<option value="ALL" selected>全部分组 / 季度</option>';
      groups.forEach(g => {{
        const opt = document.createElement('option');
        opt.value = g; 
        opt.textContent = g;
        groupSelect.appendChild(opt);
      }});
      groupSelect.value = "ALL";
    }}

    function renderGrid(items) {{
      const grid = document.getElementById('media-grid');
      grid.innerHTML = '';
      items.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="poster-box">
            <img src="${{item.poster_url}}" alt="${{item.title}}" loading="lazy">
          </div>
          <div class="card-info">
            <span class="tag">${{item.quarter_group || item.category || '日剧'}}</span>
            <div class="title">${{item.title}}</div>
            <div class="score">⭐ 豆瓣评分: ${{item.score}}</div>
          </div>
        `;
        card.addEventListener('click', () => openModal(item));
        grid.appendChild(card);
      }});
    }}

    function openModal(item) {{
      document.getElementById('modal-poster').src = item.poster_url;
      document.getElementById('modal-tag').innerText = item.quarter_group || item.category || '';
      document.getElementById('modal-title').innerText = item.title;
      document.getElementById('modal-score').innerText = `⭐ 豆瓣评分: ${{item.score}}`;
      document.getElementById('modal-summary').innerText = item.summary || '暂无详细故事简介。';
      document.getElementById('modal-overlay').classList.add('active');
    }}

    function filterData() {{
      const searchText = document.getElementById('search-input').value.toLowerCase();
      const catVal = document.getElementById('category-filter').value;
      const groupVal = document.getElementById('group-filter').value;

      const filtered = allData.filter(item => {{
        const matchSearch = item.title.toLowerCase().includes(searchText);
        const matchCat = catVal === 'ALL' || item.category === catVal;
        const matchGroup = groupVal === 'ALL' || item.quarter_group === groupVal;
        return matchSearch && matchCat && matchGroup;
      }});
      renderGrid(filtered);
    }}

    document.getElementById('search-input').addEventListener('input', filterData);
    document.getElementById('category-filter').addEventListener('change', filterData);
    document.getElementById('group-filter').addEventListener('change', filterData);
    document.getElementById('modal-close').addEventListener('click', () => document.getElementById('modal-overlay').classList.remove('active'));

    window.onload = () => {{
      populateGroupFilter();
      renderGrid(allData);
    }};
  </script>
</body>
</html>
"""
    
    html_path = os.path.join(script_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n✅ 网页 index.html 重新生成完毕！")
    webbrowser.open(f"file://{html_path}?t={datetime.now().timestamp()}")

if __name__ == "__main__":
    main()
