from django.db.models import Count, Avg
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from movies.models import Movie
from movies.serializers import MovieModelSerializer, MovieListDetailSerializer
from app.permissions import GlobalDefaultPermission
from reviews.models import Review


# automatico - usando a generics do Django Rest
class MovieCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    # serializer_class = MovieModelSerializer - retornando o serializar padrao.

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


# automatico - usando a generics do Django Rest
class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    # serializer_class = MovieModelSerializer - retornando o serializar padrao.

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


# criando manual usando a APIView ( personalizado )
class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request):
        total_movies = self.queryset.count()
        movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        total_reviews = Review.objects.count()
        average_stars = Review.objects.aggregate(avg_stars=Avg('stars'))['avg_stars']

        return response.Response(
            data={'total_movies': total_movies,
                  'movies_by_genre': movies_by_genre,
                  'total_reviews': total_reviews,
                  'average_stars': round(average_stars, 1) if average_stars else 0,
                  }, status=status.HTTP_200_OK
        )

    # criei de teste para aprendizado

    # def post( self, request):
    #     total=Review.objects.count()

    #     return response.Response(
    #         data={'total': total},
    #         status=status.HTTP_200_OK )
