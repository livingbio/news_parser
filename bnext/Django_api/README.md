# bnext api

### Create a virtual environment
```
virtualenv venv
```
for linux-like system:
```
source venv/bin/activate
```
for windows:
```
venv\Scripts\activate.bat
```

### Install required packages
```
pip install -r requirements.txt
```

### Update database
to refresh datebase, use:
```
python manage.py crawl_all
```
crawl_all command provide --page and --category option to specify which categories and how many pages you wish to crawl. For more help, see:
```
python manage.py crawl_all -h
```

### Start Server
```
python manage.py runserver
```

### API interface
base url: http://127.0.0.1:8000/api_provider/query/<query_type>?arg1=...&arg2=...&...
display setting is for setting how the queried result should be rendered
```
============================== display setting =================================
- type:
	The type of format to return. Could be either "json" or "csv"
	default to be json
	ex: type=csv

- show_parent:
	Include "show_parent" in query argument if you wish to see the (Article/Comment)
	a queried (Comment/Subcomment) belongs to.

- show_child:
	Include "show_child" in query arguement if you wish to see the (Comments/Subcomments)
	of the queried (Article/Comment).
```
common settings are settings that are shared by <query_type> of Article, Comment, SubComment
```
============================== common setting ==================================
- content:
	- content__exact:
		Exact match of the content.
		ex: content__exact=This is an example.
	- content__iexact:
		Case-insensitive match of the content.
		ex: content__exact=tHiS iS aN eXaMpLe.
	- content__contains:
		Return all the object containing desired string in its content.
		ex: content__contains=This
			content__contains=This is a test
	- content__icontains:
		Return all the object containing desired string in its content with 
		case-insensitive matching.
		ex: content__icontains=tHiS
			content__icontains=tHiS iS a TeSt

- fb_like:
	- fb_like__gt:
		Return all objects with fb_like greater than the given number.
		ex: fb_like__gt=50 will return all the objects with more than 50 likes
	- fb_like__gte:
		Return all objects with fb_like greater than or equal to the given number.
		ex: fb_like__gte=50 will return all the objects with more than or equal to 50 likes
	- fb_like_lt:
		Return all objects with fb_like less than the given number.
		ex: fb_like__lt=50 will return all the objects with less than 50 likes
	- fb_like__lte:
		Return all objects with fb_like less than or equal to the given number.
		ex: fb_like__lte=50 will return all the objects with less than or equal to 50 likes

- post_time:
	- post_time__date:
		Return all objects posted on that given date. (UTC+08:00)
		ex: post_time__date=2016/1/28
	- post_time__date__gte:
		Return all objects posted after that given date (included).
		ex: post_time__date__gte=2016/1/28
	- post_time__date__lte:
		Return all objects posted before that given date (included).
		ex: post_time_date__gte=2016/1/28
```
the following are some <query_type> depending settings
```
============================== Article setting =================================
- url:
	- url:
		Return the article of the given url.
		ex: url=http://www.bnext.com.tw/article/view/id/38607

- title:
	- title__exact
	- title__iexact
	- title__contains
	- title__icontains
	- title__startswith
	- title__istartswith
	- title__endswith
	- title__iendswith

- journalist:
	- journalist__exact
	- journalist__iexact
	- journalist__in:
		Return all articles written by journalist in the given list, seperated by ","
		ex. journalist__in=journalistA,journalistB,journalistC

- keywords:
	/***
	 * _and_contain: need to contain all keywords, for example, if an article A have
	 * 				 keywords "apple,banana,cat"
	 *
	 * _and_contain=app,ban,ca 			will return article A
	 * _and_contain=app,ban,ca,dance 	will not return article A
	 ***/
	- keywords__exact_and_contain
	- keywords__iexact_and_contain

	/***
	 * _and_match: need to match all keywords, for example, if an article A have
	 * 			   keywords "apple,banana,cat"
	 *
	 * _and_match=apple,banana,cat 		will return article A
	 * _and_match=app,ban,ca 			will not return article A
	 * _and_match=app,ban,ca,dance 		will not return article A
	 ***/
	- keywords__exact_and_match
	- keywords__iexact_and_match

	/***
	 * _or_contain: only need to contain one keyword, for example, if an article A have
	 * 				keywords "apple,banana,cat"
	 *
	 * _or_contain=app,ban,ca 			will return article A
	 * _or_contain=app,dance 			will return article A
	 * _or_contain=dance 				will not return article A
	 ***/
	- keywords__exact_or_contain
	- keywords__iexact_or_contain

	/***
	 * _or_match: only need to match one keyword, for example, if an article A have
	 * 			  keywords "apple,banana,cat"
	 *
	 * _or_match=app,ban,ca 			will not return article A
	 * _or_match=apple,ban,ca 			will return article A
	 * _or_contain=apple,dance 			will return article A
	 ***/
	- keywords__exact_or_match
	- keywords__iexact_or_match

- fb_share:
	- fb_share__gt
	- fb_share__gte
	- fb_share__lt
	- fb_share__lte

- category:
	- category__in:
		ex: category__in=categoryA,categoryB,categoryC

============================== Comment & SubComment setting ====================
- actor:
	- actor__exact
	- actor__iexact
	- actor__in

- source_type:
	- source_type__iexact
	- source_type__in
```

