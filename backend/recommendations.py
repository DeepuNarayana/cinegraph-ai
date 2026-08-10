from db import run_query

def get_recommendations(user_name: str):

    # 1. Find movies already watched by the user
    watched_query = """
    MATCH (u:User {name: $user_name})-[:WATCHED]->(movie:Movie)
    RETURN movie.title AS movie
    """

    watched_result = run_query(
        watched_query,
        {"user_name": user_name},
    )

    watched_movies = {
        row["movie"]
        for row in watched_result
    }

    # 2. Find candidate movies through shared genres
    recommendation_query = """
    MATCH
        (u:User {name: $user_name})
        -[:WATCHED]->
        (watched:Movie)
        -[:IN_GENRE]->
        (genre:Genre)

    MATCH
        (recommended:Movie)
        -[:IN_GENRE]->
        (genre)

    RETURN
        recommended.title AS recommendation,
        collect(DISTINCT genre.name) AS matching_genres

    """

    candidates = run_query(
        recommendation_query,
        {"user_name": user_name},
    )

    # 3. Remove movies the user already watched
    recommendations = [
        {
            "recommendation": row["recommendation"],
            "matching_genres": row["matching_genres"],
            "match_count": len(row["matching_genres"]),
        }
        for row in candidates
        if row["recommendation"] not in watched_movies
    ]

    # 4. Rank by number of matching genres
    recommendations.sort(
        key=lambda item: item["match_count"],
        reverse=True,
    )

    return recommendations