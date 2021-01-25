BOT_NAME = 'putereaplantelo'
SPIDER_MODULES = ['putereaplantelo.spiders']
NEWSPIDER_MODULE = 'putereaplantelo.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'putereaplantelo.pipelines.DatabasePipeline': 300,
}