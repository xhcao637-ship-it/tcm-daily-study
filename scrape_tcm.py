#!/usr/bin/env python3
"""每日中医学习报告 - 聚焦家庭常见病证 + 心血管养护"""

import html
import json
import os
import random
import re
import urllib.request
from datetime import datetime, timezone, timedelta

HEADERS = {
    "User-Agent": "Mozilla/5.0 TCM-Daily-Study/1.0",
    "Accept": "text/html",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# === 动态池：从 slug_cache.json 加载 ===
SLUG_CACHE_FILE = "slug_cache.json"

# === 按功效分类学习 ===
HERB_CATEGORIES = {
    "解表药": ["解表", "发散", "风寒", "风热", "感冒", "恶寒", "发汗"],
    "清热药": ["清热", "泻火", "凉血", "解毒", "退热", "热毒"],
    "化痰止咳平喘药": ["化痰", "止咳", "平喘", "祛痰", "润肺", "宣肺"],
    "活血化瘀药": ["活血", "化瘀", "通经", "散瘀", "行血", "通络"],
    "补虚药": ["补气", "补血", "补阴", "补阳", "滋阴", "益气", "养血"],
    "安神药": ["安神", "镇静", "宁心", "失眠", "心悸", "养心"],
    "平肝息风药": ["平肝", "息风", "潜阳", "眩晕", "头晕", "降压", "熄风"],
}


def load_slug_cache():
    if not os.path.exists(SLUG_CACHE_FILE):
        print(f"⚠ {SLUG_CACHE_FILE} not found. Run build_cache.py first.")
        return {}, {}, {}
    with open(SLUG_CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    return cache.get("herbs", {}), cache.get("formulas", {}), cache.get("herb_categories", {})


def _raw_cache():
    if not os.path.exists(SLUG_CACHE_FILE):
        return {}
    with open(SLUG_CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

BASE_URL = "https://zysj.com.cn"


def fetch_page(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ⚠ {e}")
        return ""


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_sections(page_html):
    text = clean(page_html)
    headers = [
        "别名", "来源", "性味归经", "性味", "归经",
        "功能主治", "功效", "主治", "临床应用",
        "用法用量", "组成", "处方", "方义", "注意",
        "药理作用", "化学成分", "相关药方", "摘录",
    ]
    pattern = "|".join(re.escape(h) for h in headers)
    parts = re.split(f"({pattern})", text)
    info = {}
    i = 1
    while i < len(parts) - 1:
        key = parts[i].strip()
        val = re.sub(r"^[：:\s]+", "", parts[i + 1].strip())
        if val and len(val) > 1:
            info[key] = val[:300] + ("..." if len(val) > 300 else "")
        i += 2
    return info


def pick_fields(info, keys, max_fields=4):
    result = {}
    for k in keys:
        if k in info:
            result[k] = info[k]
        if len(result) >= max_fields:
            break
    return result


def fetch_item(slug, category):
    """Fetch a single herb or formula by slug."""
    url = f"{BASE_URL}/{category}/{slug}/index.html"
    page = fetch_page(url)
    if not page:
        return None
    # Extract title from <h1> or <title>
    title_match = re.search(r"<h1[^>]*>([^<]+)</h1>", page)
    title = clean(title_match.group(1)) if title_match else slug
    # Skip if it's a 404/index page (title matches category name)
    if title in ("中药方剂", "中药材", "中医世家"):
        return None
    info = extract_sections(page)
    return {"title": title, "url": url, "info": info}


def fetch_random_items(slugs, category, field_keys, count=3):
    """Fetch details for given slugs. Returns list of (title, url, fields)."""
    results = []
    for slug in slugs:
        if len(results) >= count:
            break
        print(f"  {slug}")
        item = fetch_item(slug, category)
        if item and item["info"]:
            fields = pick_fields(item["info"], field_keys)
            if fields:
                results.append((item["title"], item["url"], fields))
    return results


def fetch_and_filter(slugs, category, field_keys, keywords, count):
    """Fetch details for slugs, keep only those matching keywords in content."""
    results = []
    for slug in slugs:
        if len(results) >= count:
            break
        print(f"  {slug}")
        item = fetch_item(slug, category)
        if not item or not item["info"]:
            continue
        all_text = " ".join(item["info"].values())
        if not any(kw in all_text for kw in keywords):
            continue
        fields = pick_fields(item["info"], field_keys)
        if fields:
            results.append((item["title"], item["url"], fields))
    return results


# === 🍵 药食同源·养生茶饮 ===

DAILY_TEAS = [
    # --- 日常养生 ---
    {
        "name": "枸杞菊花茶",
        "materials": "枸杞10粒、杭白菊3-5朵",
        "method": "沸水冲泡，焖5分钟",
        "适用人群": "长期用眼、眼睛干涩疲劳者",
        "功效": "清肝明目、滋补肝肾",
        "注意": "脾虚便溏者少饮",
        "category": "daily",
    },
    {
        "name": "熟地黄怀山药水",
        "materials": "熟地黄10g、干怀山药15g",
        "method": "加水煮20分钟，代茶饮",
        "适用人群": "肾虚腰酸、头晕耳鸣、女性气血不足面色萎黄者",
        "功效": "滋阴补肾、健脾益气",
        "注意": "脾胃湿滞、腹胀者慎用",
        "category": "daily",
    },
    {
        "name": "黄芪红枣茶",
        "materials": "黄芪10g、红枣3-5枚（去核）",
        "method": "沸水冲泡或煮10分钟",
        "适用人群": "气虚乏力、容易感冒、面色苍白者",
        "功效": "补气固表、养血安神",
        "注意": "感冒发热期间停饮；阴虚火旺者慎用",
        "category": "daily",
    },
    {
        "name": "玫瑰花茶",
        "materials": "干玫瑰花5-6朵",
        "method": "沸水冲泡，焖3分钟",
        "适用人群": "女性经前胸胁胀痛、情绪郁闷、面部色斑者",
        "功效": "疏肝理气、活血化瘀、美容养颜",
        "注意": "月经量大者经期停饮；孕妇慎用",
        "category": "daily",
    },
    {
        "name": "桂圆红枣枸杞茶",
        "materials": "桂圆肉5-6颗、红枣3枚、枸杞10粒",
        "method": "煮15分钟或保温杯焖泡",
        "适用人群": "女性气血两虚、面色无华、手脚冰凉、失眠多梦者",
        "功效": "补气养血、安神助眠",
        "注意": "上火、口腔溃疡时停饮；糖尿病患者慎用",
        "category": "daily",
    },
    {
        "name": "陈皮普洱茶",
        "materials": "陈皮一小块、普洱茶适量",
        "method": "沸水冲泡",
        "适用人群": "饭后腹胀、消化不良、痰多者",
        "功效": "理气健脾、燥湿化痰、消食",
        "注意": "胃酸过多者少饮",
        "category": "daily",
    },
    {
        "name": "西洋参麦冬茶",
        "materials": "西洋参3-5片、麦冬10粒",
        "method": "沸水冲泡，可反复续水",
        "适用人群": "熬夜伤阴、口干咽燥、心烦失眠者；中老年气阴两虚",
        "功效": "益气养阴、清热生津",
        "注意": "脾胃虚寒、腹泻者慎用",
        "category": "daily",
    },
    {
        "name": "山楂荷叶茶",
        "materials": "干山楂片5-6片、干荷叶3g",
        "method": "沸水冲泡，焖10分钟",
        "适用人群": "血脂偏高、体型偏胖、饮食油腻者",
        "功效": "消食化积、降脂减肥",
        "注意": "胃酸过多、胃溃疡者慎用；孕妇忌用",
        "category": "daily",
    },
    {
        "name": "当归红枣茶",
        "materials": "当归5g、红枣5枚（去核）",
        "method": "加水煮15分钟，代茶饮",
        "适用人群": "女性月经量少色淡、经后调养、面色萎黄者",
        "功效": "补血活血、调经止痛",
        "注意": "月经量多者慎用；孕妇忌用",
        "category": "daily",
    },
    {
        "name": "丹参山楂茶",
        "materials": "丹参5g、山楂片5-6片",
        "method": "沸水冲泡或煮10分钟",
        "适用人群": "中老年心血管保健、血瘀体质、胸闷不适者",
        "功效": "活血化瘀、消食降脂",
        "注意": "孕妇忌用；服用抗凝药物者咨询医师",
        "category": "daily",
    },
    # --- 家庭常见病对症茶饮 ---
    {
        "name": "生姜红糖水",
        "materials": "生姜3-5片、红糖适量",
        "method": "煮10分钟，趁热饮用",
        "适用人群": "风寒感冒初起：怕冷、流清涕、头痛、无汗",
        "功效": "温中散寒、发汗解表",
        "注意": "风热感冒（黄涕、咽痛）禁用；糖尿病患者去红糖",
        "category": "cold",
    },
    {
        "name": "葱白豆豉汤",
        "materials": "葱白3段（连须）、淡豆豉10g",
        "method": "煮5分钟，趁热服",
        "适用人群": "风寒感冒轻症：微恶寒、鼻塞、头痛",
        "功效": "通阳发汗、解表散寒",
        "注意": "出汗后即停，不可过汗",
        "category": "cold",
    },
    {
        "name": "金银花连翘茶",
        "materials": "金银花10g、连翘10g",
        "method": "沸水冲泡或煮5分钟",
        "适用人群": "风热感冒：咽喉肿痛、发热、黄涕",
        "功效": "清热解毒、疏散风热",
        "注意": "脾胃虚寒者慎用",
        "category": "cold",
    },
    {
        "name": "桑叶菊花茶",
        "materials": "桑叶6g、菊花6g、薄荷3g（后下）",
        "method": "沸水冲泡，焖5分钟",
        "适用人群": "风热感冒初起：头痛目赤、咽干微咳",
        "功效": "疏风清热、清利头目",
        "注意": "风寒感冒不宜",
        "category": "cold",
    },
    {
        "name": "陈皮生姜水",
        "materials": "陈皮6g、生姜3片",
        "method": "煮10分钟",
        "适用人群": "受凉后胃部不适、恶心呕吐、腹胀",
        "功效": "温胃止呕、理气化痰",
        "注意": "胃热呕吐（口臭、喜冷饮）不宜",
        "category": "digestion",
    },
    {
        "name": "山楂麦芽水",
        "materials": "山楂10g、炒麦芽15g",
        "method": "煮15分钟，代茶饮",
        "适用人群": "饮食积滞：腹胀、嗳气、不消化（大人小孩均可）",
        "功效": "消食化积、健胃",
        "注意": "哺乳期女性慎用麦芽（有回乳作用）",
        "category": "digestion",
    },
    {
        "name": "川贝雪梨水",
        "materials": "川贝母3g（研碎）、雪梨1个（去核）、冰糖适量",
        "method": "隔水炖30分钟",
        "适用人群": "干咳少痰、咽干口燥、燥咳（秋冬常见）",
        "功效": "润肺止咳、清热化痰",
        "注意": "寒咳（痰白清稀、怕冷）不宜",
        "category": "cough",
    },
    {
        "name": "罗汉果胖大海茶",
        "materials": "罗汉果1/4个、胖大海2枚",
        "method": "沸水冲泡，焖15分钟",
        "适用人群": "咽喉肿痛、声音嘶哑、干咳",
        "功效": "清热利咽、润肺化痰",
        "注意": "脾胃虚寒、腹泻者慎用",
        "category": "cough",
    },
    {
        "name": "紫苏叶生姜水",
        "materials": "紫苏叶6g、生姜3片、红糖适量",
        "method": "煮5分钟，趁热饮",
        "适用人群": "风寒感冒兼有恶心呕吐、吃了生冷食物后腹痛",
        "功效": "解表散寒、行气和胃",
        "注意": "风热感冒不宜；气虚多汗者慎用",
        "category": "cold",
    },
    {
        "name": "薏米赤小豆水",
        "materials": "薏米30g、赤小豆20g",
        "method": "提前浸泡2小时，煮40分钟",
        "适用人群": "体内湿气重：身体困重、大便黏腻、舌苔白腻",
        "功效": "健脾祛湿、利水消肿",
        "注意": "孕妇慎用薏米；便秘者不宜多饮",
        "category": "daily",
    },
]

TEA_CATEGORY_LABELS = {
    "daily": "☀️ 日常养生",
    "cold": "🤧 感冒对症",
    "cough": "💨 咳嗽对症",
    "digestion": "🍽️ 消化不适",
}


def pick_daily_teas(count=4):
    """Pick a balanced selection: some daily + some symptom-based."""
    daily = [t for t in DAILY_TEAS if t["category"] == "daily"]
    symptom = [t for t in DAILY_TEAS if t["category"] != "daily"]
    random.shuffle(daily)
    random.shuffle(symptom)
    # 2 daily + 2 symptom (or adjust if not enough)
    picked = daily[:2] + symptom[:2]
    random.shuffle(picked)
    return picked[:count]


def format_tea_section(teas):
    lines = []
    for t in teas:
        cat_label = TEA_CATEGORY_LABELS.get(t["category"], "")
        lines.append(f"### 🍵 {t['name']}  `{cat_label}`\n")
        lines.append(f"- **材料**：{t['materials']}")
        lines.append(f"- **做法**：{t['method']}")
        lines.append(f"- **适用人群**：{t['适用人群']}")
        lines.append(f"- **功效**：{t['功效']}")
        lines.append(f"- ⚠️ **注意**：{t['注意']}")
        lines.append("")
    return "\n".join(lines)


def generate_report(date_str, herb_by_category, formulas, teas):
    lines = [
        f"# 🌿 每日中医学习 ({date_str})\n",
        "按功效分类系统学习中药材，每日一方一茶。\n",
        "数据来源：[中医世家](https://zysj.com.cn) + 经典中医养生方\n",
        "---\n",
        "## 🍵 今日养生茶饮\n",
        format_tea_section(teas),
        "---\n",
        "## 🌱 今日中药材（按功效分类）\n",
    ]

    cat_icons = {
        "解表药": "🤧", "清热药": "🔥", "化痰止咳平喘药": "💨",
        "活血化瘀药": "🩸", "补虚药": "💪", "安神药": "😴", "平肝息风药": "🧠",
    }

    for cat_name, items in herb_by_category.items():
        icon = cat_icons.get(cat_name, "🌱")
        lines.append(f"### {icon} {cat_name}\n")
        if not items:
            lines.append(f"*今日未匹配到{cat_name}*\n")
        for name, url, fields in items:
            lines.append(f"**[{name}]({url})**\n")
            for k, v in fields.items():
                lines.append(f"- **{k}**：{v}")
            lines.append("")

    lines.append("---\n")
    lines.append("## 📜 今日方剂\n")
    if not formulas:
        lines.append("*今日未获取到方剂信息*\n")
    for name, url, fields in formulas:
        lines.append(f"### [{name}]({url})\n")
        for k, v in fields.items():
            lines.append(f"- **{k}**：{v}")
        lines.append("")

    lines.append("---\n")
    lines.append(f"*生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n")
    lines.append("*免责声明：仅供学习参考，不构成医疗建议。*\n")
    return "\n".join(lines)


import json


HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def pick_without_repeat(pool, key, count, history):
    """Pick items from pool that haven't been shown recently.
    Preserves pool order (priority-sorted) instead of shuffling.
    Resets when all items have been used."""
    used = set(history.get(key, []))
    available = [x for x in pool if x not in used]
    # Reset if pool exhausted
    if len(available) < count:
        available = list(pool)
        history[key] = []
    picked = available[:count]
    history.setdefault(key, []).extend(picked)
    return picked


def pick_teas_without_repeat(count, history):
    """Pick teas without repeat, balanced between daily and symptom."""
    used = set(history.get("teas", []))
    daily = [t for t in DAILY_TEAS if t["category"] == "daily" and t["name"] not in used]
    symptom = [t for t in DAILY_TEAS if t["category"] != "daily" and t["name"] not in used]
    # Reset if not enough
    if len(daily) < 2 or len(symptom) < 2:
        daily = [t for t in DAILY_TEAS if t["category"] == "daily"]
        symptom = [t for t in DAILY_TEAS if t["category"] != "daily"]
        history["teas"] = []
    random.shuffle(daily)
    random.shuffle(symptom)
    picked = daily[:2] + symptom[:2]
    random.shuffle(picked)
    picked = picked[:count]
    history.setdefault("teas", []).extend([t["name"] for t in picked])
    return picked


def main():
    now = datetime.now(timezone(timedelta(hours=8)))
    date_str = now.strftime("%Y-%m-%d")
    print(f"=== 每日中医学习 {date_str} ===\n")

    history = load_history()

    herb_cache, formula_cache, herb_categories = load_slug_cache()
    herb_priority = cache_data.get("herb_priority", {}) if (cache_data := _raw_cache()) else {}
    all_formula_slugs = list(formula_cache.keys())
    print(f"📦 缓存: {len(herb_cache)} 中药材, {len(all_formula_slugs)} 方剂")
    for cat, slugs in herb_categories.items():
        if cat in HERB_CATEGORIES:
            p0 = sum(1 for s in slugs if herb_priority.get(s, 2) == 0)
            print(f"   {cat}: {len(slugs)} (常用: {p0})")
    print()

    herb_keys = ["性味归经", "性味", "归经", "功能主治", "功效", "临床应用", "用法用量", "注意"]
    formula_keys = ["组成", "处方", "功能主治", "功效", "主治", "用法用量", "方义"]

    # 按功效分类，每类直接从分类池里选1味
    # 优先选常用药(P0)，用完后再选其他(P2)
    herb_by_category = {}
    for cat_name in HERB_CATEGORIES:
        pool = herb_categories.get(cat_name, [])
        if not pool:
            print(f"🌱 {cat_name}: 池子为空，跳过")
            herb_by_category[cat_name] = []
            continue
        # Sort pool: P0 first (shuffled), then P2 (shuffled)
        p0 = [s for s in pool if herb_priority.get(s, 2) == 0]
        p2 = [s for s in pool if herb_priority.get(s, 2) != 0]
        random.shuffle(p0)
        random.shuffle(p2)
        pool_sorted = p0 + p2
        print(f"🌱 {cat_name} (池: {len(pool)})")
        slugs = pick_without_repeat(pool_sorted, f"herb_{cat_name}", 2, history)
        items = fetch_random_items(slugs, "zhongyaocai", herb_keys, 1)
        herb_by_category[cat_name] = items

    # 方剂：随机2个
    print("📜 方剂")
    fm_slugs = pick_without_repeat(all_formula_slugs, "formulas", 4, history)
    formulas = fetch_random_items(fm_slugs, "zhongyaofang", formula_keys, 2)

    # 茶饮：1个
    print("🍵 养生茶饮")
    teas = pick_teas_without_repeat(1, history)
    print(f"  选取: {teas[0]['name']}" if teas else "  无")

    save_history(history)

    report = generate_report(date_str, herb_by_category, formulas, teas)

    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{date_str}.md", "w", encoding="utf-8") as f:
        f.write(report)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 🌿 每日中医学习\n\n")
        f.write("每天自动生成：按功效分类学中药 + 方剂 + 养生茶饮。\n\n")
        f.write(f"📅 **最新报告**：[{date_str}](reports/{date_str}.md)\n\n")
        f.write(report)

    print(f"\n✅ 完成: reports/{date_str}.md")


if __name__ == "__main__":
    main()
