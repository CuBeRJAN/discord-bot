import sys
from youtube_search import YoutubeSearch

def search_yt(terms):
    results = YoutubeSearch(terms, max_results=1).to_dict()
    print(results)
    return "https://youtube.com" + results[0]["url_suffix"]

print(search_yt(" ".join(sys.argv[1:])))
