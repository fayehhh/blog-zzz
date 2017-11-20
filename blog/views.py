from django.views.generic import ListView, DetailView

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Category, Tag
from comments.models import Comment
import markdown
from comments.forms import CommentForm
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
"""
render函数根据我们传入的参数来构造 HttpResponse
"""


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:

            return {}

        left = []
        right = []
        left_has_more = False

        right_has_more = False

        first = False
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


def detail(request, pk):
	post = get_object_or_404(Post, id=pk)

	post.increase_views()
	post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',
	'markdown.extensions.toc',])
	form = CommentForm()
	comment_list = post.comment_set.all().order_by("-create_time")
	context = {
		'post': post,
		'form': form,
		'comment_lit': comment_list
	}

	return render(request, 'blog/detail.html', context=context)


# def archives(request, year, month):
# 	post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
# 	return render(request, "blog/index.html", context={"post_list": post_list})
class archives(ListView):
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		context.update(pagination_data)
		return context

	def get_queryset(self, **kwargs):
		year = self.kwargs["year"]
		month = self.kwargs["month"]
		post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
		return post_list

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False

		right_has_more = False

		first = False
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number

		# 获得分页后的总页数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:

			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True

			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}

		return data


# def category(request, pk):
# 	cate = get_object_or_404(Category, pk=pk)
# 	post_list = Post.objects.filter(category=cate)
# 	return render(request, "blog/index.html", context={"post_list": post_list})
class category(ListView):
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 3

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)

		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		context.update(pagination_data)
		return context

	def get_queryset(self, **kwargs):
		pk = self.kwargs["pk"]
		cate = get_object_or_404(Category, pk=pk)
		post_list = Post.objects.filter(category=cate)
		return post_list

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False

		right_has_more = False

		first = False
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number

		# 获得分页后的总页数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:

			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True

			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}

		return data


class TagView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 3

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		context.update(pagination_data)
		return context

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False

		right_has_more = False

		first = False
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number

		# 获得分页后的总页数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:

			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True

			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}

		return data


def search(request):
	q = request.GET.get("q")
	error_msg = ""

	if not q:
		error_msg = "请输入关键词"
		return render(request, 'blog/index.html', {"error_msg": error_msg})
	post_list = Post.objects.filter(Q(title__icontains=q)|Q(excerpt__icontains=q))
	return render(request, "blog/index.html", {'error_msg': error_msg, 'post_list': post_list})


def ajax(request):
	text = ""
	if request.method == 'POST':
		user = request.POST.get('username')
		cate = Comment.objects.filter(name=user)
		if len(cate) > 0:
			text = "该名字存在！"
		else:
			text = "该名字可以使用！"
		return HttpResponse(text)
	return render(request, 'blog/detail.html')