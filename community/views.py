# community/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'community/post_list.html', {'page_obj': page_obj})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    
    return render(request, 'community/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You can't edit this post.")
        return redirect('community:post_detail', pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form, 'editing': True})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You can't delete this post.")
        return redirect('community:post_detail', pk=pk)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community:post_list')
    
    return render(request, 'community/post_confirm_delete.html', {'post': post})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('community:post_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, "You can't delete this comment.")
        return redirect('community:post_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('community:post_detail', pk=post_pk)

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    html = render_to_string(
        'community/includes/post_list_results.html',
        {'posts': posts},
        request=request
    )
    
    return JsonResponse({
        'html': html,
        'count': posts.count()
    })