from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Filter reviews parent none"""
    
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecuresiveSerializer(serializers. Serializer):
    """Show childrens recursive"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """List of actors and directors"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorRetrieveSerializer(serializers.ModelSerializer):
    """Show all fields for actor or director"""

    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    """List of movies"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ("id","title", "tagline", 'category', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    """List review"""

    childrens = RecuresiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "name", "text", "childrens")


class MovieRetrieveSerializer(serializers.ModelSerializer):
    """Movie retrieve"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Create rating"""

    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get("ip"),
            movie=validated_data.get("movie", None),
            defaults={'star': validated_data.get("star")}
        )
        return rating