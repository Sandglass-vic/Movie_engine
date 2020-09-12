import json
import os
import re
from django.core.management.base import BaseCommand
from engine.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Delete the created objs
        if Movie.objects.all():
            Movie.objects.all().delete()
        if Celebrity.objects.all():
            Celebrity.objects.all().delete()
        # Load movie data
        movie_data_path = os.getcwd() + "\\data\\movie\\"
        movie_index_set = os.listdir(movie_data_path)
        for movie_index in movie_index_set:
            # Create a movie obj
            with open(movie_data_path + movie_index, 'r', encoding='utf-8') as file:
                data = json.load(file)
                index = int(re.findall('([0-9]*?).json', movie_index)[0])
                # Str
                name = data['name'][0] if data['name'] else ""
                region = data['region'][0] if data['region'] else ""
                language = data['language'][0] if data['language'] else ""
                # Numbers
                year = int(data['year'][0]) if data['year'] else 0
                runtime = float(data['runtime'][0]) if data['runtime'] else 0
                rank = int(data['rank'][0]) if data['rank'] else 0
                # List
                director = "\n".join(data['director']) if data['director'] else ""
                writer = "\n".join(data['writer']) if 'writer' in data and data['writer'] else ""
                genre = "\n".join(data['genre']) if data['genre'] else None
                release_date = "\n".join(data['release_date']) if data['release_date'] else ""
                other_names = "\n".join(data['other_names']) if 'other_names' in data and data['other_names'] else ""
                intro = "\n".join(data['intro']) if 'intro' in data and data['intro'] else ""
                movie = Movie(index=index, name=name, region=region, language=language, year=year, runtime=runtime,
                              rank=rank, director=director, writer=writer, genre=genre, release_date=release_date,
                              other_names=other_names, intro=intro
                              )
                movie.save()
                # Create review objs
                cot = 0
                for piece in data['review']:
                    Review.objects.create(index=movie.index*10+cot, text=piece, from_movie=movie)
                    cot += 1
                # Create its actors or add a link between them
                for actor_index in data['actor_index']:
                    celebrity = None
                    if Celebrity.objects.filter(index=actor_index):
                        celebrity = Celebrity.objects.get(index=actor_index)
                    else:
                        # Create a new celebrity
                        celebrity_data_path = os.getcwd() + ("\\data\\celebrity\\%d.json" % actor_index)
                        with open(celebrity_data_path, 'r', encoding='utf-8') as celebrity_file:
                            celebrity_data = json.load(celebrity_file)
                            name = celebrity_data['name'][0] if celebrity_data['name'] else ''
                            gender = celebrity_data['gender'][0] if celebrity_data['gender'] else ''
                            constellation = celebrity_data['constellation'][0] if celebrity_data[
                                'constellation'] else ''
                            birthday = celebrity_data['birthday'][0] if celebrity_data['birthday'] else ''
                            birthplace = celebrity_data['birthplace'][0] if celebrity_data['birthplace'] else ''
                            # List
                            occupation = "\n".join(celebrity_data['occupation']) if 'occupation' in celebrity_data \
                                                                                    and celebrity_data['occupation'] else ""
                            other_names = "\n".join(celebrity_data['other_names']) if 'other_names' in celebrity_data \
                                                                                      and celebrity_data['other_names'] else ""
                            families = "\n".join(celebrity_data['families']) if 'families' in celebrity_data \
                                                                                and celebrity_data['families'] else ""
                            intro = "\n".join(celebrity_data['intro']) if 'intro' in celebrity_data \
                                                                          and celebrity_data['intro'] else ""
                            celebrity = Celebrity(index=actor_index, name=name, gender=gender,
                                                  constellation=constellation, birthday=birthday,
                                                  birthplace=birthplace, occupation=occupation, other_names=other_names,
                                                  families=families, intro=intro
                                                  )
                            celebrity.save()
                    movie.celebrity_set.add(celebrity)
                    # Co_actors
                    for other_index in data['actor_index']:
                        if other_index == actor_index:
                            continue
                        # Whether they have other co-acted films or not
                        if celebrity.coactor_set.filter(index=other_index):
                            coactor = celebrity.coactor_set.get(index=other_index)
                            coactor.times += 1
                            coactor.save()
                        else:
                            Coactor.objects.create(index=other_index, from_who=celebrity)
