import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from utils import read_json, write_json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_EXTENSIONS = read_json(os.path.join(CURRENT_DIR, "font_extensions.json"))

EXTENSION_RESOURCE_MAP = {
    ".css": "stylesheet",
    "rss.xml": "rss_feed",
    ".js": "script",
    ".png": "icon",
}


def get_page(url):
    try:
        return requests.get(url)

    except requests.exceptions.MissingSchema:
        return requests.get(f"https://{url}")


def is_external_resource(tag, url):
    path = tag.get("src", tag.get("href"))
    tag_domain = urlparse(path).netloc
    url_domain = urlparse(url).netloc

    if tag_domain and tag_domain != url_domain and tag.name != "a":
        return True

    return False


def guess_resource_type(path):
    path = path.lower()

    for ext, res_type in EXTENSION_RESOURCE_MAP.items():
        if path.endswith(ext):
            return res_type

    if any([path.endswith(ext) for ext in FONT_EXTENSIONS]) or "font" in path:
        return "font"

    return "link"


def extract_text_from_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    non_visible_tags = [
        "[document]",
        "html",
        "noscript",
        "header",
        "input",
        "script",
        "meta",
        "head",
    ]

    text = [
        tag.text for tag in soup.find_all() if tag.name not in non_visible_tags
    ]

    return " ".join(text)


def generate_word_freq_dict(text):
    escape_chars = [chr(char) for char in range(1, 32)]
    text = text.translate({ord(ec): " " for ec in escape_chars}).lower()
    word_list = re.findall(r"\b[^\d\W]+\b", text)

    return Counter(word_list)


def add_domain_if_required(address, source_url):
    address_domain = urlparse(address).netloc
    if not address_domain and not urlparse(f"https://{address}").netloc:
        source_domain = urlparse(source_url).netloc

        if not source_domain:
            source_domain = urlparse(f"https://{source_url}").netloc

        slash = "" if address[0] == "/" else "/"

        return f"{source_domain}{slash}{address}"

    return address


def run(url, output_dir=CURRENT_DIR):
    if not os.path.isdir(output_dir):
        raise FileNotFoundError(f"{output_dir} is not a valid directory")

    page = get_page(url)

    soup = BeautifulSoup(page.content, "html.parser")
    all_elems = soup.find_all()

    external_resources = [
        elem for elem in all_elems if is_external_resource(elem, url)
    ]

    output = defaultdict(list)
    for er in external_resources:
        path = er.get("src", er.get("href"))

        if er.name == "link":
            output[guess_resource_type(path)].append(path)

        else:
            output[er.name].append(path)

    if output:
        er_path = os.path.join(output_dir, "external_resources.json")
        write_json(output, er_path)

    pp_href = list(
        set(
            add_domain_if_required(elem["href"], url)
            for elem in soup.find_all("a")
            if "privacypolicy" in elem.text.lower().replace(" ", "")
        )
    )

    if not pp_href:
        print(f"No privacy policy page found @ {url}")
        return

    if len(pp_href) > 1:
        while True:
            options_str = "\n  ".join(
                [f"{i + 1}: {link}" for i, link in enumerate(pp_href)]
            )
            option = input(
                "Please select which page to scrape:\n  "
                + options_str
                + "\nOption: "
            )

            try:
                option = int(option)
                if option - 1 in range(len(pp_href)):
                    target_url = pp_href[option - 1]
                    break

            except ValueError:
                print(f"Invalid option {option}, please select again.")
                pass

    else:
        target_url = pp_href[0]

    pp_page = get_page(target_url)
    text = extract_text_from_page(pp_page)

    word_freq = generate_word_freq_dict(text)

    write_json(
        word_freq,
        os.path.join(CURRENT_DIR, "privacy_policy_word_frequency.json"),
    )


if __name__ == "__main__":
    args = sys.argv[1:]

    run(*args)
