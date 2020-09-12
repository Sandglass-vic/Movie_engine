from django import template
from engine.models import *

register = template.Library()


@register.simple_tag(name='brief')
def brief(movie: Movie, length=100):
    intro = movie.intro
    return intro[:length] + '...' if len(intro) >= length else intro


@register.simple_tag(name='movie_image')
def movie_image(movie: Movie):
    return 'engine/images/movie/%d.png' % movie.index


@register.simple_tag(name='celebrity_image')
def celebrity_image(celebrity: Celebrity):
    return 'engine/images/celebrity/%d.png' % celebrity.index


@register.simple_tag(name='movie_actors')
def movie_actors(movie: Movie):
    return movie.celebrity_set.all()


@register.simple_tag(name='celebrity_movies')
def celebrity_movies(celebrity: Celebrity):
    return celebrity.movies.all()


@register.simple_tag(name='celebrity_image_from_index')
def celebrity_image_from_index(index: int):
    return celebrity_image(Celebrity.objects.get(index=index))


@register.simple_tag(name='celebrity_name_from_index')
def celebrity_name_from_index(index: int):
    return Celebrity.objects.get(index=index).name


@register.simple_tag(name='to_list')
def to_list(mystring: str):
    return mystring.split('\n')


@register.simple_tag(name='slash_join')
def slash_join(mystring: str):
    return '/'.join(mystring.split('\n'))


@register.simple_tag(name='get_min')
def get_min(r: range):
    if r:
        return r[0]


@register.simple_tag(name='get_max')
def get_max(r: range):
    if r:
        return r[len(r) - 1]
