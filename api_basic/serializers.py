from rest_framework import serializers
from .models import Article


# Example 1: Use serializer

# class ArticleSerializer(serializers.Serializer):
#     title =serializers.CharField(max_length=100)
#     author=serializers.CharField(max_length=100)
#     email=serializers.CharField(max_length=100)
#     date =serializers.DateTimeField()

#     def create(self,validated_data):
#         return Article.objects.create(validated_data)

#     def update(self, instance, validated_data):
#         instance.title=validated_data.get('title',instance.title)
#         instance.author=validated_data.get('author',instance.author)
#         instance.email=validated_data.get('email',instance.email)
#         instance.date=validated_data.get('date',instance.date)
#         instance.save()
#         return instance
#         # return super().update(instance, validated_data)

#  Example 2: Use serializer model (This should have the same function as example 1)
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article

        # specified catagory of fields
        # fields =['id','title','author']

        # if we want to display all the fields we can use __all__:
        fields = '__all__'


