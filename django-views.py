from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.db.models import Q
from .models import Page, Post
from .serializers import PageSerializer, PostSerializer
from .services.facebook import FacebookScraper
from .services.ai import generate_page_summary

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = StandardResultsSetPagination
    scraper = FacebookScraper()

    def get_object(self):
        username = self.kwargs.get('pk')
        
        # Check cache
        cache_key = f'page:{username}'
        page = cache.get(cache_key)
        if page:
            return page
        
        # Check database
        try:
            page = Page.objects.get(username=username)
            cache.set(cache_key, page, timeout=300)  # Cache for 5 minutes
            return page
        except Page.DoesNotExist:
            # Scrape new page
            try:
                page = self.scraper.scrape_page(username)
                cache.set(cache_key, page, timeout=300)
                return page
            except Exception as e:
                return Response(
                    {'error': f'Failed to scrape page: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['get'])
    def search(self, request):
        min_followers = request.query_params.get('min_followers')
        max_followers = request.query_params.get('max_followers')
        category = request.query_params.get('category')
        name = request.query_params.get('name')
        
        queryset = self.queryset
        
        if min_followers:
            queryset = queryset.filter(followers_count__gte=min_followers)
        if max_followers:
            queryset = queryset.filter(followers_count__lte=max_followers)
        if category:
            queryset = queryset.filter(category=category)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        page = self.get_object()
        posts = Post.objects.filter(page=page)
        
        page = self.paginate_queryset(posts)
        serializer = PostSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        page = self.get_object()
        followers = page.followers.all()
        
        page = self.paginate_queryset(followers)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        page = self.get_object()
        summary = generate_page_summary(page)
        return Response({'summary': summary})
