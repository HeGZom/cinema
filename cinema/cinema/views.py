# from django.shortcuts import render
# from django.http import Http404
#
# posts = [
#     {
#         'id': 0,
#         'title': 'Побег из Шоушенка',
#         'date': '10 декабря 2024 года',
#         'category': 'thriller',
#         'director': 'Фрэнк Дарабонт',
#         'genre': 'Драма',
#         'cast': 'Тим Роббинс, Морган Фриман, Боб Гантон',
#         'text': '''Успешный банкир Энди Дюфрейн обвинён в убийстве своей жены
#                        и её любовника. Оказавшись в тюрьме Шоушенк, он сталкивается с
#                        жестокостью и несправедливостью, но находит друга в лице заключённого Реда.
#                        Вместе они преодолевают трудности, мечтая о свободе.''',
#
#         'image': 'img/img_film/shawshank.jpg',  # Путь к картинке
#         #'trailer_url': 'https://www.youtube.com/watch?v=kgAeKpAPOYk',
#     },
#
#     {
#         'id': 1,
#         'title': 'Интерстеллар',
#         'date': '12 декабря 2024 года',
#         'category': 'Science-fiction',
#         'director': 'Кристофер Нолан',
#         'genre': 'Научная фантастика',
#         'cast': 'Мэттью МакКонахи, Энн Хэтэуэй, Джессика Честейн',
#         'text': '''В будущем Земля сталкивается с экологическим кризисом. Группа исследователей
#                        отправляется через червоточину в поисках нового дома для человечества.
#                        Это эпическое путешествие через время и пространство.''',
#         'image': 'img/img_film/interstelar.jpg',
#         #'trailer_url': 'https://www.youtube.com/watch?v=6ybBuTETr3U',
#     },
#     {
#         'id': 2,
#         'title': 'Дюна 2',
#         'date': '15 декабря 2024 года',
#         'category': 'Science-fiction',
#         'director': 'Дени Вильнёв',
#         'genre': 'Научная фантастика',
#         'cast': 'Тимоти Шаламе, Зендея, Оскар Айзек',
#         'text': '''Продолжение эпической саги о выживании и борьбе за контроль над планетой Арракис.
#                    Действие фильма разворачивается в мире, где борьба за ресурсы становится вопросом жизни и смерти.''',
#         'image': 'img/img_film/duna.png',  # Путь к картинке для Дюны 2
#         #'trailer_url': 'https://www.youtube.com/watch?v=U2Qp5pL3ovA',
#     },
# ]
#
# posts_dict = {post['id']: post for post in posts}
#
# def index(request):
#     template = 'cinema/index.html'
#     context = {'index': posts[::-1]}
#     return render(request, template, context)
#
#
# def post_detail(request, id):
#
#     if id not in posts_dict.keys():
#         raise Http404(f'Фильм с id {id} не существует')
#
#     template = 'cinema/detail.html'
#     context = {'post': posts_dict[id]}
#
#     return render(request, template, context)
#
#
# def category_posts(request, category_slug):
#     # template = 'cinema/category.html'
#     # context = {'category_slug': category_slug}
#     # return render(request, template, context)
#     filtered_movies = [post for post in posts if post['category'] == category_slug]
#
#     if not filtered_movies:
#         raise Http404(f'Фильмы категории "{category_slug}" не найдены')
#
#     template = 'cinema/category.html'
#     context = {'movies': filtered_movies, 'category_slug': category_slug}
#     return render(request, template, context)

