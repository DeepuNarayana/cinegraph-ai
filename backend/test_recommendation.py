from backend.db import run_query


query = """
MATCH
    (u:User {name: "Deepu"})
    -[:WATCHED]->
    (watched:Movie)
    -[:IN_GENRE]->
    (genre:Genre)

MATCH
    (recommended:Movie)
    -[:IN_GENRE]->
    (genre)

RETURN
    u.name AS user,
    watched.title AS watched_movie,
    genre.name AS shared_genre,
    recommended.title AS recommended_movie
ORDER BY recommended_movie
"""

result = run_query(query)

print("\n===== RECOMMENDATION PATH =====")

for row in result:
    print(row)