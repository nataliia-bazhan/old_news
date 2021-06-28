from django.shortcuts import redirect


def news(request):
    return redirect("content:posts")
