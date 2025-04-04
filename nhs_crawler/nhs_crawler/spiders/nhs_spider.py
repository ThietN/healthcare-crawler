import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import re

class NHSSpider(scrapy.Spider):
    name = 'nhs_spider'
    start_urls = ['https://www.nhs.uk/conditions/']

    def parse(self, response):
        # Lấy tất cả link bệnh
        condition_links = response.css('.nhsuk-list a::attr(href)').getall()
        for link in condition_links:
            yield response.follow(link, self.parse_condition)

    def parse_condition(self, response):
        # 1️⃣ Lấy tiêu đề bệnh từ <h1>
        disease_name = response.css('div.nhsuk-grid-column-two-thirds h1::text').get()

        # 2️⃣ Nếu không có, tìm trong thẻ "Overview"
        if not disease_name or disease_name.strip() == "":
            overview_heading = response.css("h2::text").get()
            if overview_heading and "overview" in overview_heading.lower():
                # Lấy span chứa tên bệnh
                disease_name = response.css("h2 + p span::text").get()

        # 3️⃣ Nếu vẫn không có tên bệnh, bỏ qua
        if not disease_name or disease_name.strip() == "":
            return

        disease_name = disease_name.strip()

        # 4️⃣ Lấy toàn bộ nội dung của trang
        page_text = response.css('div.nhsuk-grid-column-two-thirds *::text').getall()
        page_text = "\n".join([text.strip() for text in page_text if text.strip()])

        # 5️⃣ Loại bỏ các nội dung không cần thiết
        unwanted_sections = ["Page last reviewed", "Next review due", "Was this information useful?"]
        for section in unwanted_sections:
            page_text = re.sub(section + ".*", "", page_text, flags=re.DOTALL)

        yield {
            'Disease': disease_name,
            'Symptoms': page_text  # Lưu toàn bộ nội dung trang
        }

# Chạy Scrapy và lưu kết quả vào Excel
output_filename = f"nhs_conditions_{datetime.now().year}.xlsx"

class ExcelPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def close_spider(self, spider):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_excel(output_filename, index=False)
            print(f"✅ File saved: {output_filename}")
        else:
            print("❌ No valid data found. No file saved.")

# Cấu hình Scrapy
process = CrawlerProcess(settings={
    "ITEM_PIPELINES": {'__main__.ExcelPipeline': 1},
})

process.crawl(NHSSpider)
process.start()
