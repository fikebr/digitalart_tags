# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://www.pythonforbeginners.com/beautifulsoup/python-beautifulsoup-basic

from bs4 import BeautifulSoup


def metadata_from_log(html, imgfile):
    soup = BeautifulSoup(html, "html.parser")
    id = imgfile.replace(".", "_")

    d = soup.find("div", attrs={"id": id})

    metadata_tables = d.find_all("table", class_="metadata")

    result = {}

    for table in metadata_tables:
        labels = [label.text for label in table.find_all("td", class_="label")]
        values = [value.text for value in table.find_all("td", class_="value")]
        metadata = dict(zip(labels, values))
        result.update(metadata)

    return(result)