import scrapy
from scrapy_selenium import SeleniumRequest
from urllib.parse import urljoin

class AmazonFashionDetailedSpider(scrapy.Spider):
    name = 'amazon_fashion_detailed'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/fashion']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        # Identify main categories or featured products to start scraping from
        # This part requires adjusting based on the site's structure
        category_links = response.xpath('//a[contains(@href, "/fashion/")]')
        for link in category_links:
            category_url = link.xpath('.//@href').extract_first()
            if category_url:
                full_url = urljoin("https://www.amazon.com", category_url)
                yield SeleniumRequest(url=full_url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        # Parse individual products on the category page
        product_links = response.xpath('//div[contains(@data-component-type, "s-search-result")]//a[@class="a-link-normal s-no-outline"]/@href').extract()
        for product_link in product_links:
            product_url = urljoin(response.url, product_link)
            yield SeleniumRequest(url=product_url, callback=self.parse_product_details)

        # Pagination handling (needs adjustment to work with Amazon's dynamic loading)
        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next"]/@href').extract_first()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield SeleniumRequest(url=next_page_url, callback=self.parse_category_page)

    def parse_product_details(self, response):
        # Extract detailed product information, including handling exceptions for missing information
        try:
            name = response.xpath('//span[@id="productTitle"]/text()').extract_first().strip()
        except AttributeError:
            name = 'N/A'
        
        try:
            price = response.xpath('//span[contains(@id, "priceblock_")]/text()').extract_first()
        except AttributeError:
            price = 'N/A'
        
        try:
            brand = response.xpath('//a[@id="bylineInfo"]/text()').extract_first()
        except AttributeError:
            brand = 'N/A'

        # Example for additional fields that require complex logic or might be missing
        materials, style, gender, sizes = self.extract_additional_details(response)

        yield {
            'name': name,
            'price': price,
            'brand': brand,
            'materials': materials,
            'style': style,
            'gender': gender,
            'sizes': sizes,
            'purchase_link': response.url,
            'img_link': response.xpath('//img[@id="landingImage"]/@src').extract_first(),
            # Additional field - Customer ratings
            'customer_ratings': self.extract_customer_ratings(response),
        }

    def extract_additional_details(self, response):
        # Placeholder for complex logic to extract materials, style, gender, sizes
        # Each of these would require custom logic and error handling
        return 'N/A', 'N/A', self.determine_gender(response), 'N/A'

    def determine_gender(self, response):
        # Improved gender determination logic
        product_description = " ".join(response.xpath('//div[@id="feature-bullets"]//text()').extract()).lower()
        if any(word in product_description for word in ['women', 'female', 'ladies']):
            return 'Female'
        elif any(word in product_description for word in ['men', 'male', 'gentlemen']):
            return 'Male'
        return 'Unisex'

    def extract_customer_ratings(self, response):
        # Extract customer ratings with error handling
        try:
            ratings = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract_first()
            return ratings
        except AttributeError:
            return 'No ratings'
