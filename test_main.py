import pytest

from main import (
    Movie,
    get_movies_by_rating,
    get_top_10_certified_fresh_movies,
    parse_movie_list,
)


# --- Fixtures: reusable test data ---

@pytest.fixture
def sample_movies() -> list[Movie]:
    return [
        Movie(1, 10.0, 'Interstellar', True),
        Movie(2, 8.5, 'Fast and the Furious', False),
        Movie(3, 9.5, 'Sinners', True),
        Movie(4, 7.5, 'Inception', False),
        Movie(5, 9.0, 'The Matrix', True),
        Movie(6, 9.5, 'The Lord of the Rings: The Return of the King', True),
    ]


# --- Movie ---

def test_movie_accepts_valid_rating():
    movie = Movie(1, 10.0, 'Interstellar', True)
    assert movie.rating == 10.0


def test_movie_rejects_invalid_rating():
    with pytest.raises(ValueError):
        Movie(1, 11.0, 'Interstellar', True)


# --- parse_movie_list ---

def test_parse_movie_list_returns_list_of_movies():
    list_of_lists = [
        [1, 10.0, 'Interstellar', True],
        [2, 8.5, 'Fast and the Furious', True],
    ]
    movies = parse_movie_list(list_of_lists)
    assert len(movies) == 2
    assert movies[0] == Movie(1, 10.0, 'Interstellar', True)
    assert movies[1] == Movie(2, 8.5, 'Fast and the Furious', True)


def test_parse_movie_list_rejects_invalid_rating():
    list_of_lists = [
        [1, 10.0, 'Interstellar', True],
        [2, 15.5, 'Bad movie rating', True],
    ]
    movies = parse_movie_list(list_of_lists)
    assert len(movies) == 1
    assert movies[0] == Movie(1, 10.0, 'Interstellar', True)


# --- get_movies_by_rating ---

def test_get_movies_by_rating_filters_certified_fresh(sample_movies):
    fresh = get_movies_by_rating(sample_movies, certified_fresh=True, limit=10)
    assert all(m.certified_fresh for m in fresh)
    assert len(fresh) == 4
    assert Movie(2, 8.5, 'Fast and the Furious', False) not in fresh


def test_get_movies_by_rating_filters_certified_not_fresh(sample_movies):
    rotten = get_movies_by_rating(sample_movies, certified_fresh=False, limit=10)
    assert all(not m.certified_fresh for m in rotten)
    assert len(rotten) == 2
    assert Movie(1, 10.0, 'Interstellar', True) not in rotten
    assert rotten == [
        Movie(2, 8.5, 'Fast and the Furious', False),
        Movie(4, 7.5, 'Inception', False),
    ]


def test_get_movies_by_rating_sorts_by_rating_descending(sample_movies):
    result = get_movies_by_rating(sample_movies, limit=10)
    expected = [
        Movie(1, 10.0, 'Interstellar', True),
        Movie(3, 9.5, 'Sinners', True),
        Movie(6, 9.5, 'The Lord of the Rings: The Return of the King', True),
        Movie(5, 9.0, 'The Matrix', True),
        Movie(2, 8.5, 'Fast and the Furious', False),
        Movie(4, 7.5, 'Inception', False),
    ]
    assert result == expected


def test_get_movies_by_rating_breaks_ties_by_title(sample_movies):
    result = get_movies_by_rating(sample_movies, certified_fresh=True, limit=10)
    # Both have 9.5: 'Sinners' comes before 'The Lord of the Rings: The Return of the King'
    nine_ratings = [m for m in result if m.rating == 9.5]
    assert [m.movie_title for m in nine_ratings] == [
        'Sinners',
        'The Lord of the Rings: The Return of the King',
    ]


def test_get_movies_by_rating_respects_limit(sample_movies):
    result = get_movies_by_rating(sample_movies, certified_fresh=True, limit=2)
    assert len(result) == 2
    assert result[0] == Movie(1, 10.0, 'Interstellar', True)
    assert result[1] == Movie(3, 9.5, 'Sinners', True)


def test_get_movies_by_rating_returns_empty_when_no_matches():
    movies = [Movie(1, 8.0, 'Fast and the Furious', False)]
    result = get_movies_by_rating(movies, certified_fresh=True, limit=10)
    assert result == []


# --- get_top_10_certified_fresh_movies ---

def test_get_top_10_certified_fresh_movies_excludes_rotten(sample_movies):
    result = get_top_10_certified_fresh_movies(sample_movies)
    assert all(m.certified_fresh for m in result)
    assert Movie(2, 8.5, 'Fast and the Furious', False) not in result


def test_get_top_10_certified_fresh_movies_returns_at_most_10():
    many_fresh = [
        Movie(i, float(i % 10), f"Movie {i}", True)
        for i in range(1, 21)
    ]
    result = get_top_10_certified_fresh_movies(many_fresh)
    assert len(result) == 10


def test_get_top_10_certified_fresh_movies_with_fewer_than_10(sample_movies):
    result = get_top_10_certified_fresh_movies(sample_movies)
    assert len(result) == 4  # only 4 fresh movies in the fixture
