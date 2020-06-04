import graphene
import json
from datetime import datetime
import uuid


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4()) #we can have default vaue fr this field like this way
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())

    avatar_url = graphene.String()

    # This we have created just to demonstrate use of self
    def resolve_avatar_url(self,info):
        return 'https://cloudinary.com/{}/{}'.format(
            self.username,
            self.id
        )

#We need to define root Type i.e Query
class Query(graphene.ObjectType):
    users = graphene.List(User,limit=graphene.Int()) #if u ant to pass
                                                    # argument
    hello = graphene.String()
    is_admin = graphene.Boolean()

    # Below is nothing but resolver ,so every resolver
    # has to be prepended with resolve keyword
    def resolve_hello(self,info):
        return "World"

    def resolve_is_admin(self,info):
        return True

    # if u ant make this limit optional ,then u can have
    # limit=None
    def resolve_users(self,info,limit=None):
        return [
            User(id="1",username="saurabh",created_at=datetime.now()),
            User(id="2", username="Rajat1", created_at=datetime.now()),
            User(id="3", username="Shubham", created_at=datetime.now())
        ][:limit]


class CreateUser(graphene.Mutation):
    user=graphene.Field(User)

    class Arguments:  # This is the way to pass arguments
        username = graphene.String()

    # it is predefined , for every mutation ,it will be same
    def mutate(self,info,username):

        user=User(username=username)

        return CreateUser(user=user)

# Actually this CreatePost mutation is just created
# to understand functioning of info argument everywhere like in resolver and mutate()
# info => Here u will get context data,means in info
# u can access al context data that passed while executing Query or Mutation
# like Here if u see ,we are creating post but if we want to give this
# flexibility to authenticated users only ,then we need to kw ,which user is currently logged in
# so all this information will be passed from frontend while executing Query or Mutation
class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self,info,title,content):
        print(info, info.context,info.context.get('is_anonymous'),'---->context data info')
        if info.context.get('is_anonymous'):
            raise Exception("Not Authenticated")
        post=Post(title=title,content=content)
        return CreatePost(post=post)
#We need to define root Mutation Type i.e Root Mutation class i.e Mutation
# As we CRUD ,R-> root Type i.e Query (above class) is responsible
# but for remaining C-create ,Update,d-Delete
# Mutation is responsible
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field() #mutation has to be a class
                                    # like here CreateUser mutation is
    create_post   = CreatePost.Field()

# schema = graphene.Schema(query=Query,auto_camelcase=False)
schema = graphene.Schema(query=Query,mutation=Mutation)

# result=schema.execute(
#     """
#     {
#     hello
#     }
#     """
# )

#Here if u notice resolver name is is_admin
#but u can not use ,u have to use like isAdmin
#but u can override this bevahiour by specifying argument
# auto_camelcase=False in schema like below
# schema = graphene.Schema(query=Query,auto_camelcase=False)
# which is above if see
# result=schema.execute(
#     """
#     {
#     is_admin
#     }
#     """
# )

# result=schema.execute(
#     """
#     {
#     users(limit: 2){
#             username,
#             created_at
#               }
#     }
#     """
# )

#
# result=schema.execute(
#     """
#     mutation{
#     createUser(username : "Rajat"){
#             user{
#             id
#             username
#             createdAt
#
#             }
#             }
#     }
#     """
# )

# passing variable dynamically in mutation class


# $username:String -->This type has to match with
# createUser() argument username type
# result = schema.execute(
#     """
#     mutation($username:String){
#     createUser(username : $username){
#             user{
#             id
#             username
#             createdAt
#             }
#             }
#     }
#     """,
#
#     variable_values={'username':"Shubham"} # way of passing values
#                                          # of variable i.e username here
#                                         #dynamically
# )

# query getUsersQuery ($limit: Int) ==> query is predefined
# nothing but we are retrieving ,while retrieving ,how acn we pass variables
# vale dynamically
# getUsersQuery => this the name that we have given to this
# query ,u can have different name also
# result = schema.execute(
#     """
#     query getUsersQuery ($limit: Int){
#     users(limit : $limit){
#
#             id
#             username
#             createdAt
#
#             }
#     }
#     """,
#
#     variable_values={'limit':2} # way of passing values
#                                          # of variable i.e username here
#                                         #dynamically
# )


# for CreatePost
# context={'is_anonymous':True}  This way we can pass
# data in context dictionary
# result = schema.execute(
#     """
#     mutation{
#         createPost(title:"first ",content:"fisrt content"){
#         post{
#             title
#             content
#         }
#         }
#     }
#     """,
#     context={'is_anonymous':False}
# )

# users(limit: 2){
#     username,
#     created_at
# }

result=schema.execute(
    """
    {
        users{
        id
        createdAt
        username
        avatarUrl   
        }
    }
    """
)

# print(result.data.items())
# print(result.data['hello'])
print(json.dumps(result.data,indent=2))