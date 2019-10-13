from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

# Create your views here.

# POST VIEWS
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # Define how to grab this list, SQL Query
    def get_queryset(self):
        # published_date__lte == less than or equal to the current time - translates SQL code into Python
        # '-published_date' == descending, so most recent post showing first
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

# This shows the post form
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    # In case user is not logged in, go to log in page
    # Must be logged in to create a post
    login_url = '/login/'
    # After the user is logged in, redirect to the post form
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Post
    # You don't want the success_url to activate until you delete it
    success_url = reverse_lazy('post_list')

# A view for unpublished drafts
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

@login_required
# This function calls the Post Model's publish method
def post_publish (request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

########################
# Above are the VIEWS for the BLOG POST #
########################
# Below are the VIEWS for the COMMENTS #
########################

# COMMENT VIEWS

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

        return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)

    # Call approve method from Comment Model which sets the approved_comment attribute to True
    comment.approve()

    # Comment Model includes post as a foreign key; after approving that comment, if I want to go to the post of that comment, I need to redirect to post.pk, thus...
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
