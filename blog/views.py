from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin #заменяет логин_реккуайерд т.к. у нас класс а не функция
from django.contrib.auth.mixins import UserPassesTestMixin #нужно для того чтобы пользователь мог редактировать только свой пост
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    context = {
        'posts':Post.objects.all() 
    } #таким образом мы даём доступ переменной posts на странице
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post #какую модель использует
    template_name = 'blog/home.html' #поменяли страницу по умолчанию
    context_object_name = 'posts' #переменная цикла на странице
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post 
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts' 
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

class PostDetailView(DetailView):
    model = Post 

class PostCreateView(LoginRequiredMixin, CreateView): 
    model = Post 
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #устанавлиает значение юзера перед сабмитом формы
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post 
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #устанавлиает значение юзера перед сабмитом формы
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/' #если это не добавить то пост не удалится и так же здесь показываем куда редирект

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False