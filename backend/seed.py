from db import run_query


def seed():
    # Clear existing graph
    run_query("""
        MATCH (n)
        DETACH DELETE n
    """)

    # Create movies
    run_query("""
        CREATE
            (:Movie {
                id: 'm1',
                title: 'Interstellar',
                year: 2014
            }),
            (:Movie {
                id: 'm2',
                title: 'Inception',
                year: 2010
            }),
            (:Movie {
                id: 'm3',
                title: 'The Martian',
                year: 2015
            })
    """)

    # Create genres
    run_query("""
        CREATE
            (:Genre {name: 'Sci-Fi'}),
            (:Genre {name: 'Drama'}),
            (:Genre {name: 'Thriller'})
    """)

    # Create users
    run_query("""
        CREATE
            (:User {
                id: 'u1',
                name: 'Deepu'
            }),
            (:User {
                id: 'u2',
                name: 'Rahul'
            })
    """)

    # Create movie -> genre relationships
    run_query("""
        MATCH
            (interstellar:Movie {id: 'm1'}),
            (inception:Movie {id: 'm2'}),
            (martian:Movie {id: 'm3'}),
            (scifi:Genre {name: 'Sci-Fi'}),
            (drama:Genre {name: 'Drama'}),
            (thriller:Genre {name: 'Thriller'})

        CREATE
            (interstellar)-[:IN_GENRE]->(scifi),
            (interstellar)-[:IN_GENRE]->(drama),

            (inception)-[:IN_GENRE]->(scifi),
            (inception)-[:IN_GENRE]->(thriller),

            (martian)-[:IN_GENRE]->(scifi),
            (martian)-[:IN_GENRE]->(drama)
    """)

    # Create user -> movie relationships
    run_query("""
        MATCH
            (deepu:User {id: 'u1'}),
            (rahul:User {id: 'u2'}),
            (interstellar:Movie {id: 'm1'}),
            (inception:Movie {id: 'm2'}),
            (martian:Movie {id: 'm3'})

        CREATE
            (deepu)-[:WATCHED]->(interstellar),
            (deepu)-[:WATCHED]->(inception),

            (rahul)-[:WATCHED]->(inception)
    """)

    print("✅ CineGraph seed completed")


if __name__ == "__main__":
    seed()