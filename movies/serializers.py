from rest_framework import serializers

from .models import Movie, Review, Rating


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


class MovieListSerializer(serializers.ModelSerializer):
    """List of movies"""

    class Meta:
        model = Movie
        fields = ("title", "tagline", 'category')


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
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
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
        rating = Rating.objects.update_or_create(
            ip=validated_data.get("ip"),
            movie=validated_data.get("movie", None),
            defaults={'star': validated_data.get("star")}
        )
        return rating