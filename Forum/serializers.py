from rest_framework.serializers import ModelSerializer
from .models import Category, Article, ArticleComments, Question, QuestionComments,ArticleLiked


class CategoriesSerializers(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ArticleSerializers(ModelSerializer):


    class Meta:
        model = Article
        fields = "__all__"

        extra_kwargs={
            "views":{"read_only":True}
        }



class ArticleCommentSerializers(ModelSerializer):
    class Meta:
        model = ArticleComments
        fields = "__all__"


class QuestionSerializers(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

        extra_kwargs={
            "views":{"read_only":True}
        }


class QuestionCommentSerializers(ModelSerializer):
    class Meta:
        model = QuestionComments
        fields = "__all__"

class ArticleLikedSerializer(ModelSerializer):
    class Meta:
        model = ArticleLiked
        fields = ("article",)