#################################################################################################################3
# from django.contrib.auth import get_user_model
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, Http404
# from django.utils.timezone import now
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import ListView, TemplateView, UpdateView, DetailView
# from .models import Session, isReservation, Seat
#
# from django.db.models import Q, Case, When
# from django.shortcuts import get_object_or_404, redirect, reverse
# from django.views.decorators.http import require_POST
#
# from .forms import UserUpdateForm, ReservationCreateForm, MovieForm, SessionForm
#
# User = get_user_model()
#
#
# class SessionListView(ListView):
#     model = Session
#     template_name = 'cinema/session_list.html'
#     context_object_name = 'sessions'
#     paginate_by = 8
#
#     def get_queryset(self):
#         return (Session.objects.filter(start_time__gte=now())
#                 .order_by('start_time')
#                 .select_related('movie', 'hall')
#                 .prefetch_related('seats'))
#
#
# class SessionDetailView(DetailView):
#     model = Session
#     template_name = 'cinema/session_detail.html'
#     context_object_name = 'session'
#
#     def get_object(self):
#         return get_object_or_404(Session, id=self.kwargs['session_id'])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         session = self.get_object()
#
#         # Создаем форму бронирования
#         form = ReservationCreateForm(session=session, user=self.request.user)
#
#         # Добавляем форму в контекст
#         context['form'] = form
#         return context
#
#     def post(self, request, *args, **kwargs):
#         session = self.get_object()
#         seat_id = request.POST.get('seat')  # Получаем ID выбранного места
#         seat = get_object_or_404(Seat, id=seat_id, session=session)
#
#         # Проверяем, свободно ли место
#         if seat.is_reserved:
#             return render(request, self.template_name, {
#                 'session': session,
#                 'form': ReservationCreateForm(session=session, user=request.user),
#                 'error_message': "Это место уже забронировано."
#             })
#
#         # Создаем бронирование
#         reservation = isReservation.objects.create(
#             session=session,
#             user=request.user,
#             seat=seat,
#             status='PENDING'
#         )
#
#         # Изменяем статус места на занятое
#         seat.is_reserved = True
#         seat.save()
#
#         # Перенаправляем пользователя на страницу профиля
#         return redirect('cinema:profile', username=request.user.username)
#
#
# class ProfileView(TemplateView):
#     template_name = 'cinema/profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs['username']
#         user = get_object_or_404(get_user_model(), username=username)
#         context['profile'] = user
#
#         if user.groups.filter(name='Admin').exists():
#             role = 'Администратор'
#         elif user.groups.filter(name='Cashier').exists():
#             role = 'Кассир'
#         else:
#             role = 'Зритель'
#
#         context['role'] = role
#
#         if role == 'Кассир':
#             # Для кассира добавляем пользователя в запрос
#             user_reservations = (
#                 isReservation.objects.select_related('session', 'seat', 'session__movie', 'user')
#                 .order_by(
#                     Case(
#                         When(status='PENDING', then=0),
#                         When(status='CONFIRMED', then=1),
#                         When(status='CANCELLED', then=2),
#                         default=3,
#                     )
#                 )
#             )
#         elif role == 'Зритель':
#             user_reservations = (
#                 isReservation.objects.filter(user=user)
#                 .select_related('session', 'seat', 'session__movie')
#             )
#         else:
#             user_reservations = None
#
#         context['user_reservations'] = user_reservations
#         return context
#
#
# class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = get_user_model()
#     form_class = UserUpdateForm
#     template_name = 'cinema/user.html'
#
#     def test_func(self):
#         return self.request.user.id == self.get_object().id
#
#     def handle_no_permission(self):
#         user = self.get_object()
#         return redirect('cinema:profile', username=user.username)
#
#     def get_success_url(self):
#         context = self.get_context_data()
#         user = context['user']
#         user_username = user.username
#         return reverse('cinema:profile', kwargs={'username': user_username})
#
#
# @login_required
# @require_POST
# def update_reservation_status(request, pk):
#     reservation = get_object_or_404(isReservation, pk=pk)
#     if request.user.groups.filter(name='Cashier').exists():
#         status = request.POST.get('status')
#         if status in dict(isReservation.STATUS_CHOICES):
#             reservation.status = status
#             reservation.save()
#     return redirect('cinema:profile', username=request.user.username)
#
#
# @login_required
# def add_movie(request):
#     if not request.user.groups.filter(name='Admin').exists():
#         raise Http404("У вас нет прав для доступа к этой странице.")
#
#     if request.method == 'POST':
#         form = MovieForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('cinema:profile', username=request.user.username)
#     else:
#         form = MovieForm()
#
#     return render(request, 'cinema/add_movie.html', {'form': form})
#
#
# @login_required
# def add_session(request):
#     if not request.user.groups.filter(name='Admin').exists():
#         raise Http404("У вас нет прав для доступа к этой странице.")
#
#     if request.method == 'POST':
#         form = SessionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cinema:profile', username=request.user.username)
#     else:
#         form = SessionForm()
#
#     return render(request, 'cinema/add_session.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView, UpdateView, DetailView
from django.db.models import Q, Case, When
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm, ReservationCreateForm, MovieForm, SessionForm
from .models import Session, isReservation, Seat

