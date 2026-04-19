import asyncio
import json
import os
import requests
from datetime import datetime
from playwright.async_api import async_playwright

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
TARGET_SCHEME_URLS = [
    "https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/nippon-india-taiwan-equity-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/quant-small-cap-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth"
]

DATA_RAW_DIR      = "data/raw"
OUTPUT_PATH       = os.path.join(DATA_RAW_DIR, "targeted_schemes.json")

os.makedirs(DATA_RAW_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# Step 1: Discover all scheme URLs from an AMC page
# ─────────────────────────────────────────────
async def scrape_amc_schemes(browser, amc_url):
    """Returns a list of {name, url} dicts from the AMC list page."""
    print(f"\n📂 Scraping AMC page: {amc_url}")
    page = await browser.new_page()
    await page.goto(amc_url, wait_until="networkidle")

    scheme_links = await page.query_selector_all("a.seoFundExtraDetails_anchorLink__fJRi4")
    schemes = []
    for link in scheme_links:
        name = await link.inner_text()
        href = await link.get_attribute("href")
        if href:
            full_url = f"https://groww.in{href}" if href.startswith("/") else href
            schemes.append({"name": name.strip(), "url": full_url})

    await page.close()
    print(f"   → Found {len(schemes)} schemes")
    return schemes


# ─────────────────────────────────────────────
# Step 2: Extract the 6 key factual fields from each scheme page
# ─────────────────────────────────────────────
async def scrape_scheme_details(browser, scheme):
    """
    Extracts factual data for the 6 required fields:
    NAV, Minimum SIP, Fund Size, Exit Load, Expense Ratio, Rating
    and any available document links.
    """
    print(f"  📊 Scraping: {scheme['name']}")
    page = await browser.new_page()
    try:
        await page.goto(scheme["url"], wait_until="networkidle", timeout=60000)

        # ── Helper: locate a value by the text label next to it ──────────────
        async def get_value_by_label(label_text):
            """
            Finds a container whose text contains the label,
            then reads the sibling/child value element.
            Uses a JS evaluate for robustness across hash-suffixed class names.
            """
            try:
                value = await page.evaluate(f"""
                    () => {{
                        const labels = Array.from(document.querySelectorAll('*'));
                        for (const el of labels) {{
                            if (el.children.length === 0 &&
                                el.textContent.trim().toLowerCase() === '{label_text.lower()}') {{
                                const parent = el.closest('[class]');
                                const sibling = parent?.nextElementSibling ||
                                                parent?.parentElement?.querySelector('[class*="val_"]');
                                return sibling ? sibling.textContent.trim() : null;
                            }}
                        }}
                        return null;
                    }}
                """)
                return value or "N/A"
            except Exception:
                return "N/A"

        # ── Extract the 6 Key Data Fields ─────────────────────────────────
        record = {
            "scheme_name":   scheme["name"],
            "source_url":    scheme["url"],
            "last_updated":  datetime.now().strftime("%Y-%m-%d"),

            # NAV – has a dedicated CSS class from earlier verification
            "nav":           await get_text(page, "div.val_currentNav__H670Q"),

            # Remaining 5 fields – targeted by label text
            "min_sip":       await get_value_by_label("Min. for SIP"),
            "fund_size_aum": await get_value_by_label("Fund size (AUM)"),
            "expense_ratio": await get_value_by_label("Expense ratio"),
            "exit_load":     await get_value_by_label("Exit load"),
            "rating":        await get_value_by_label("Rating"),

            # Official document links (SID / KIM / Factsheet)
            "documents": []
        }

        # ── Document Link Harvesting ──────────────────────────────────────
        links = await page.query_selector_all("a")
        for link in links:
            text = (await link.inner_text()).lower().strip()
            href = await link.get_attribute("href")
            if href and any(kw in text for kw in ["sid", "kim", "factsheet",
                                                   "scheme information",
                                                   "key information"]):
                record["documents"].append({
                    "type": text.upper(),
                    "url":  href
                })

        return record

    except Exception as e:
        print(f"    ⚠️  Error scraping {scheme['name']}: {e}")
        return None
    finally:
        await page.close()


# ─────────────────────────────────────────────
# Helper: safe text extractor by CSS selector
# ─────────────────────────────────────────────
async def get_text(page, selector):
    try:
        el = await page.query_selector(selector)
        return await el.inner_text() if el else "N/A"
    except Exception:
        return "N/A"


# ─────────────────────────────────────────────
# Step 3: Download a document (PDF) to data/raw/
# ─────────────────────────────────────────────
def download_file(url, folder, filename):
    if not url.startswith("http"):
        return None
    try:
        resp = requests.get(url, stream=True, timeout=30)
        if resp.status_code == 200:
            safe_name = "".join(c if c.isalnum() else "_" for c in filename) + ".pdf"
            path = os.path.join(folder, safe_name)
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return path
    except Exception as e:
        print(f"      ⬇️  Download failed for {url}: {e}")
    return None


# ─────────────────────────────────────────────
# Main Orchestrator
# ─────────────────────────────────────────────
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        all_records = []

        for scheme_url in TARGET_SCHEME_URLS:
            # Note: We wrap the URL in the format expected by scrape_scheme_details
            # In the old version, name was found on the AMC page. Here we'll title-case the slug.
            name_parts = scheme_url.split("/")[-1].replace("-", " ")
            scheme_obj = {"name": name_parts.title(), "url": scheme_url}
            
            record = await scrape_scheme_details(browser, scheme_obj)
            if record:
                all_records.append(record)

        # ── Save targeted_schemes.json ─────────────────────────────────
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(all_records, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Ingestion complete. {len(all_records)} schemes saved → {OUTPUT_PATH}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
