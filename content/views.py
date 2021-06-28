from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from background_task import background


def all_posts(request):
    context = {'posts': Post.objects.all()}
    return render(request, "all_posts.html", context)


def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.up_votes = 0
        new_post.author = request.user
        new_post.save()
        context = {
            "link": new_post.link,
            "title": new_post.title,
            "author": request.user.username,
        }
    context["form"] = PostForm()
    return render(request, "create_post.html", context)


def post_details(request, pk):
    post = Post.objects.get(id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = Post.objects.get(id=pk)
        new_comment.up_votes = 0
        new_comment.author = request.user
        new_comment.save()
    context = {}
    context["form"] = CommentForm()
    context["post"] = post
    return render(request, "post_details.html", context)


def post_update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.link = form.cleaned_data["link"]
            post.save()
            return redirect("content:user_content")
    else:
        form = PostForm(instance=post)
    context = {"form": form}
    return render(request, "post_update.html", context)


def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect("content:user_content")


def all_comments(request):
    context = {"comments": Comment.objects.all()}
    return render(request, "all_comments.html", context)


def comment_update(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data["content"]
            comment.save()
            return redirect("content:user_content")
    else:
        form = CommentForm(instance=comment)
    context = {"form": form}
    return render(request, "comment_update.html", context)


def comment_delete(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect("content:user_content")


def user_content(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)
    context = {"posts": posts, "comments": comments, "user": request.user}
    return render(request, "user_content.html", context)


def post_vote(request, pk):
    post = Post.objects.get(id=pk)
    if request.user in post.get_users_voted():
        post.up_votes -= 1
        post.users_voted.remove(request.user)
    else:
        post.up_votes += 1
        post.users_voted.add(request.user)
    post.save()
    posts = Post.objects.all()
    return render(request, "all_posts.html", {"posts": posts})


def comment_vote(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user in comment.get_users_voted():
        comment.up_votes -= 1
        comment.users_voted.remove(request.user)
    else:
        comment.up_votes += 1
        comment.users_voted.add(request.user)
    comment.save()
    comments = Comment.objects.all()
    return render(request, "all_comments.html", {"comments": comments})


@background(schedule=60)
def clear_votes():
    for comment in Comment.objects.all():
        comment.up_votes = 0
        comment.users_voted.clear()
        comment.save()
    for post in Post.objects.all():
        post.up_votes = 0
        post.users_voted.clear()
        post.save()


clear_votes(repeat=60 * 60 * 24)
