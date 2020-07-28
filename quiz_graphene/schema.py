import graphene
from quiz.schema import Query, Mutation, schema

class Query(Query, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
