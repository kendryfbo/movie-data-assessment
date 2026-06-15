from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# current list of lists of movies
movie_list = [
    [1, 9.0, 'Interstellar', True],
    [2, 8.5, 'Fast and the Furious', True],
]


@dataclass(frozen=True, slots=True)
class Movie:
    id: int
    rating: float
    movie_title: str
    certified_fresh: bool

    def __post_init__(self):
        if self.rating < 0.0 or self.rating > 10.0:
            raise ValueError(f"Rating must be between 0.0 and 10.0, got {self.rating}")


def parse_movie_list(movie_list: list[list]) -> list[Movie]:
    """Safely parses the old list of lists into a strongly typed list of Movie objects.

    Args:
        movie_list: The list of lists to parse.

    Returns:
        A list of Movie objects.
    """
    movies: list[Movie] = []
    for row in movie_list:
        try:
            movies.append(Movie(*row))
        except (TypeError, ValueError) as e:
            logger.error(f"Error parsing movie: {row}: {e}")
            continue
    return movies


def get_movies_by_rating(
    movies: list[Movie],
    certified_fresh: bool | None = None,
    limit: int = 10,
) -> list[Movie]:
    """Filters movies by freshness and sorts them by rating in descending order.

    Args:
        movies: The collection of Movie objects to process.
        certified_fresh: True for fresh only, False for rotten only, None for both.
        limit: The maximum number of top-rated movies to return.

    Returns:
        A list of the top-rated Movie objects, up to the specified limit.
    """
    if certified_fresh is not None:
        movies = [movie for movie in movies if movie.certified_fresh == certified_fresh]
    return sorted(movies, key=lambda x: (-x.rating, x.movie_title))[:limit]


def get_top_10_certified_fresh_movies(movies: list[Movie]) -> list[Movie]:
    """Gets the top 10 certified fresh movies.

    Args:
        movies: The collection of Movie objects to process.

    Returns:
        A list of the top 10 certified fresh Movie objects.
    """
    return get_movies_by_rating(movies, certified_fresh=True, limit=10)


if __name__ == '__main__':
    movies = parse_movie_list(movie_list)
    top_10_certified_fresh_movies = get_top_10_certified_fresh_movies(movies)
    print(top_10_certified_fresh_movies)
