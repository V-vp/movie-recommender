from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
import json
import requests
import urllib.request
from django.http import JsonResponse
from _collections import OrderedDict
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm
from .models import MovieInfo
from django.contrib.auth.models import Permission, User

rating_user = settings.CSV
cs1 = settings.CSV2

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'recommender/login.html')
    albums = MovieInfo.objects.filter(user=request.user)
    query = request.GET.get("q")
    if query:
        albums = albums.filter(
            Q(movie_name__icontains=query)
        ).distinct()
        return render(request, 'recommender/home1.html', {
            'albums': albums,
        })
    else:
        albums = MovieInfo.objects.filter(user=request.user).values('imdb','awards','user_rating','pk','movie_name','star1','star2','star3','star4','star5','movie_earn','movie_rating','movie_plot','movie_poster','movie_year','movie_director','movie_runtime','movie_stars').distinct()
        #print(albums)
        if albums:
            rating_info = MovieInfo.objects.filter(user=request.user).values('user_rating','imdb').distinct()
            rates = []
            print(rating_info)
            checking_list = []
            for i in rating_info:
                    checking_list.append(i['imdb'])

            for i in rating_info:
                if i['user_rating']!=0:
                    rates.append([i['user_rating'],i['imdb']])
            rates.sort(reverse=True)
            moive_list =[]
            for i in rates:
                moive_list.append(i[1])

            ratings_df = pd.read_csv(rating_user, header=None,
                                     names=['user_id', 'movie_title', 'movie_id', 'rating', 'imdb_id', 'tmdb_id'])

            ratings_mtx_df = ratings_df.pivot_table(values='rating', index='user_id', columns='imdb_id')
            ratings_mtx_df.fillna(0, inplace=True)

            movie_index = ratings_mtx_df.columns

            corr_matrix = np.corrcoef(ratings_mtx_df.T)

            def get_movie_similarity(movie_title):
                movie_idx = list(movie_index).index(movie_title)
                return corr_matrix[movie_idx]

            def get_movie_recommendations(user_movies):
                movie_similarities = np.zeros(corr_matrix.shape[0])
                for movie_id in user_movies:
                    movie_similarities = movie_similarities + get_movie_similarity(movie_id)
                similarities_df = pd.DataFrame({
                    'imdb_id': movie_index,
                    'sum_similarity': movie_similarities
                })
                similarities_df = similarities_df[~(similarities_df.imdb_id.isin(user_movies))]
                similarities_df = similarities_df.sort_values(by=['sum_similarity'], ascending=False)
                return similarities_df


            sample_user_movies = moive_list
            # print(sample_user_movies)
            recommendations = get_movie_recommendations(sample_user_movies)
            name = int(recommendations.imdb_id.head(1).tolist()[0])

            imdb_id = str(format(name, "07"))
            movie_1 = requests.get(url='http://www.omdbapi.com/?i=tt' + imdb_id + '&apikey=adfd045f')
            jsonvalue1 = movie_1.json()
            movie_info_1 = jsonvalue1
            movie_list_1 = {'movie1_imdb':name, 'movie1_awards': movie_info_1['Awards'],
                            'movie1_name': movie_info_1['Title'], 'movie1_year': movie_info_1['Year'],
                            'movie1_director': movie_info_1['Director'], 'movie1_rating': movie_info_1['imdbRating'],
                            'movie1_stars': movie_info_1['Actors'], 'movie1_plot': movie_info_1['Plot'],
                            'movie1_runtime': movie_info_1['Runtime'], 'movie1_box': movie_info_1['BoxOffice'],
                            'movie1_poster': movie_info_1['Poster']}

            print(checking_list)
            print(movie_list_1['movie1_imdb'])
            if movie_list_1['movie1_imdb'] in checking_list :
                pass
            else:
                pk = request.user.pk
                user = User.objects.get(pk=pk)
                info = MovieInfo()
                info.user = user
                info.movie_name = movie_list_1['movie1_name']
                info.awards = movie_list_1['movie1_awards']
                info.imdb = movie_list_1['movie1_imdb']
                info.movie_year = movie_list_1['movie1_year']
                info.movie_director = movie_list_1['movie1_director']
                info.movie_rating = movie_list_1['movie1_rating']
                info.movie_stars = movie_list_1['movie1_stars']
                info.movie_plot = movie_list_1['movie1_plot']
                info.movie_runtime = movie_list_1['movie1_runtime']
                info.movie_earn = movie_list_1['movie1_box']
                info.movie_poster = movie_list_1['movie1_poster']
                info.save()

                albums = MovieInfo.objects.filter(user=request.user).values('imdb', 'awards', 'user_rating', 'pk',
                                                                        'movie_name', 'movie_earn', 'movie_rating',
                                                                        'movie_plot', 'movie_poster', 'movie_year',
                                                                        'movie_director', 'movie_runtime',
                                                                        'movie_stars','star1','star2','star3','star4','star5').distinct()

            return render(request, 'recommender/home1.html', {
                    'albums': albums,'rating_info':rating_info,'rates':rates
                })
        return render(request, 'recommender/home.html')

