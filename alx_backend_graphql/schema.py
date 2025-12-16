import graphene


class CRMQuery:
    hello = graphene.String(default_value="Hello, GraphQL!")

from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    pass


class Mutation(CRMMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
