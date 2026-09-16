import json
from pathlib import Path

movies = [
    {"id": 1, "title": "Terminate", "year": 1989},
    {"id": 2, "title": "Kindergarten Cop", "year": 1993}
]


data = json.dumps(movies)
print(data)
Path("movies.json").write_text(data)


data = Path("movies.json").read_text()
movies = json.loads(data)
print(movies)