# Статические данные о фильмах
posts = [
    {
        'id': 2,
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
        'image': 'img/img_film/shawshank.jpg',
        'session_id': 2,  # Добавьте ID сеанса
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
        'session_id': 1,  # Добавьте ID сеанса
    },
    {
        'id': 0,
        'title': 'Дюна 2',
        'date': '15 декабря 2024 года',
        'category': 'Science-fiction',
        'director': 'Дени Вильнёв',
        'genre': 'Научная фантастика',
        'cast': 'Тимоти Шаламе, Зендея, Оскар Айзек',
        'text': '''Продолжение эпической саги о выживании и борьбе за контроль над планетой Арракис.
                   Действие фильма разворачивается в мире, где борьба за ресурсы становится вопросом жизни и смерти.''',
        'image': 'img/img_film/duna.png',
        'session_id': 0,  # Добавьте ID сеанса
    },
]

posts_dict = {post['id']: post for post in posts}

# Представления для статических данных
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
    filtered_movies = [post for post in posts if post['category'] == category_slug]
    if not filtered_movies:
        raise Http404(f'Фильмы категории "{category_slug}" не найдены')
    template = 'cinema/category.html'
    context = {'movies': filtered_movies, 'category_slug': category_slug}
    return render(request, template, context)

# Представления для работы с сеансами и бронированиями
class SessionListView(ListView):
    model = Session
    template_name = 'cinema/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 8

    def get_queryset(self):
        return (Session.objects.filter(start_time__gte=now())
                .order_by('start_time')
                .select_related('movie', 'hall')
                .prefetch_related('seats'))

class SessionDetailView(DetailView):
    model = Session
    template_name = 'cinema/session_detail.html'
    context_object_name = 'session'

    def get_object(self):
        return get_object_or_404(Session, id=self.kwargs['session_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.get_object()
        form = ReservationCreateForm(session=session, user=self.request.user)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        session = self.get_object()
        seat_id = request.POST.get('seat')
        seat = get_object_or_404(Seat, id=seat_id, session=session)

        if seat.is_reserved:
            return render(request, self.template_name, {
                'session': session,
                'form': ReservationCreateForm(session=session, user=request.user),
                'error_message': "Это место уже забронировано."
            })

        reservation = isReservation.objects.create(
            session=session,
            user=request.user,
            seat=seat,
            status='PENDING'
        )

        seat.is_reserved = True
        seat.save()
        return redirect('cinema:profile', username=request.user.username)

class ProfileView(TemplateView):
    template_name = 'cinema/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = get_object_or_404(get_user_model(), username=username)
        context['profile'] = user

        if user.groups.filter(name='Admin').exists():
            role = 'Администратор'
        elif user.groups.filter(name='Cashier').exists():
            role = 'Кассир'
        else:
            role = 'Зритель'

        context['role'] = role

        if role == 'Кассир':
            user_reservations = (
                isReservation.objects.select_related('session', 'seat', 'session__movie', 'user')
                .order_by(
                    Case(
                        When(status='PENDING', then=0),
                        When(status='CONFIRMED', then=1),
                        When(status='CANCELLED', then=2),
                        default=3,
                    )
                )
            )
        elif role == 'Зритель':
            user_reservations = (
                isReservation.objects.filter(user=user)
                .select_related('session', 'seat', 'session__movie')
            )
        else:
            user_reservations = None

        context['user_reservations'] = user_reservations
        return context

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'cinema/user.html'

    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        user = self.get_object()
        return redirect('cinema:profile', username=user.username)

    def get_success_url(self):
        context = self.get_context_data()
        user = context['user']
        user_username = user.username
        return reverse('cinema:profile', kwargs={'username': user_username})

@login_required
@require_POST
def update_reservation_status(request, pk):
    reservation = get_object_or_404(isReservation, pk=pk)
    if request.user.groups.filter(name='Cashier').exists():
        status = request.POST.get('status')
        if status in dict(isReservation.STATUS_CHOICES):
            reservation.status = status
            reservation.save()
    return redirect('cinema:profile', username=request.user.username)

@login_required
def add_movie(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise Http404("У вас нет прав для доступа к этой странице.")

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cinema:profile', username=request.user.username)
    else:
        form = MovieForm()
    return render(request, 'cinema/add_movie.html', {'form': form})

@login_required
def add_session(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise Http404("У вас нет прав для доступа к этой странице.")

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema:profile', username=request.user.username)
    else:
        form = SessionForm()
    return render(request, 'cinema/add_session.html', {'form': form})