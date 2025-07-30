from rest_framework import serializers

from blog import models
from core.serializers import BaseSearchSerializer


class PostListItemSerializer(serializers.ModelSerializer):
    """ Api serializer for Post model in list endpoint (summary)"""
    
    class Meta:
        model = models.Post
        fields = (
            "id",
            "title",
            "slug",
            "lang",
            "banner_image_url",
            "description",
            "author",
            "created_at",
            "updated_at",
        )
        
        
class PostDetailSerializer(PostListItemSerializer):
    """ Api serializer for Post model with full fields """
    
    related_post = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Post
        fields = "__all__"
        
    def get_related_post(self, obj) -> dict:
        """Retrieve related post as dict"""
        
        if not obj.related_post:
            return {
                "id": None,
                "title": None,
                "slug": None,
            }
        
        return {
            "id": obj.related_post.id,
            "title": obj.related_post.title,
            "slug": obj.related_post.slug,
        }
        

class PostSearchSerializer(BaseSearchSerializer):
    """ Api serializer for Post model in search endpoint """
    
    # Calculated fields
    image = serializers.URLField(source="banner_image_url")
    extra = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="updated_at")
    type = serializers.CharField(default="post")
    
    # overwrite model
    class Meta(BaseSearchSerializer.Meta):
        model = models.Post

    def get_extra(self, obj) -> dict:
        """Retrieve extra fields (author) as dict"""
        
        return {
            "author": obj.author,
        }