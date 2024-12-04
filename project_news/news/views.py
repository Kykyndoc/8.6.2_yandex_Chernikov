from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.NEWS
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.ARTICLE
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.NEWS
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.ARTICLE
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


