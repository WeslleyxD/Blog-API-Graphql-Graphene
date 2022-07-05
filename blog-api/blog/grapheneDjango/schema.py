from enum import Enum
from unicodedata import name
from graphene import ID, Boolean, Int, ObjectType, String, Schema, List, Field, String, Mutation
from graphene_django import DjangoObjectType
from blog.models import Post, Comment
from django.utils.text import slugify



class NoInListError (Exception):
    pass

# https://docs.graphene-python.org/projects/django/en/latest/schema/
# https://docs.graphene-python.org/en/latest/quickstart/


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('__all__')
        convert_choices_to_enum = False
        description = 'testando xablau'

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('__all__')

class CreatePostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("title", "tag", "body")


class Query(ObjectType):
    all_posts = List(PostType,
            limit=Int(description='Quantidade de items buscados'), 
            order_by=String(description='Ordene por ["id" ou "publish"]. Para colocar em ordem descrente utilize "-" antes do parâmetro. Exemplo: "-id".'))
    get_post = Field(PostType, description='Obtenha um item de conforme o parâmetro', 
            id=ID(required=True))
    all_comments = List(CommentType)


    def resolve_all_posts(root, info, limit=None, order_by=None):   
        if limit:
            return Post.objects.all()[:limit]
        elif order_by:
            return Post.objects.all()[:limit].order_by(order_by)
        else:
            return Post.objects.all()
        

    def resolve_get_post(root, info, id):    
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None


    def resolve_all_comments(root, info):
        return Comment.objects.select_related("post").all()


#---------------------------------


class UpdatePost(Mutation):
    class Arguments:
        # The input arguments for this mutation
        title = String()
        id = ID(required=True)
        body = String()

    # The class attributes define the response of the mutation
    post = Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, title=None, body=None):
        post = Post.objects.get(pk=id)
        if title:
            post.title = title  
            post.slug = slugify(title)  
        if body:
            post.body = body
        post.save()

        # Notice we return an instance of this mutation
        return UpdatePost(post=post)




class CreatePost(Mutation):
    class Arguments:
        # The input arguments for this mutation
        title = String(required=True)
        tag = String(required=True)
        body = String(required=True)

    # The class attributes define the response of the mutation
    post = Field(CreatePostType)

    @classmethod
    def mutate(cls, root, info, title=None, tag=None, body=None):
        post_tag = Post.TAG_CHOICES
        all_tags = [tag_post[0] for tag_post in post_tag ]
        
        if tag.lower() in all_tags:
            post = Post.objects.create(title=title, tag=tag.lower(), body=body)
            post.slug = slugify(title)
            post.save()
        else: 
            raise NoInListError ('Tag inválida')
        
        # Notice we return an instance of this mutation
        return CreatePost(post=post)



class DeletePost(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = ID(required=True)

    # The class attributes define the response of the mutation
    post = Field(PostType)

    @classmethod
    def mutate(cls, root, info, id):

        post_id = Post.objects.get(id=id)
        post_id.delete()
        
        # Notice we return an instance of this mutation
        return



class Mutation(ObjectType):
    update_post = UpdatePost.Field()
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()


schema = Schema(query=Query, mutation=Mutation)