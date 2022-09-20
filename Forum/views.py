from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from Forum.models import Article, Category, ArticleComments, Question


class BaseView(View):
    view = {}


class BlogHomeView(BaseView):
    def get(self, request):
        self.view['blogs'] = Article.objects.filter(publish=True)
        self.view['categories'] = Category.objects.all()
        self.view['trend'] = Article.objects.filter(trending=True)

        return render(self.request, 'blog.html', self.view)


class CategoryView(BaseView):
    def get(self, request, name):
        self.view['blogs'] = Article.objects.filter(publish=True)
        self.view['categories'] = Category.objects.all()
        self.view['trend'] = Article.objects.filter(trending=True)

        return render(self.request, 'blog_category.html', self.view)


class BlogDetailView(BaseView):
    def get(self, request, slug, *args, **kwargs):
        self.view['blogs_detail'] = Article.objects.filter(slug=slug)
        self.view['comments'] = ArticleComments.objects.all()
        return render(self.request, 'single-post.html', self.view)

    def post(self, request, slug, *args, **kwargs):
        comment = request.POST['comments']
        username = request.user

        return HttpResponse('/forum/blog/slug')


def AskQuestionView(request):
    cat_view = {}
    if request.method == 'POST':
        question = request.POST['question']
        images = request.FILES['images']
        questions = Question.objects.create(
            asked_by=request.user,
            question=question
        )
        questions.save()
        messages.success(request, 'Your question is submitted')
        return HttpResponse('hello')
    cat_view['categories'] = Category.objects.all()
    return render(request, 'ask_question.html')


class UserQAView(BaseView):
    def get(self, request):
        return render(self.request, 'userqa.html', self.view)


class UserQaDetailView(BaseView):
    def get(self, request):
        return render(self.request, 'userqa.html', self.view)


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
