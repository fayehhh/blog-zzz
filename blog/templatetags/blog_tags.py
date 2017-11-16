from django.db.models.aggregates import Count

from ..models import Post, Category, Tag
from django import template

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by("-create_time")[:num]


@register.simple_tag
def archives():
	return Post.objects.dates('create_time', 'month', order='DESC')  # dates 方法会返回一个列表，列表中的元素为每一篇
# 文章（Post）的创建时间，且是 Python 的 date 对象，精确到月份，降序排列


@register.simple_tag
def get_categories():
	# 记得在顶部引入 count 函数
	# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称,filter把文章为0的分类去掉
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# 获取每个分类的文章数的方法
# @register.simple_tag
# def get_category():
# 	dict1 = {}
# 	category = Category.objects.all()
# 	for i in category:
# 		o = Post.objects.filter(category=i)
# 		dict1[i] = len(o)
# 	# print(dict1)
# 	return dict1
 # get_recent_posts as recent_post_list %}
	# for post in recent_post_list %}

# @register.simple_tag
# def count():
# 	category = Category.objects.all()
# 	list1 = []
# 	for i in category:
# 		category = Post.objects.filter(category=i)
# 		list1.append(len(category))
# 	return list1

# tag_list = Tag.objects.annotate(num_posts=Count('post'))


@register.simple_tag
def get_tags():
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)