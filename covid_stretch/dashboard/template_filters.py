# coding=utf-8
#
# Usage: In HTML template, use {{ mydict|get_item:item.NAME }}
# See https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable


from django.template.defaulttags import register


@register.filter(name='lookup')
def lookup(value, arg):
	return value.get(arg)
