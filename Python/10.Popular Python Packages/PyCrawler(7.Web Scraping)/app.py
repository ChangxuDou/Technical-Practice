# Stack Overflow returns a Cloudflare challenge page (HTTP 403)
# instead of the question list when accessed through requests.
# For this exercise, we parse a local HTML snapshot copied from
# the browser to practice extracting data with BeautifulSoup.
# The snapshot does not update automatically.

import requests
from bs4 import BeautifulSoup
from pathlib import Path

file = Path(__file__).parent / "questions.html"

soup = BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")

questions = soup.select(".s-post-summary.js-post-summary")
for question in questions:
    print(question.select_one(".s-link").get_text())
