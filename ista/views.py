from django.shortcuts import render, get_object_or_404
from .models import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import ImageForm
# Create your views here.

class PostListView(ListView):
    model = Image
    template_name = 'ista/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'images'
    ordering = ['-date_posted']
    paginate_by = 5    

class UserPostListView(ListView):
    model = Image
    template_name = 'ista/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'images'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Image  
    context_object_name = 'image'
    template_name = 'ista/detail_posts.html' 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class=ImageForm
    template_name='ista/create_posts.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    form_class=ImageForm
    template_name='ista/create_posts.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    success_url = '/'
    template_name='ista/confirm_delete_posts.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

   