import graphene
from graphene_django import DjangoObjectType
from graphql import  GraphQLError
from django.db.models import Q
from .models import *
from users.schema import UserType


class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None):
        if search:
            filter = (
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(url__icontains=search)
            )
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Log in to add a track.')

        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()



