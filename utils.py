import requests


def get_movie_detail(movie_id):
    movie_id=str(movie_id)
    movie_details=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=277e998c81d1568adc13dac9f303a253&language=en-US'.format(movie_id))
    movie_details=movie_details.json()
    overview=movie_details['overview']
    reviews=requests.get('https://api.themoviedb.org/3/movie/{}/reviews?api_key=277e998c81d1568adc13dac9f303a253&language=en-US'.format(movie_id))
    reviews=reviews.json()
    list_of_reviews=[]
    for review in reviews['results']:
        list_of_reviews.append(review['content'])

get_movie_detail(640146)