def recommend(request):
    if not request.user.is_authenticated:
        return render(request, 'recommender/login.html')
    else:
        animation = int(request.POST['animation'])
        action = int(request.POST['action'])
        adventure = int(request.POST['adventure'])
        children = int(request.POST['children'])
        comedy = int(request.POST['comedy'])
        crime = int(request.POST['crime'])
        documentary = int(request.POST['documentary'])
        drama = int(request.POST['drama'])
        Fantasy = int(request.POST['Fantasy'])
        Mystery = int(request.POST['Mystery'])
        Horror = int(request.POST['Horror'])
        Romance = int(request.POST['Romance'])
        Sci_Fi = int(request.POST['Sci_Fi'])
        Thriller = int(request.POST['Thriller'])
        War = int(request.POST['War'])
        Western = int(request.POST['Western'])

        df = pd.read_csv(cs1, names=['movie_id', 'movie_title', 'movie_genre', 'imdb_id', 'tmdb_id'])
        x = np.array(df)

        df = pd.concat([df, df.movie_genre.str.get_dummies(sep='|')], axis=1)
        movie_categories = df.columns[3:]
        movie_categories = movie_categories[3:]

        user_preferences = OrderedDict(zip(movie_categories, []))

        user_preferences['Action'] = action
        user_preferences['Adventure'] = adventure
        user_preferences['Animation'] = animation
        user_preferences["Children"] = children
        user_preferences["Comedy"] = comedy
        user_preferences['Crime'] = crime
        user_preferences['Documentary'] = documentary
        user_preferences['Drama'] = drama
        user_preferences['Fantasy'] = Fantasy
        user_preferences['Film-Noir'] = 0
        user_preferences['Horror'] = Horror
        user_preferences['IMAX'] = 0
        user_preferences['Musical'] = 0
        user_preferences['Mystery'] = Mystery
        user_preferences['Romance'] = Romance
        user_preferences['Sci-Fi'] = Sci_Fi
        user_preferences['Thriller'] = Thriller
        user_preferences['War'] = War
        user_preferences['Western'] = Western

        def dot_product(v1, v2):
            return sum([i * j for i, j in zip(v1, v2)])

        def get_movie_score(movie_features, user_preferences):
            return dot_product(movie_features, user_preferences)

        a = df[movie_categories].apply(get_movie_score, args=([user_preferences.values()]), axis=1)

        def recommendations(user_preferences, n_recommendations):
            df['score'] = df[movie_categories].apply(get_movie_score, args=([user_preferences.values()]), axis=1)
            return df.sort_values(by=['score'], ascending=False)['imdb_id'][:n_recommendations]

        a = recommendations(user_preferences, 3)
        a = np.array(a)
        a1 = str(format(a[0], "07"))
        a2 = str(format(a[1], "07"))
        a3 = str(format(a[2], "07"))

        movie_1 = requests.get(url='http://www.omdbapi.com/?i=tt' + a1 + '&apikey=adfd045f')
        movie_2 = requests.get(url='http://www.omdbapi.com/?i=tt' + a2 + '&apikey=adfd045f')
        movie_3 = requests.get(url='http://www.omdbapi.com/?i=tt' + a3 + '&apikey=adfd045f')

        # r = requests.get(url='http://theapache64.xyz:8080/movie_db/search?keyword=',params='tonystark')

        jsonvalue1 = movie_1.json()
        movie_info_1 = jsonvalue1
        jsonvalue2 = movie_2.json()
        movie_info_2 = jsonvalue2
        jsonvalue3 = movie_3.json()

        movie_info_3 = jsonvalue3

        movie_list_1 = {'movie1_imdb':a[0],'movie1_awards': movie_info_1['Awards'],'movie1_name': movie_info_1['Title'], 'movie1_year': movie_info_1['Year'],
                        'movie1_director': movie_info_1['Director'], 'movie1_rating': movie_info_1['imdbRating'],
                        'movie1_stars': movie_info_1['Actors'], 'movie1_plot': movie_info_1['Plot'],
                        'movie1_runtime': movie_info_1['Runtime'], 'movie1_box': movie_info_1['BoxOffice'],'movie1_poster': movie_info_1['Poster']}

        movie_list_2 = {'movie2_imdb':a[1],'movie2_awards': movie_info_2['Awards'],'movie2_name': movie_info_2['Title'], 'movie2_year': movie_info_2['Year'],
                        'movie2_director': movie_info_2['Director'],
                        'movie2_rating': movie_info_2['imdbRating'], 'movie2_stars': movie_info_2['Actors'],
                        'movie2_plot': movie_info_2['Plot'], 'movie2_runtime': movie_info_2['Runtime'],
                        'movie2_box': movie_info_2['BoxOffice'],'movie2_poster': movie_info_2['Poster']}

        movie_list_3 = {'movie3_imdb':a[2],'movie3_awards': movie_info_3['Awards'],'movie3_name': movie_info_3['Title'], 'movie3_year': movie_info_3['Year'],
                        'movie3_director': movie_info_3['Director'],
                        'movie3_rating': movie_info_3['imdbRating'], 'movie3_stars': movie_info_3['Actors'],
                        'movie3_plot': movie_info_3['Plot'], 'movie3_runtime': movie_info_3['Runtime'],
                        'movie3_box': movie_info_3['BoxOffice'],'movie3_poster': movie_info_3['Poster']}



        pk = request.user.pk
        user = User.objects.get(pk=pk)
        info = MovieInfo()
        info.user = user
        info.movie_name = movie_list_1['movie1_name']
        info.awards = movie_list_1['movie1_awards']
        info.imdb = movie_list_1['movie1_imdb']
        info.movie_year = movie_list_1['movie1_year']
        info.movie_director = movie_list_1['movie1_director']
        info.movie_rating = movie_list_1['movie1_rating']
        info.movie_stars = movie_list_1['movie1_stars']
        info.movie_plot = movie_list_1['movie1_plot']
        info.movie_runtime = movie_list_1['movie1_runtime']
        info.movie_earn = movie_list_1['movie1_box']
        info.movie_poster = movie_list_1['movie1_poster']
        info.save()

        info1 = MovieInfo()
        info1.user = user
        info1.movie_name = movie_list_2['movie2_name']
        info1.movie_year = movie_list_2['movie2_year']
        info1.awards = movie_list_2['movie2_awards']
        info1.imdb = movie_list_2['movie2_imdb']
        info1.movie_director = movie_list_2['movie2_director']
        info1.movie_rating = movie_list_2['movie2_rating']
        info1.movie_stars = movie_list_2['movie2_stars']
        info1.movie_plot = movie_list_2['movie2_plot']
        info1.movie_runtime = movie_list_2['movie2_runtime']
        info1.movie_earn = movie_list_2['movie2_box']
        info1.movie_poster = movie_list_2['movie2_poster']
        info1.save()

        info2 = MovieInfo()
        info2.user = user
        info2.movie_name = movie_list_3['movie3_name']
        info2.awards = movie_list_3['movie3_awards']
        info2.imdb = movie_list_3['movie3_imdb']
        info2.movie_year = movie_list_3['movie3_year']
        info2.movie_director = movie_list_3['movie3_director']
        info2.movie_rating = movie_list_3['movie3_rating']
        info2.movie_stars = movie_list_3['movie3_stars']
        info2.movie_plot = movie_list_3['movie3_plot']
        info2.movie_runtime = movie_list_3['movie3_runtime']
        info2.movie_earn = movie_list_3['movie3_box']
        info2.movie_poster = movie_list_3['movie3_poster']
        info2.save()

        albums = MovieInfo.objects.filter(user=request.user).values('user_rating','pk', 'movie_name', 'movie_earn', 'movie_rating',
                                                                    'movie_plot', 'movie_poster', 'movie_year',
                                                                    'movie_director', 'movie_runtime',
                                                                    'movie_stars').distinct()

        return redirect('index')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = MovieInfo.objects.filter(user=request.user).values('user_rating','pk', 'movie_name', 'movie_earn',
                                                                            'movie_rating', 'movie_plot',
                                                                            'movie_poster', 'movie_year',
                                                                            'movie_director', 'movie_runtime',
                                                                            'movie_stars').distinct()
                if albums:
                    return redirect('index')
                else:
                    return render(request, 'recommender/home.html')
            else:
                return render(request, 'recommender/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'recommender/login.html', {'error_message': 'Invalid login'})
    return render(request,'recommender/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'recommender/home.html')
    context = {
        "form": form,
    }
    return render(request, 'recommender/register.html', context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'recommender/login.html', context)

def detail(request,pk):
    if not request.user.is_authenticated:
        return render(request, 'recommender/login.html')
    else:
        user = request.user
        album = get_object_or_404(MovieInfo, pk=pk)
        return render(request, 'recommender/detail.html', {'album': album, 'user': user})


def delete(request,pk):
    MovieInfo.objects.get(pk=pk).delete()
    albums = MovieInfo.objects.filter(user=request.user).values('user_rating','pk', 'movie_name', 'movie_earn', 'movie_rating',
                                                                'movie_plot', 'movie_poster', 'movie_year',
                                                                'movie_director', 'movie_runtime',
                                                                'movie_stars').distinct()

    return redirect('index')

def rating1(request, pk):
    album = get_object_or_404(MovieInfo, pk=pk)
    try:
        if album.star1:
            album.star1 = False
        else:
            album.star1 = True
            album.user_rating = 1
        album.save()
    except (KeyError, MovieInfo.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def rating2(request, pk):
    album = get_object_or_404(MovieInfo, pk=pk)
    try:
        if album.star2:
            album.star1 = False
            album.star2 = False
        else:
            album.star1 = True
            album.star2 = True
            album.user_rating = 2
        album.save()
    except (KeyError, MovieInfo.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def rating3(request, pk):
    album = get_object_or_404(MovieInfo, pk=pk)
    try:
        if album.star3:
            album.star1 = False
            album.star2 = False
            album.star3 = False
        else:
            album.star1 = True
            album.star2 = True
            album.star3 = True
            album.user_rating = 3
        album.save()
    except (KeyError, MovieInfo.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def rating4(request, pk):
    album = get_object_or_404(MovieInfo, pk=pk)
    try:
        if album.star4:
            album.star1 = False
            album.star2 = False
            album.star3 = False
            album.star4 = False
        else:
            album.star1 = True
            album.star2 = True
            album.star3 = True
            album.star4 = True
            album.user_rating = 4
        album.save()
    except (KeyError, MovieInfo.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def rating5(request, pk):
    album = get_object_or_404(MovieInfo, pk=pk)
    try:
        if album.star5:
            album.star1 = False
            album.star2 = False
            album.star3 = False
            album.star4 = False
            album.star5 = False
        else:
            album.star1 = True
            album.star2 = True
            album.star3 = True
            album.star4 = True
            album.star5 = True
            album.user_rating = 5
        album.save()
    except (KeyError, MovieInfo.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
