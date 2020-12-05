from import_export import resources
from quote.models import Quote
from .models import Author
class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
class QuoteResource(resources.ModelResource):
    class Meta:
        model = Quote