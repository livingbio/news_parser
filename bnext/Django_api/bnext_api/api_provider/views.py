# -*- coding: utf-8 -*-

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from api_provider.models import Article, Comment, SubComment
from django.shortcuts import get_object_or_404

import json, csv
import copy
from datetime import datetime

def welcome(request):
	return HttpResponse("".join([
			"<h2>Welcome !</h3>",
			"<p>This is a crawling interface of tech-news website: <a href=\"http://www.bnext.com.tw/\">數位時代</a></p>",
			"<p>author: Chieh-En Tsai (Andy Tsai)</p>",
			"<p>contact info: athaha821216@gmail.com</p>"
		]))

# ---------------------------------------------------------------------
#	csv writer not supporting unicode by default
#	https://docs.python.org/2/library/csv.html
# ---------------------------------------------------------------------
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    
	notice: to replace \n or not ?
    """

    def __init__(self, f, fieldnames):
    	self.writer = csv.DictWriter(f, fieldnames)

    def writerow(self, row):
    	for r in row:
    		row[r] = unicode(row[r]).encode('utf-8')
    	self.writer.writerow(row)

    def writeheader(self):
    	self.writer.writeheader()

    def writerows(self, rows):
    	for row in rows:
    		self.writerow(row)

# ---------------------------------------------------------------------------
# Helper Method
# ---------------------------------------------------------------------------
def _get_model_fields(model):
	"""
	get fields list of a model
	"""
	return [field.name for field in model._meta.fields]


def _object_to_printable_dict(obj):
	"""
	convert a Article object into dict
	"""
	obj = copy.copy(obj.__dict__)
	keys = obj.keys()
	for key in keys:
		if key.startswith('_'):
			del obj[key]

	obj['post_time'] = obj['post_time'].strftime('%Y-%m-%dT%H:%M:%S')

	return obj

def _get_parent(obj):
	if obj.__class__ == Comment:
		return [obj.article]
	elif obj.__class__ == SubComment:
		return [obj.comment]
	return []


def _get_child(obj):
	if obj.__class__ == Comment:
		return obj.subcomment_set.all()
	elif obj.__class__ == Article:
		return obj.comment_set.all()
	return []

# ---------------------------------------------------------------------------
# TODO: write a views to return
# 		- comments of an article
#		- article of a comment
#		- subcomments of a comment
#		- comment of a subcomment
# ---------------------------------------------------------------------------



def basic_view(request, query_type, id, output_type):
	if query_type == 'article':
		SuperModel = Article
	elif query_type == 'comment':
		SuperModel = Comment
	elif query_type == 'subcomment':
		SuperModel = SubComment
	else:
		raise Http404("Please specify query type among [article, comment, subcomment]")

	obj = SuperModel.objects.get(pk=id)
	obj = _object_to_printable_dict(obj)
	if output_type == 'json':
		_str = json.dumps(obj, ensure_ascii=False)
		return HttpResponse(_str, content_type='application/json')
	elif output_type == 'csv':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment;filename="{}.csv"'.format(query_type+'_'+str(id))
		writer = UnicodeWriter(response, obj.keys())
		writer.writeheader()
		writer.writerow(obj)
		return response

def query_api(request, query_type):

# ---------------------------------------------------------------------------
# argument preprocessing
# ---------------------------------------------------------------------------
	query_type = query_type.encode('ascii').lower()
	if query_type == 'article':
		SuperModel = Article
	elif query_type == 'comment':
		SuperModel = Comment
	elif query_type == 'subcomment':
		SuperModel = SubComment
	else:
		raise Http404("Please specify query type among [article, comment, subcomment]")
	
	queryDict = request.GET
	includeDict = {}
	excludeDict = {}

	for key in queryDict:
		if key.startswith('ex_'):
			excludeDict[key[3:]] = queryDict[key]
		elif key.startswith('in_'):
			includeDict[key[3:]] = queryDict[key]
		else:
			includeDict[key] = queryDict[key] 		# default using include

	pool = SuperModel.objects.all()
	display_type = 'json' 							# default using json format
# ---------------------------------------------------------------------------
# first filter include, then filter exclude
# ---------------------------------------------------------------------------
	workingDict = includeDict
	filterFun = pool.filter
	flag_noMatch = True
	for i in range(2):
		if i == 1:
			workingDict = excludeDict
# ---------------------------------------------------------------------------
# start filtering, common settings
# ---------------------------------------------------------------------------
		for key in workingDict:

			if i == 0:
				filterFun = pool.filter
			else:
				filterFun = pool.exclude

			if key == 'type':
				if workingDict[key] == 'csv':
					display_type = 'csv'

			if key.startswith(u'post_time'):
				flag_noMatch = False
				operation = key[11:]
				time_info = datetime.strptime(workingDict[key], '%Y/%m/%d')
				# time_info = time_info.astimezone(timezone.now().tzinfo)
				# import pdb; pdb.set_trace()
				if operation == 'date':
					pool = filterFun(post_time__date=time_info)
				elif operation == 'date__gte':
					pool = filterFun(post_time__date__gte=time_info)
				elif operation == 'date__lte':
					pool = filterFun(post_time__date__lte=time_info)
				else:
					pass

			if key.startswith(u'fb_like'):
				flag_noMatch = False
				operation = key[9:]
				num = int(workingDict[key])
				if operation == 'gt':
					pool = filterFun(fb_like__gt=num)
				elif operation == 'gte':
					pool = filterFun(fb_like__gte=num)
				elif operation == 'lt':
					pool = filterFun(fb_like__lt=num)
				elif operation == 'lte':
					pool = filterFun(fb_like__lte=num)
				else:
					pass

			if key.startswith('content'):
				flag_noMatch = False
				operation = key[9:]
				if operation == 'exact':
					pool = filterFun(content__exact=workingDict[key])
				elif operation == 'iexact':
					pool = filterFun(content__iexact=workingDict[key])
				elif operation == 'contains':
					pool = filterFun(content__contains=workingDict[key])
				elif operation == 'icontains':
					pool = filterFun(content__icontains=workingDict[key])
				else:
					pass
# ---------------------------------------------------------------------------
# Article
# ---------------------------------------------------------------------------
			if query_type == 'article':

				if key.startswith('url'):
					flag_noMatch = False
					pool = filterFun(url__iexact=workingDict[key])

				if key.startswith('title'):
					flag_noMatch = False
					operation = key[7:]
					if operation == 'exact':
						pool = filterFun(title__exact=workingDict[key])
					elif operation == 'iexact':
						pool = filterFun(title__iexact=workingDict[key])
					elif operation == 'contains':
						pool = filterFun(title__contains=workingDict[key])
					elif operation == 'icontains':
						pool = filterFun(title__icontains=workingDict[key])
					elif operation == 'startswith':
						pool = filterFun(title__startswith=workingDict[key])
					elif operation == 'istartswith':
						pool = filterFun(title__istartswith=workingDict[key])
					elif operation == 'endswith':
						pool = filterFun(title__endswith=workingDict[key])
					elif operation == 'iendswith':
						pool = filterFun(title__iendswith=workingDict[key])
					else:
						pass

				if key.startswith('journalist'):
					flag_noMatch = False
					operation = key[12:]
					if operation == 'in':
						l = workingDict[key].split(',')
						pool = filterFun(journalist__in=l)
					elif operation == 'exact':
						pool = filterFun(journalist__exact=workingDict[key])
					elif operation == 'iexact':
						pool = filterFun(journalist__iexact=workingDict[key])
					else:
						pass

				if key.startswith('keywords'):
					flag_noMatch = False
					operation = key[10:]
					keywords = workingDict[key].split(u',')
					if operation == 'exact_and_contain':
						regex = '(?=.*'+')(?=.*'.join(keywords)+')'
						pool = filterFun(keywords__regex=ur'{}'.format(regex))
					elif operation == 'iexact_and_contain':
						regex = '(?=.*'+')(?=.*'.join(keywords)+')'
						pool = filterFun(keywords__iregex=ur'{}'.format(regex))
					elif operation == 'exact_and_match':
						regex = '(?=.*(^|,)'+'(,|$))(?=.*(^|,)'.join(keywords)+'(,|$))'
						pool = filterFun(keywords__regex=ur'{}'.format(regex))
					elif operation == 'iexact_and_match':
						regex = '(?=.*(^|,)'+'(,|$))(?=.*(^|,)'.join(keywords)+'(,|$))'
						pool = filterFun(keywords__iregex=ur'{}'.format(regex))
					elif operation == 'exact_or_contain':
						regex = '(?=.*(('+ ')|('.join(keywords) +')))'
						pool = filterFun(keywords__regex=ur'{}'.format(regex))
					elif operation == 'iexact_or_contain':
						regex = '(?=.*('+ '|'.join(keywords) +'))'
						pool = filterFun(keywords__iregex=ur'{}'.format(regex))
					elif operation == 'exact_or_match':
						regex = '(?=.*('+ '((^|,)' + '(,|$))|((^|,)'.join(keywords) + '(,|$))' + '))'
						pool = filterFun(keywords__regex=ur'{}'.format(regex))
					elif operation == 'iexact_or_match':
						regex = '(?=.*('+ '((^|,)' + '(,|$))|((^|,)'.join(keywords) + '(,|$))' + '))'
						pool = filterFun(keywords__iregex=ur'{}'.format(regex))
					else:
						pass

				if key.startswith('fb_share'):
					flag_noMatch = False
					operation = key[10:]
					num = int(workingDict[key])
					if operation == 'gt':
						pool = filterFun(fb_share__gt=num)
					elif operation == 'gte':
						pool = filterFun(fb_share__gte=num)
					elif operation == 'lt':
						pool = filterFun(fb_share__lt=num)
					elif operation == 'lte':
						pool = filterFun(fb_share__lte=num)
					else:
						pass

				if key.startswith('category'):
					flag_noMatch = False
					keywords = workingDict[key].split(u',')
					pool = filterFun(category__in=keywords)
# ---------------------------------------------------------------------------
# Comment or SubComment
# ---------------------------------------------------------------------------
			else:

				if key.startswith('actor'):
					flag_noMatch = False
					operation = key[7:]
					if operation == 'exact':
						pool = filterFun(actor__exact=workingDict[key])
					elif operation == 'iexact':
						pool = filterFun(actor__iexact=workingDict[key])
					elif operation == 'in':
						l = workingDict[key].split(u',')
						pool = filterFun(actor__in=l)
					else:
						pass

				if key.startswith('source_type'):
					flag_noMatch = False
					operation = key[13:]
					if operation == 'exact':
						pool = filterFun(source_type__exact=workingDict[key])
					elif operation == 'iexact':
						pool = filterFun(source_type__iexact=workingDict[key])
					elif operation == 'in':
						l = workingDict[key].split(u',')
						pool = filterFun(source_type__in=l)
					else:
						pass

# ---------------------------------------------------------------------------
# response
# ---------------------------------------------------------------------------

	if flag_noMatch:
		pool = []
	ret = []
	for obj in pool:
		uni = _object_to_printable_dict(obj)
		if 'get_child' in queryDict:
			uni['child'] = json.dumps([_object_to_printable_dict(_obj) for _obj in _get_child(obj)], ensure_ascii=False)
		if 'get_parent' in queryDict:
			uni['parent'] = json.dumps([_object_to_printable_dict(_obj) for _obj in _get_parent(obj)], ensure_ascii=False)
		ret.append(uni)

	if display_type == 'json':
		_str = json.dumps(ret, ensure_ascii=False)
		return HttpResponse(_str, content_type='application/json')
	elif display_type == 'csv':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment;filename="{}.csv"'.format(request.__str__())
		if len(pool) == 0:
			header = []
		else:
			header = obj[0].keys()
		writer = UnicodeWriter(response, header)
		writer.writeheader()
		for obj in pool:
			writer.writerow(obj)
		return response

