from django.shortcuts import render
from django.http import Http404

posts = [
    {
        'id': 0,
        'title': 'Побег из Шоушенка',
        'date': '10 декабря 2024 года',
        'category': 'thriller',
        'director': 'Фрэнк Дарабонт',
        'genre': 'Драма',
        'cast': 'Тим Роббинс, Морган Фриман, Боб Гантон',
        'text': '''Успешный банкир Энди Дюфрейн обвинён в убийстве своей жены 
                       и её любовника. Оказавшись в тюрьме Шоушенк, он сталкивается с 
                       жестокостью и несправедливостью, но находит друга в лице заключённого Реда. 
                       Вместе они преодолевают трудности, мечтая о свободе.''',

        'image': 'img/img_film/shawshank.jpg',  # Путь к картинке
        #'trailer_url': 'https://www.youtube.com/watch?v=kgAeKpAPOYk',
    },

    {
        'id': 1,
        'title': 'Интерстеллар',
        'date': '12 декабря 2024 года',
        'category': 'Science-fiction',
        'director': 'Кристофер Нолан',
        'genre': 'Научная фантастика',
        'cast': 'Мэттью МакКонахи, Энн Хэтэуэй, Джессика Честейн',
        'text': '''В будущем Земля сталкивается с экологическим кризисом. Группа исследователей 
                       отправляется через червоточину в поисках нового дома для человечества. 
                       Это эпическое путешествие через время и пространство.''',
        'image': 'img/img_film/interstelar.jpg',
        #'trailer_url': 'https://www.youtube.com/watch?v=6ybBuTETr3U',
    },
    {
        'id': 2,
        'title': 'Дюна 2',
        'date': '15 декабря 2024 года',
        'category': 'Science-fiction',
        'director': 'Дени Вильнёв',
        'genre': 'Научная фантастика',
        'cast': 'Тимоти Шаламе, Зендея, Оскар Айзек',
        'text': '''Продолжение эпической саги о выживании и борьбе за контроль над планетой Арракис. 
                   Действие фильма разворачивается в мире, где борьба за ресурсы становится вопросом жизни и смерти.''',
        'image': 'img/img_film/duna.png',  # Путь к картинке для Дюны 2
        #'trailer_url': 'https://www.youtube.com/watch?v=U2Qp5pL3ovA',
    },
]

posts_dict = {post['id']: post for post in posts}

def index(request):
    template = 'cinema/index.html'
    context = {'index': posts[::-1]}
    return render(request, template, context)


def post_detail(request, id):

    if id not in posts_dict.keys():
        raise Http404(f'Фильм с id {id} не существует')
    
    template = 'cinema/detail.html'
    context = {'post': posts_dict[id]}

    return render(request, template, context)


def category_posts(request, category_slug):
    # template = 'cinema/category.html'
    # context = {'category_slug': category_slug}
    # return render(request, template, context)
    filtered_movies = [post for post in posts if post['category'] == category_slug]

    if not filtered_movies:
        raise Http404(f'Фильмы категории "{category_slug}" не найдены')

    template = 'cinema/category.html'
    context = {'movies': filtered_movies, 'category_slug': category_slug}
    return render(request, template, context)
