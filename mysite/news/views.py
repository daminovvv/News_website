from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


class HomeNews(ListView):
    paginate_by = 3
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)


class CategoryNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryNews, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
