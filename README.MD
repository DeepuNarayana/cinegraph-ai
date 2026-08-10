CineGraph AI

Graph-powered movie recommendation application built with React,FastAPI, and CognoDB.

CineGraph AI recommends movies for a user by traversing relationships ina graph. It looks at movies the user has already watched, finds theirshared genres, discovers other movies connected to those genres,excludes movies the user has already watched, and ranks the remainingcandidates by the number of matching genres.

Features

User-based movie recommendations
Graph-based multi-hop recommendation logic
CognoDB graph database
Parameterized Cypher queries
FastAPI REST API
React frontend
Dynamic username input
Excludes already-watched movies
Ranks recommendations by matching genre count
Seed script for reproducible sample data
Use Case

The application demonstrates how graph relationships can be used todiscover relevant movie recommendations.

User
  |
  | WATCHED
  v
Movie
  |
  | IN_GENRE
  v
Genre
  ^
  | IN_GENRE
  |
Movie Candidate

For a user such as Deepu, the system finds the genres associated withmovies they have watched and uses those relationships to discover candidate movies.

Why a Graph Database?

The core problem is relationship discovery.

A recommendation requires traversing several connected entities:

User -> WATCHED -> Movie -> IN_GENRE -> Genre
                                      ^
                                      |
                              IN_GENRE |
                                      |
                                Movie Candidate

A graph database represents these relationships directly. This makesmulti-hop traversal natural and keeps the recommendation logic focusedon the connections between users, movies, and genres.

Architecture
+-------------------------+
|       React UI          |
|      CineGraph AI       |
+------------+------------+
             |
             | HTTP
             v
+-------------------------+
|        FastAPI          |
|        REST API         |
+------------+------------+
             |
             v
+-------------------------+
| Recommendation Service  |
|   recommendations.py   |
+------------+------------+
             |
             | Cypher
             v
+-------------------------+
|        CognoDB          |
|     Graph Database      |
+-------------------------+

Graph Data Model

+-------------+        WATCHED        +-------------+
|    User     | --------------------> |    Movie    |
|-------------|                       |-------------|
| id          |                       | id          |
| name        |                       | title       |
|             |                       | year        |
+-------------+                       +------+------+
                                             |
                                             | IN_GENRE
                                             v
                                      +-------------+
                                      |    Genre    |
                                      |-------------|
                                      | name        |
                                      +------+------+
                                             ^
                                             |
                                             | IN_GENRE
                                             |
                                      +-------------+
                                      |    Movie    |
                                      |  Candidate  |
                                      +-------------+

Main entities
User
Movie
Genre
Main relationships
WATCHED: User -> Movie
IN_GENRE: Movie -> Genre

Recommendation Logic

The recommendation query performs a multi-hop graph traversal:

Find the requested user.

Find movies watched by that user.

Traverse from watched movies to their genres.

Find other movies connected to those genres.

Exclude movies already watched by the user.

Group candidates by movie.

Collect matching genres.

Count matching genres.

Sort by match count in descending order.

The core Cypher pattern is:

MATCH
(u:User {name: $user_name})
-[:WATCHED]->
(watched:Movie)
-[:IN_GENRE]->
(genre:Genre)
<-[:IN_GENRE]-
(recommended:Movie)

WHERE NOT (u)-[:WATCHED]->(recommended)

RETURN
    recommended.title AS recommendation,
    collect(DISTINCT genre.name) AS matching_genres,
    count(DISTINCT genre) AS match_count

ORDER BY match_count DESC

The user name is supplied as a Cypher parameter rather than concatenatedinto the query.

Example

For Deepu, the application returns:

{
  "user": "Deepu",
  "recommendations": [
    {
      "recommendation": "The Martian",
      "matching_genres": [
        "Sci-Fi",
        "Drama"
      ],
      "match_count": 2
    }
  ]
}

For Rahul, the sample graph produces recommendations includingInterstellar and The Martian.

Project Structure

CineGraph AI/
|
+-- backend/
|   +-- __init__.py
|   +-- db.py
|   +-- main.py
|   +-- recommendations.py
|   +-- seed.py
|   +-- test_db.py
|   +-- test_recommendation.py
|
+-- frontend/
|   +-- src/
|   |   +-- components/
|   |   +-- services/
|   |   +-- App.jsx
|   |   +-- App.css
|   |   +-- index.css
|   |   +-- main.jsx
|   +-- public/
|   +-- package.json
|   +-- package-lock.json
|   +-- vite.config.js
|
+-- requirements.txt
+-- .gitignore
+-- README.md

Prerequisites

Python 3.10+

Node.js and npm

A CognoDB instance

CognoDB connection credentials

CognoDB Setup

Create or use a CognoDB graph database and obtain the connection detailsrequired by the application.

Configure the backend through environment variables.

Create a .env file in the project root:

COGNODB_URI=your_cognodb_uri
COGNODB_USER=your_cognodb_user
COGNODB_PASSWORD=your_cognodb_password
COGNODB_DATABASE=neo4j

Install dependencies

pip install -r requirements.txt

Seed the graph

python -m backend.seed

The seed script creates the sample users, movies, genres, andrelationships required by the application.

Start FastAPI

uvicorn backend.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Vite will display the local frontend URL in the terminal.

API

Health/root endpoint

GET /

Recommendations

GET /recommendations/{user_name}

Example:

GET /recommendations/Deepu

Example response:

{
  "user": "Deepu",
  "recommendations": [
    {
      "recommendation": "The Martian",
      "matching_genres": [
        "Sci-Fi",
        "Drama"
      ],
      "match_count": 2
    }
  ]
}

Seed Data

The seed script creates sample data for:

Users

Deepu

Rahul

Movies

Interstellar

Inception

The Martian

Genres

Sci-Fi

Drama

Thriller

The script also creates WATCHED and IN_GENRE relationships.

Database Access Layer

backend/db.py is responsible for:

Loading database configuration from environment variables

Creating the CognoDB driver

Verifying connectivity

Executing parameterized Cypher queries

Closing the driver

The application does not hard-code database credentials.

Error Handling

The database layer validates required configuration such as the CognoDBURI and password before creating the driver.

Database connectivity is isolated in the database access layer so thatAPI and recommendation logic do not directly manage connection details.

Screenshots

Application UI

Add the final CineGraph AI UI screenshot here.

docs/screenshots/cinegraph-ui.png

API

Add the Swagger/API response screenshot here.

docs/screenshots/swagger-response.png

Graph

Add the CognoDB graph/query screenshot here.

docs/screenshots/cognodb-graph.png

Demo

Live application:

TODO: Add hosted application URL

Screen recording:

TODO: Add screen recording URL
