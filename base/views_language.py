from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Language, Language_Category

from .utils import check_what_language, extension_of_lang, humanize_date


def all_post(request):
    category = Language_Category.objects.all()

    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    if q:
        posts = Language.objects.filter(
            Q(user__username__icontains=q) |
            Q(title__icontains=q) |
            Q(lang__contains=q)
        )
        total_posts = len(posts)

        context = {"posts": posts, "category": category,
                   "total_posts": total_posts}
        return render(request, 'base/posts.html', context)

    posts = Language.objects.all()
    total_posts = len(posts)

    context = {"posts": posts, "category": category,
               "total_posts": total_posts}
    return render(request, 'base/posts.html', context)


def all_post_with_id(request, id):
    post = Language.objects.get(id=id)
    output = check_what_language(post)

    posts = Language.objects.all()
    total_posts = len(posts)
    category = Language_Category.objects.all()

    context = {"posts": posts, "category": category,
               "total_posts": total_posts, "output": output, "id": id}
    return render(request, 'base/posts.html', context)


@login_required
def create_post(request):
    category = Language_Category.objects.all()
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        lang = request.POST.get("lang")
        extension = extension_of_lang(lang)
        source = request.POST.get("source")
        description = request.POST.get('description')

        language = Language(user=user, lang=lang,
                            extension=extension, source=source, title=title, description=description)
        language.save()
        return redirect('posts-page')
    return render(request, 'base/create-post.html', {"category": category})


@login_required
def update_post(request, id):
    category = Language_Category.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        lang = request.POST.get("lang")
        extension = extension_of_lang(lang)
        source = request.POST.get("source")
        description = request.POST.get('description')

        language = Language.objects.filter(id=id)
        language.update(lang=lang,
                        extension=extension, source=source, title=title, description=description)
        return redirect('post', id)

    post = Language.objects.get(id=id)
    return render(request, 'base/update-post.html', {"category": category, "post": post})


@login_required
def delete_post(request, id):
    post = Language.objects.get(id=id)
    if request.method == "POST":
        post.delete()
        return redirect('posts-page')
    return render(request, 'base/delete-post.html', {"post": post})


def view_post(request, id):
    post = Language.objects.get(id=id)
    created = humanize_date(post.created)
    output = check_what_language(post)
    context = {"post": post, "output": output, "created": created}
    return render(request, 'base/post.html', context)
