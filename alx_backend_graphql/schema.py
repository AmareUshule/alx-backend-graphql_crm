import graphene


#class CRMQuery:
   # hello = graphene.String(default_value="Hello, GraphQL!")

from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    pass


class Mutation(CRMMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
import crm.schema

class Query(crm.schema.Query, graphene.ObjectType):
    # This will inherit queries from crm app
    pass

class Mutation(crm.schema.Mutation, graphene.ObjectType):
    # This will inherit mutations from crm app
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
