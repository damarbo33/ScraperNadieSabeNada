# ScraperNadieSabeNada
If you don't have internet connection and wanted to listen your favourite podcasts offline, this scraper helps you to automatize all the process and download all files for you.

It works for http://play.cadenaser.com/programa/nadie_sabe_nada/ but it can be adapted to download other podcasts of the same web modifying the following constants defined in scrapNadie.py:

DOMAIN = "http://play.cadenaser.com"

URL = DOMAIN + "/programa/nadie_sabe_nada"

DOWNLOAD_DIR = "C:/audio/"

You can specify in what page and entry start to scrap. For that, you can modify the variables: 

iniPage = 1

iniEntry = 0
