#!/usr/bin/env python3
"""从中医世家抓取中药材，提取功效并按分类归档到 slug_cache.json。
支持增量：已归类的不会重新抓取。"""

import html
import json
import os
import re
import time
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 TCM-Daily-Study/1.0",
    "Accept": "text/html",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

CACHE_FILE = "slug_cache.json"

HERB_CATEGORIES = {
    "解表药": ["解表", "发散", "风寒", "风热", "感冒", "恶寒", "发汗", "散寒", "疏风", "辛温解表", "辛凉解表"],
    "清热药": ["清热", "泻火", "凉血", "解毒", "退热", "热毒", "清肝", "清肺", "清胃"],
    "化痰止咳平喘药": ["化痰", "止咳", "平喘", "祛痰", "润肺", "宣肺", "降气", "痰饮"],
    "活血化瘀药": ["活血", "化瘀", "通经", "散瘀", "行血", "通络", "破血", "逐瘀"],
    "补虚药": ["补气", "补血", "补阴", "补阳", "滋阴", "益气", "养血", "壮阳", "填精", "益精"],
    "安神药": ["安神", "镇静", "宁心", "失眠", "心悸", "养心", "定志", "镇惊"],
    "平肝息风药": ["平肝", "息风", "潜阳", "眩晕", "头晕", "熄风", "镇痉", "抽搐", "痉挛"],
    "消食药": ["消食", "消积", "健胃", "化积", "消胀", "食积"],
    "理气药": ["理气", "行气", "疏肝", "破气", "降气", "宽胸", "气滞"],
    "祛湿药": ["祛湿", "利湿", "燥湿", "化湿", "利水", "渗湿", "通淋"],
    "止血药": ["止血", "凉血止血", "收敛止血", "化瘀止血"],
    "收涩药": ["收涩", "固涩", "涩精", "止泻", "固表", "敛汗", "缩尿"],
}


def fetch_page(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    ⚠ {e}")
        return ""


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


from common_herbs import COMMON_HERBS


def classify_herb(page_html, slug):
    """Extract name, classify herb, and assign priority."""
    text = clean(page_html)
    title_m = re.search(r"<h1[^>]*>([^<]+)</h1>", page_html)
    title = clean(title_m.group(1)) if title_m else ""
    if title in ("中药材", "中医世家", ""):
        return None, [], 2

    categories = []
    for cat_name, keywords in HERB_CATEGORIES.items():
        if any(kw in text for kw in keywords):
            categories.append(cat_name)

    # Priority: 0 = common (教材必学), 1 = 药典收录, 2 = other
    priority = 0 if slug in COMMON_HERBS else 2
    return title, categories, priority


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def main():
    cache = load_cache()

    # Ensure structure
    if "herbs" not in cache:
        cache["herbs"] = {}
    if "herb_categories" not in cache:
        cache["herb_categories"] = {cat: [] for cat in HERB_CATEGORIES}
    if "classified_herbs" not in cache:
        cache["classified_herbs"] = []
    if "formulas" not in cache:
        cache["formulas"] = {}

    # Step 1: Scrape herb index if not done
    if len(cache["herbs"]) < 100:
        print("=== 抓取中药材索引 ===")
        for idx in range(1, 25):
            url = f"https://zysj.com.cn/zhongyaocai/index__{idx}.html"
            print(f"  索引页 {idx}")
            page = fetch_page(url)
            if not page:
                continue
            for m in re.finditer(r'href="/zhongyaocai/([^/"]+)/index\.html"[^>]*>([^<]+)</a>', page):
                slug, name = m.group(1), m.group(2).strip()
                if slug not in cache["herbs"] and name and len(name) > 1:
                    cache["herbs"][slug] = name
            time.sleep(0.3)
        save_cache(cache)
        print(f"✅ 索引: {len(cache['herbs'])} 中药材\n")

    # Step 2: Scrape formula index if not done
    if len(cache["formulas"]) < 100:
        print("=== 抓取方剂索引 ===")
        for idx in range(1, 25):
            url = f"https://zysj.com.cn/zhongyaofang/index_{idx}.html"
            print(f"  索引页 {idx}")
            page = fetch_page(url)
            if not page:
                continue
            for m in re.finditer(r'href="/zhongyaofang/([^/"]+)/index\.html"[^>]*>([^<]+)</a>', page):
                slug, name = m.group(1), m.group(2).strip()
                if slug not in cache["formulas"] and name and len(name) > 1:
                    cache["formulas"][slug] = name
            time.sleep(0.3)
        save_cache(cache)
        print(f"✅ 索引: {len(cache['formulas'])} 方剂\n")

    # Step 3: Classify herbs (incremental — skip already classified)
    classified = set(cache["classified_herbs"])
    unclassified = [s for s in cache["herbs"] if s not in classified]
    print(f"=== 归类中药材: {len(unclassified)} 待处理, {len(classified)} 已完成 ===")

    batch_size = 200  # Process in batches to allow incremental saves
    batch = unclassified[:batch_size]

    for i, slug in enumerate(batch):
        name = cache["herbs"][slug]
        url = f"https://zysj.com.cn/zhongyaocai/{slug}/index.html"
        print(f"  [{i+1}/{len(batch)}] {name} ({slug})")
        page = fetch_page(url)
        if not page:
            cache["classified_herbs"].append(slug)  # Mark as done even if failed
            continue

        title, categories, priority = classify_herb(page, slug)
        if not title:
            cache["classified_herbs"].append(slug)
            continue

        for cat in categories:
            cat_list = cache["herb_categories"].setdefault(cat, [])
            if slug not in cat_list:
                cat_list.append(slug)

        if not categories:
            other_list = cache["herb_categories"].setdefault("其他", [])
            if slug not in other_list:
                other_list.append(slug)

        # Store priority
        cache.setdefault("herb_priority", {})[slug] = priority

        cache["classified_herbs"].append(slug)

        # Save every 50 items
        if (i + 1) % 50 == 0:
            save_cache(cache)
            print(f"  💾 已保存 ({i+1}/{len(batch)})")

        time.sleep(0.3)

    save_cache(cache)

    # Print summary
    print(f"\n=== 归类结果 ===")
    print(f"中药材总数: {len(cache['herbs'])}")
    print(f"已归类: {len(cache['classified_herbs'])}")
    print(f"方剂总数: {len(cache['formulas'])}")
    for cat, slugs in cache["herb_categories"].items():
        print(f"  {cat}: {len(slugs)}")

    remaining = len(cache["herbs"]) - len(cache["classified_herbs"])
    if remaining > 0:
        print(f"\n⚠ 还有 {remaining} 个未归类，请再次运行 build_cache.py 继续")
    else:
        print(f"\n✅ 全部归类完成！")


if __name__ == "__main__":
    main()
