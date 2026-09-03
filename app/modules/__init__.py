models = {}

def load_models():
    global models
    from .books_example.models import Book
    models['Book'] = Book
