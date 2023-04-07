from pornhub_api import PornhubApi
import random
import sys

api = PornhubApi()

def category_list():
    print("Available categories:")
    cats = []
    for category in api.video.categories().categories:
        cats.append(category.category)
    print("```", ", ".join(cats), "```")

def random_category():
    return random.choice(api.video.categories().categories)

def get_category_by_name(name):
    categories = api.video.categories().categories
    for category in categories:
        if str(category.category) == str(name):
            return category

def by_category_name(category_n):
    category = get_category_by_name(category_n)
    if not category:
        print("Category not found!")
        return
    result = api.search.search_videos(
        ordering="mostviewed",
        category=category
    )
    i = random.randint(0, result.size())
    print(f"{result[i].title}\n\n{result[i].url}")
    

if sys.argv[1] == "list":
    category_list()
elif sys.argv[1] == "category":
    by_category_name(sys.argv[2])
