from django.db.models import Q

from rest_framework import viewsets

from content import models as content_models
from blog import models as blog_models
from properties import models as properties_models
from content import serializers
from blog.serializers import PostSearchSerializer
from properties.serializers import PropertySearchSerializer
from content.serializers import SearchLinkSearchSerializer


class BestDevelopmentsImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = content_models.BestDevelopmentsImage.objects.all()
    serializer_class = serializers.BestDevelopmentsImageSerializer
    pagination_class = None


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    """Api viewset for search endpoint (properties and posts)"""

    def list(self, request, *args, **kwargs):

        # Get lang from Accept-Language
        lang = request.headers.get("Accept-Language", "es")
        query = request.query_params.get("q", "")

        # Fetch data from both models
        posts = blog_models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query),
            lang=lang,
        )
        properties = properties_models.Property.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__description__en__icontains=query) |
            Q(short_description__description__es__icontains=query) |
            Q(description_es__icontains=query) |
            Q(description_en__icontains=query),
            active=True,
        )
        search_links = content_models.SearchLink.objects.filter(
            Q(title__es__icontains=query) |
            Q(title__en__icontains=query) |
            Q(description__es__icontains=query) |
            Q(description__en__icontains=query),
        )

        # Serialize them with request context
        post_data = [
            PostSearchSerializer(post, context={"request": request}).data
            for post in posts
        ]
        property_data = [
            PropertySearchSerializer(prop, context={"request": request}).data
            for prop in properties
        ]
        search_link_data = [
            SearchLinkSearchSerializer(link, context={"request": request}).data
            for link in search_links
        ]

        # Merge and optionally sort
        merged = post_data + property_data + search_link_data

        # sort by date field
        merged.sort(key=lambda result: result.get("date"), reverse=True)

        # Optional: manually apply pagination
        page = self.paginate_queryset(merged)
        if page is not None:
            return self.get_paginated_response(page)

        return merged
