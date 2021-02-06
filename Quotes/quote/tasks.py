from celery import shared_task
from .models import QuoteOfDay,Quote
import random
@shared_task
def quote_of_day():
    quote = Quote.objects.all()
    random_quote = random.choice(list(quote.values_list('quote',flat=True)))
    quote_author = Quote.objects.get(quote=random_quote)
    qod = QuoteOfDay.objects.all()
    if len(qod)==0:
        qod = QuoteOfDay(quote=random_quote,author=quote_author.author)
        qod.save()
    else:
        qodd = QuoteOfDay.objects.all()[0]
        qodd.quote = random_quote
        qodd.author = quote_author.author.short_name
        qodd.save()
    return quote_author