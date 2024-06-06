import requests
from bs4 import BeautifulSoup
import pandas as pd

list_of_movies = []
list_of_url = []
for i in range(1,51):
    url = "https://www.themoviedb.org/movie?page="
    url = url+str(i)
    list_of_url.append(url)

for j in list_of_url:
    response = requests.get(j).text
    soup_data = BeautifulSoup(response,'lxml')
    first_div = soup_data.find('div',class_='page_wrapper')
    div = first_div.find_all('div',class_='card style_1')
    for k in div:
        div_content = k.find('div',class_='content')
        Movie_name = div_content.find('h2').text
     
        release_date = div_content.find('p').text
        
        Rate = div_content.find('div',class_='user_score_chart')
        Rating = Rate['data-percent']
    
        url_ = div_content.find('a')
        # print(url_)
        urls = j
        final_url = urls.replace('/movie',url_['href'])
        
        response2 = requests.get(final_url).text
        soup_data2 = BeautifulSoup(response2,'lxml')

        content_web = soup_data2.find('div',class_='header large border first')

        inside_content_web = content_web.find('div',class_='facts')

        genre = inside_content_web.find('span',class_='genres').text.strip().replace('\xa0',' ')

        if inside_content_web.find('span',class_='runtime') == None:
            runtime = 'Not found'
        else:
            runtime = inside_content_web.find('span',class_='runtime').text.strip()
            # print(runtime)

        dir_cont = content_web.find('div',class_='header_info')

        li_character = dir_cont.find_all('li',class_='profile')
        # print(li_character)
        director=set()
        for i in range(0,len(li_character)):
            if 'Director' in li_character[i].find('p',class_="character").text:
                direct = li_character[i].find('a').text
                director.add(direct)
        director = list(director)
    
        str_director=''
        for i in range(0,len(director)):
            str_director+= director[i]+','
        
        if str_director.endswith(',') == True:
            director = str_director[:-1]

        overview = soup_data2.find('div',class_="overview").text.strip()
    
        movie_data = {
            'Release date':release_date,
            'Movie':Movie_name,
            'Director': director,
            'Genre' : genre,
            'Runtime':runtime,
            'Rating':Rating,
            'Overview':overview
        }

        list_of_movies.append(movie_data)
        
df = pd.DataFrame(list_of_movies)
df.to_excel('movies.xlsx')