import requests
from bs4 import BeautifulSoup


def get_movie_detail(movie_id):
    movie_id=str(movie_id)
    movie_details=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=277e998c81d1568adc13dac9f303a253&language=en-US'.format(movie_id))
    movie_details=movie_details.json()
    overview=movie_details['overview']
    img_url='https://image.tmdb.org/t/p/w500' + movie_details['poster_path']
    reviews=requests.get('https://api.themoviedb.org/3/movie/{}/reviews?api_key=277e998c81d1568adc13dac9f303a253&language=en-US'.format(movie_id))
    reviews=reviews.json()
    list_of_reviews=[]
    for review in reviews['results']:
        list_of_reviews.append(review['content'])
    return {"Overview":overview,"Reviews":list_of_reviews, "img": img_url}

def scrape_wikipedia(url):
    response=requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    p_tags = soup.find_all('p')
    wiki_data=''
    for p in p_tags:
        wiki_data=wiki_data+p.text
    return wiki_data


def search_wikipedia(name):
    """
    Searches Wikipedia for articles with the given name and returns the first
    matching article's title and URL.
    """
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": name,
        "srprop": "",
        "utf8": "",
        "formatversion": 2
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()
        article_title = data["query"]["search"][0]["title"]
        article_url = "https://en.wikipedia.org/wiki/" + article_title.replace(" ", "_")
        return article_title, article_url
    except:
        return None
    
    
# result = search_wikipedia("Avatar The Way of Water(2022)")
# html = scrape_wikipedia(result[1])