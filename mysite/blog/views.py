from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Post2, Comment2, Like, Profile
from .forms import PostForm, CommentForm, PostForm2, CommentForm2, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
#from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
#from .models import User

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import logout

@login_required
def mypage(request):
    user = request.user
    def two_interests_overlap(one, two):
        i_1 = set([s.strip() for s in one.split("#") if len(s.strip()) > 0])
        i_2 = set([s.strip() for s in two.split("#") if len(s.strip()) > 0])
        return len(i_1.intersection(i_2)) > 0
    interest = request.user.profile.interest
    all_profiles = Profile.objects.all()
    users = [p.user
     for p in all_profiles
     if p.user != user and two_interests_overlap(p.interest, interest)]

    myposts = Post.objects.filter(author=user)
    mycomments = Comment.objects.filter(author=user)

    like_count = 0
    for p in myposts:
        like = Like.objects.filter(post=p, comment=None)
        like_count += len(like)
    for p in mycomments:
        like = Like.objects.filter(post=None, comment=p)
        like_count += len(like)

    return render(request, 'registration/mypage.html', {'user': user, 'recom_users': users, 'like_count':like_count})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        #user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/mypage')
        else:
            pass
            #messages.error(request, _('Please correct the error below.'))
    else:
        #user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/update_user.html', {
        #'user_form': user_form,
        'profile_form': profile_form
    })

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
        return redirect('/')
    else:
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})

def user_check(request):
    users = User.objects.filter(username=request.GET['username'])
    return render(request, 'registration/usercheck.html', {'num_users': len(users)})

@login_required
@transaction.atomic
def increment_like(request, pk, posttype):
    user = request.user
    if posttype == 'post':
        post = get_object_or_404(Post, pk=pk)
        p = post
        like = Like.objects.filter(user=user, post=post, comment=None)
    elif posttype == 'comment':
        post = get_object_or_404(Comment, pk=pk)
        p = post.post
        like = Like.objects.filter(user=user, comment=post, post=None)

    if len(like) > 0:
        return render(request, 'blog/like.html', {'response': len(like)})
    if posttype == 'post':
        new_like = Like(user=user, post=post)
    elif posttype == 'comment':
        new_like = Like(user=user, comment=post)
    new_like.save()
    return render(request, 'blog/like.html', {'response': len(like), 'post': p})

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(post=post)
    userlike = Like.objects.filter(user=request.user, post=post)
    comments = post.comments.all()
    userlikes = [len(Like.objects.filter(user=request.user, comment=comment)) for comment in comments]

    return render(request, 'blog/post_detail.html', {'post': post, 'num_like': len(like), 'userlike': len(userlike),
                                                     'comzip': zip(comments, userlikes)})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def post_list2(request):
    posts = Post2.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list2.html', {'posts': posts})

@login_required
def post_detail2(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    cur_time = timezone.now()
    return render(request, 'blog/post_detail2.html', {'post': post, 'cur_time': cur_time})

@login_required
def post_new2(request):
    if request.method == "POST":
        form = PostForm2(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail2', pk=post.pk)
    else:
        form = PostForm2()
    return render(request, 'blog/post_edit2.html', {'form':form})

@login_required
def post_edit2(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    if request.method == "POST":
        form = PostForm2(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail2', pk=post.pk)
    else:
        form = PostForm2(instance=post)
    return render(request, 'blog/post_edit2.html', {'form': form})

@login_required
def post_remove2(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    post.delete()
    return redirect('post_list2')

def add_comment_to_post2(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    if request.method == "POST":
        form = CommentForm2(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail2', pk=post.pk)
    else:
        form = CommentForm2()
    return render(request, 'blog/add_comment_to_post2.html', {'form': form})

@login_required
def comment_approve2(request, pk):
    comment = get_object_or_404(Comment2, pk=pk)
    comment.approve()
    return redirect('post_detail2', pk=comment.post.pk)

@login_required
def comment_remove2(request, pk):
    comment = get_object_or_404(Comment2, pk=pk)
    comment.delete()
    return redirect('post_detail2', pk=comment.post.pk)

@login_required
def recommend(request):
    user = request.user
    def two_interests_overlap(one, two):
        i_1 = set([s.strip() for s in one.split("#") if len(s.strip()) > 0])
        i_2 = set([s.strip() for s in two.split("#") if len(s.strip()) > 0])
        return len(i_1.intersection(i_2)) > 0
    interest = request.user.profile.interest
    all_profiles = Profile.objects.all()
    users = [p.user
     for p in all_profiles
     if p.user != user and two_interests_overlap(p.interest, interest)]

    return render(request, 'blog/recommend.html', {'user': user, 'recom_users': users})
