from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# posts = [
#     {
#         'author': 'Max Finn',
#         'title': 'Who Has Two Thumbs and Isn\'t Going to Get Enough Sleep Tonight',
#         'content': 'This guy!',
#         'date_posted': 'April 20, 2020',
#     },
#     {
#         'author': 'Max Finn',
#         'title': '4Chan: A Hacker Biography',
#         'content': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
#         'date_posted': 'April 21, 2020',
#     },
#     {
#         'author': 'Max Finn',
#         'title': 'Hot Take: White Claws Suck',
#         'content': 'Drink real alcohol, and it\'s only 5%. Look up malt liquor. Thanks for coming to my Ted talk.',
#         'date_posted': 'April 22, 2020',
#     }
# ]

# def index(request):
#     context = {
#         'posts': Post.objects.all()
#         # 'posts': posts
#     }
#     return render(request, 'blog/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        
class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
