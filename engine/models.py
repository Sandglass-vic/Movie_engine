from django.db import models


class Movie(models.Model):
    # Exception 0
    index = models.IntegerField(primary_key=True, unique=True)
    year = models.IntegerField()
    runtime = models.IntegerField()
    rank = models.FloatField()
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    genre = models.CharField(max_length=40)
    release_date = models.CharField(max_length=80)
    other_names = models.CharField(max_length=40)
    intro = models.TextField(max_length=3000)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return self.name


class Review(models.Model):
    # index = from_movie.index * 10 + its order
    index = models.IntegerField(unique=True)
    text = models.TextField(max_length=3000)
    from_movie = models.ForeignKey(Movie, to_field='index',  on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]


class Celebrity(models.Model):
    index = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=4)
    constellation = models.CharField(max_length=10)
    birthday = models.CharField(max_length=15)
    birthplace = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50)
    families = models.CharField(max_length=100)
    intro = models.TextField(max_length=2000)
    movies = models.ManyToManyField(Movie)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return self.name


class Coactor(models.Model):
    index = models.IntegerField(unique=False)
    times = models.IntegerField(unique=False, default=1)
    from_who = models.ForeignKey(Celebrity, to_field='index', on_delete=models.CASCADE)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return Celebrity.objects.get(index=self.index).__str__()