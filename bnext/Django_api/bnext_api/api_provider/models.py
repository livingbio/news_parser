from __future__ import unicode_literals

from django.db import models

class Article(models.Model):
	url 			= models.CharField(max_length=500)
	title 			= models.CharField(max_length=500)
#	source_press 	= models.CharField(max_length=500) <- no source press
	post_time 		= models.DateTimeField('posting date')
	journalist		= models.CharField(max_length=500)
	content 		= models.TextField()
#	popularity 		= models.CharField(max_length=500) <- no popularity
#	compare 		= models.CharField(max_length=500) <- no compare
	keywords 		= models.CharField(max_length=500) # <- json string for keywords list
	fb_like 		= models.IntegerField()
	fb_share 		= models.IntegerField()
	category 		= models.CharField(max_length=500)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	article 		= models.ForeignKey(Article, on_delete=models.CASCADE)

	content 		= models.TextField()
	actor 			= models.CharField(max_length=500)
	fb_like 		= models.IntegerField()
#	fb_dislike		= models.IntegerField() <- no fb_dislike
	post_time 		= models.DateTimeField('posting time')
	source_type 	= models.CharField(max_length=500)

	def __str__(self):
		return self.content

	def __unicode__(self):
		return self.content

class SubComment(models.Model):
	comment 		= models.ForeignKey(Comment, on_delete=models.CASCADE)

	content 		= models.TextField()
	actor 			= models.CharField(max_length=500)
	fb_like 		= models.IntegerField()
#	fb_dislike		= models.IntegerField() <- no fb_dislike
	post_time 		= models.DateTimeField('posting time')
	source_type 	= models.CharField(max_length=500)

	def __str__(self):
		return self.content

	def __unicode__(self):
		return self.content