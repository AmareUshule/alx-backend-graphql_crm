import graphene


class CRMQuery:
    hello = graphene.String(default_value="Hello, GraphQL!")


class Query(CRMQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
