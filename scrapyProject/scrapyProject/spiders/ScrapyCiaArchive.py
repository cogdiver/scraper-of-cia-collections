import scrapy

class ScrapyCiaArchive(scrapy.Spider):
  name = 'archives'
  start_urls = ['https://www.cia.gov/readingroom/special-collections-archive']
  custom_settings = {
    'FEED_URI': 'archives.json',
    'FEED_FORMAT': 'json',
    'FEED_EXPORT_ENCODING': 'utf-8'
  }

  def parse(self, response):
    links_archives = response.xpath('//a[starts-with(@href, "/readingroom/collection") and (parent::h2)]/@href').getall()
    for archive in links_archives:
      yield response.follow(archive, callback=self.parse_archive, cb_kwatgs={'url': response.urljoin(archive)})

  def parse_archive(self, response, **kwargs):
    link = kwargs['url']
    title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
    try:
      paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()
    except:
      paragraph = ''

    yield {
        'url': link,
        'title': title,
        'body': paragraph
    }