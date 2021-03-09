from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('kpi_ua')
    process.crawl('rozetka')
    process.start()


def task1():
    print("Task #1")

    root = etree.parse("task1.xml")
    pages = root.xpath("//page")

    max_texts_count = 0
    for page in pages:
        count_texts = page.xpath("count(fragment[@type='text'])")
        max_texts_count = count_texts if count_texts > max_texts_count else max_texts_count

    print("Max text elements: %d" % max_texts_count)


def task2():
    print("Task #2")

    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")

    print("XHTML page will be opened in web-browser...")
    webbrowser.get('safari').open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    print("Cleanup..", end="", flush=True)
    cleanup()
    print("Scrapping data..", end="", flush=True)
    scrap_data()
    print("Ready!")
    while True:
        print("*" * 50)
        print("Select task:")
        print("1. Task #1")
        print("2. Task #2")
        print("> ", end="", flush=True)
        number = input()
        if number == "1":
            task1()
        elif number == "2":
            task2()
        else:
            break
    print("Exit")
