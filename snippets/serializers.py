from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title',
                  'code', 'linenos', 'language', 'style', 'owner',)


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(
#         many=True, view_name='snippet-detail', 
#         queryset=Snippet.objects.all())

#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'snippets',)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail',
        queryset=Snippet.objects.all())
    # snippets = serializers.CharField()
    # snippet_code = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """ 
        print(validated_data)
        user = User.objects.create_user(validated_data['username'])
        snippet = Snippet.objects.create(code=validated_data['snippets'], owner=user)
        snippet.save()
        return user
    
