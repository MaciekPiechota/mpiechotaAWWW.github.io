import requests 

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def get_html_doc(url):
    r = requests.get(url)
    return r.text

def scrape_languages():
    html_doc = get_html_doc('https://www.tiobe.com/tiobe-index/')

    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.find("table", class_="table table-striped", id="VLTH")

    languages = []

    for row in table.find_all("tr")[1:6]:
        columns = row.find_all("td")
        languages.append(columns[0].text.strip())

    return languages

def get_languages_informations(languages):
    langs_info = dict()
    for language in languages:


        query = f"{language} Wikipedia"
        results = DDGS().text(query)
        wiki_url = next(results)["href"]

        wiki_html_doc = get_html_doc(wiki_url)

        soup = BeautifulSoup(wiki_html_doc, "html.parser")
        paragraphs = soup.select("p")

        langs_info[language] = {
            "lang": language,
            "website": wiki_url,
            "paragraphs": []
        }


        for i in range(1, min(len(paragraphs), 5)):
            langs_info[language]["paragraphs"].append(
                paragraphs[i].get_text())

    return langs_info

def save_as_markdown(langs_info):
    markdown_text = f"# Popular Programing Languages :computer: \n\n"
    for key, lang_info in langs_info.items():
        markdown_text += f"## {key}\n\n"
        markdown_text += f"### **[original website]({lang_info['website']})**\n\n"
        for paragraph in lang_info["paragraphs"]:
            markdown_text += f"{paragraph} \n\n"

    with open("popular_languages.md", 'w') as file:
        file.write(markdown_text)


if __name__ == "__main__":
    languages = scrape_languages()

    langs_info = get_languages_informations(languages)

    save_as_markdown(langs_info)



