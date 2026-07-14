import csv

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://moviesda33.com"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

static_files = [
    ("movies-2012", "/tamil-2012-movies/?page={}"),
    ("movies-2015", "/tamil-2015-movies/?page={}"),
    ("movies-2016", "/tamil-2016-movies/?page={}"),
    ("movies-2017", "/tamil-2017-movies/?page={}"),
    ("movies-2018", "/tamil-2018-movies/?page={}"),
    ("movies-2019", "/tamil-2019-movies/?page={}"),
    ("movies-2020", "/tamil-2020-movies/?page={}"),
    ("movies-2021", "/tamil-2021-movies/?page={}"),
    ("movies-2022", "/tamil-2022-movies/?page={}"),
    ("movies-2023", "/tamil-2023-movies/?page={}"),
    ("movies-2024", "/tamil-2024-movies/?page={}"),
    ("movies-2025", "/tamil-2025-movies/?page={}"),
]

dynamic_files = [
    ("hd-movies", "/tamil-hd-movies/?page={}"),
    ("movies-2026", "/tamil-2026-movies/?page={}"),
]

collection_base = "/tamil-movies-collection/?page={}"


def get_total_pages(href):
    href = (BASE_URL + href) if (BASE_URL not in href) else href

    print(f"Getting total pages count for {href}")

    try:
        response = requests.get(href.format(1), headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        total_pages = int(soup.select_one("#totalPages").get_text(strip=True))

        print(f"Found {total_pages} pages.")
        return total_pages

    except Exception as e:
        print(f"Failed to determine total pages: {e}", "Defaulting to 1")
        return 1


def get_all_files(href, filename, filemode="w"):
    href = (BASE_URL + href) if (BASE_URL not in href) else href

    with open(filename + ".csv", filemode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for page in range(get_total_pages(href), 0, -1):
            url = href.format(page)
            print(f"Scraping page {page}: {url}")

            try:
                response = requests.get(url, headers=headers, timeout=20)
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to fetch page {page}: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            movies = soup.select("div.f, div.folder")

            for movie in movies[::-1]:
                a = movie.select_one("a")
                if not a:
                    continue

                name = movie.get_text(" ", strip=True).replace(",", " ")
                link = a.get("href", "").strip()

                if name and link:
                    writer.writerow([name, link])
                    print(f"  -> {name}")

    print(f"Done! {href} Saved to {filename}")


def index_files(list_of_file_sources):
    for filename, href in list_of_file_sources:
        get_all_files(href, filename)


def index_collection(href, filename="collections"):
    print(f"Start indexing collection: {href=} {filename=}")

    href = (BASE_URL + href) if (BASE_URL not in href) else href

    total_pages = get_total_pages(href)

    for page in range(total_pages):
        url = href.format(page + 1)

        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        actors = soup.select("div.f, div.folder")

        for actor in actors:
            print("\n\n--------------------------------------------")
            print("Collecting for actor", actor)

            a = actor.select_one("a")
            if not a:
                continue

            link = a.get("href", "").strip()

            if not link:
                continue

            get_all_files(link, filename, "a")


index_static_files = lambda: index_files(static_files)
index_dynamic_files = lambda: index_files(dynamic_files)


if __name__ == "__main__":
    # index_static_files()
    index_dynamic_files()
    # index_collection(collection_base)
    pass
