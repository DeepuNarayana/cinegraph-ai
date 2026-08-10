# from db import verify_connection


# if __name__ == "__main__":
#     verify_connection()
#     print("✅ CognoDB connection successful")

# from db import run_query


# query = """
# MATCH
#     (u:User {name: $user_name})
#     -[:WATCHED]->
#     (watched:Movie)
#     -[:IN_GENRE]->
#     (genre:Genre)
#     <-[:IN_GENRE]-
#     (recommended:Movie)

# WHERE NOT (u)-[:WATCHED]->(recommended)

# RETURN DISTINCT
#     watched.title AS watched_movie,
#     genre.name AS genre,
#     recommended.title AS recommendation
# """

# result = run_query(
#     query,
#     {"user_name": "Deepu"},
# )

# print(result)
#Watched
from db import run_query

# print(
#     run_query("""
#         MATCH (u:User {name: "Deepu"})-[:WATCHED]->(m:Movie)
#         RETURN u.name AS user, m.title AS movie
#     """)
# )

#In genere
# print(
#     run_query("""
#         MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
#         RETURN m.title AS movie, g.name AS genre
#     """)
# )
# Without Where

# print(
#     run_query("""
#         MATCH
#             (u:User {name: "Deepu"})
#             -[:WATCHED]->
#             (watched:Movie)
#             -[:IN_GENRE]->
#             (genre:Genre)
#             <-[:IN_GENRE]-
#             (recommended:Movie)

#         RETURN
#             u.name AS user,
#             watched.title AS watched_movie,
#             genre.name AS genre,
#             recommended.title AS recommendation
#     """)
# )

print(
    run_query("""
        MATCH
            (u:User {name: "Deepu"})
            -[:WATCHED]->
            (watched:Movie)
            -[:IN_GENRE]->
            (genre:Genre)
            <-[:IN_GENRE]-
            (recommended:Movie)

        RETURN
            watched.title AS watched_movie,
            genre.name AS genre,
            recommended.title AS recommendation,
            (u)-[:WATCHED]->(recommended) AS already_watched
    """)
)