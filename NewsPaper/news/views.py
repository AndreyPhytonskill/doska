from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author,Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    permission_required = ('post.Can change post',)
    form_class = PostForm


# метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostsList(ListView):
    paginate_by = 10
    model = Post
    ordering = 'time'
    template_name = 'posts.html'
    context_object_name = 'news'


#class SearchAuthor(ListView):
#    model = Author


class SearchPosts(ListView):
    paginate_by = 10
    model = Post
    ordering = 'time'
    template_name = 'post_seach.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_edit.html'
    permission_required = ('post.Can add post',)
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


# дженерик для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    permission_required = ('post.Can delete post',)
    queryset = Post.objects.all()
    success_url = '/news/'

class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.Can add post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.Can change post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('post.Can delete post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.Can add post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.Can change post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('post.Can delete post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить новость"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

class CategorySubscribeView(ListView):
    model = Category
    template_name = 'post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def subscribe_category(request, pk):
     user = request.user
     category = Category.objects.get(id=pk)
     category.subscribers.add(user)
     id_u = request.user.id
     email = category.subscribers.get(id=id_u).email
     send_mail(
         subject=f'News Portal: подписка на обновления категории {category}',
         message=f'«{request.user}», вы подписались на обновление категории: «{category}».',
         from_email='subscribe.category@yandex.ru',
         recipient_list=[f'{email}', ],
        )
     return redirect('/news')