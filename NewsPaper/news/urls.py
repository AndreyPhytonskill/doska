from django.urls import path
# импортируем наши представления
from .views import PostsList, PostDetail, SearchPosts,CategorySubscribeView
from .views import ArticleCreate, ArticleUpdate, ArticleDelete
from .views import NewsCreate, NewsUpdate, NewsDelete,subscribe_category

urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchPosts.as_view(), name='search_posts'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('category/', CategorySubscribeView.as_view()),
    path('category/<int:pk>', subscribe_category, name='subscribe_category'),
]