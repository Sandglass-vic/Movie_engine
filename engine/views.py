from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from datetime import datetime
from engine.models import *
from django.db.models import Q

import random


def info_dict(info_type: str, page_num: int, per_page=25):
    range_len = 2
    # Get data
    if info_type == 'movies':
        data = Movie.objects.all()
    elif info_type == 'celebrities':
        data = Celebrity.objects.all()
    else:
        data = None
    # Return the corresponding page
    paginator = Paginator(data, per_page=per_page)
    page_num = min(paginator.num_pages, page_num)
    page_num = max(page_num, 1)
    page_num_range = range(max(1, page_num - range_len), min(paginator.num_pages, page_num + range_len) + 1)
    page = paginator.get_page(page_num)
    return {'all_num': paginator.count, 'page': page, 'page_num_range': page_num_range}


def index(request):
    page_num = int(request.GET.get('page', 1))
    return render(request, 'engine/movies_info.html', info_dict(info_type='movies', page_num=page_num))


def movies_info(request):
    page_num = int(request.GET.get('page', 1))
    return render(request, 'engine/movies_info.html', info_dict(info_type='movies', page_num=page_num))


def celebrities_info(request):
    page_num = int(request.GET.get('page', 1))
    return render(request, 'engine/celebrities_info.html', info_dict(info_type='celebrities', page_num=page_num))


def search_dict(search_type: str, keyword: str, page_num: int, per_page=10):
    range_len = 2
    # Get data
    t_begin = datetime.now()
    if search_type == 'movie':
        data = Movie.objects.filter(Q(celebrity__name__contains=keyword) | Q(name__contains=keyword)).distinct()
    elif search_type == 'celebrity':
        data = Celebrity.objects.filter(Q(name__contains=keyword) | Q(movies__name__contains=keyword)).distinct()
    elif search_type == 'review':
        data = Review.objects.filter(Q(text__contains=keyword)).distinct()
    else:
        data = None
    time_cost = (datetime.now() - t_begin).total_seconds()
    # Return the corresponding page
    paginator = Paginator(data, per_page=per_page)
    page_num = min(paginator.num_pages, page_num)
    page_num = max(page_num, 1)
    page_num_range = range(max(1, page_num - range_len), min(paginator.num_pages, page_num + range_len) + 1)
    page = paginator.get_page(page_num)
    return {'search_type':search_type, 'keyword': keyword, 'time_cost': time_cost, 'all_num': paginator.count,
            'page': page, 'page_num_range': page_num_range}


def search(request):
    search_type = request.GET['search_type']
    keyword = request.GET['keyword']
    if not keyword:
        return redirect('engine:index')
    page_num = int(request.GET.get('page', 1))
    if search_type == 'movie':
        return render(request, 'engine/search_movie.html', search_dict(search_type='movie', keyword=keyword,
                                                                       page_num=page_num))
    elif search_type == 'celebrity':
        return render(request, 'engine/search_celebrity.html', search_dict(search_type='celebrity', keyword=keyword,
                                                                           page_num=page_num))
    elif search_type == 'review':
        return render(request, 'engine/search_review.html', search_dict(search_type='review', keyword=keyword,
                                                                        page_num=page_num))
    else:
        return reverse('engine:index')


def movie_info(request, its_index: int):
    movie = Movie.objects.get(index=its_index)
    return render(request, 'engine/movie_info.html', {'movie': movie, 'actors': movie.celebrity_set.all(),
                                                      'reviews': movie.review_set.all()})


def celebrity_info(request, its_index):
    celebrity = Celebrity.objects.get(index=its_index)
    coactors = list(celebrity.coactor_set.all())
    coactors.sort(key=lambda coactor: coactor.times, reverse=True)
    return render(request, 'engine/celebrity_info.html', {'celebrity': celebrity, 'movies': celebrity.movies.all(),
                                                          'coactors': coactors[:10]})