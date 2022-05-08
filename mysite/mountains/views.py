import asyncio

from cart.forms import CartAddEquipmentForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import UpdateView
from telegrambot.bot import bot


from .filters import EquipmentFilter
from .forms import ChangeUserInfoForm, RegisterUserForm, CommentForm, WishesForm, SendForm
from .models import AdvUser, Category, Subcategory, Equipment, Brand, Post, Comment, Store, City, Wishes, \
    EquipmentStatistic

from telethon import TelegramClient

# ----------------------------------------------------------------------------------------------------------------------


def main_page(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    api_id = 16404765
    api_hash = '53d981575513ea76fc69e734a161387d'

    if request.method == 'POST':
        if request.POST.get('Send'):
            phone = request.POST.get('phone')
            name = request.POST.get('name')

            client = TelegramClient('me', api_id, api_hash)

            async def main():
                await client.send_message(phone, f" Hello, {name}!")

            with client:
                client.loop.run_until_complete(main())

    return render(request, 'main_page.html')


class UserLoginView(LoginView):
    template_name = 'login.html'

from django.db.models import Q, Count


@login_required
def profile(request):


    user = request.user
    wish, created = Wishes.objects.get_or_create(user=user)
    context = {"wish": wish}
    return render(request, 'profile.html', context)


def wish_remove(request):
    user = request.user
    Wishes.objects.get(user=user).delete()
    return render(request, 'profile.html')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = '/accounts/profile/'
    success_message = 'Ваши данные успешно изменены!'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = '/accounts/profile/'
    success_message = 'Пароль пользователя изменен'


def registration(request):
    form = RegisterUserForm()
    context = {'form': form}
    if request.method == 'POST':
        if request.POST:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user_email = request.POST.get('email')
                user = form.save()
                # group = Group.objects.get(name='Newcomer')
                # user.groups.add(group)
                # user.save()
                if user:
                    subject = 'Registration'
                    massage = f'Hello {user.username}! Нou have successfully registered! ' \
                              f' Follow the link to enter the site: http://127.0.0.1:8000/accounts/login/'
                    from_email = settings.EMAIL_HOST_USER
                    to = user_email
                    send_mail(subject, massage, from_email, [to])
                return redirect('/accounts/profile/')
            else:
                error = form.errors
                context = {"form": form, "error": error}

    return render(request, 'user_register.html', context)


class UserLogoutview(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'


# ----------------------------------------------------------------------------------------------------------------------


def all_categories(request):
    categories = Category.objects.all()
    # print(categories.query)
    f = EquipmentFilter(request.GET, queryset=Equipment.objects.all())
    popular = EquipmentStatistic.objects.filter(date=timezone.now() - timezone.timedelta(3)).order_by('-views')[:5]
    if request.session.get('seen'):
        seen = request.session['seen']
        seen_equipments = Equipment.objects.filter(id__in=seen)
        context = {"categories": categories, 'filter': f, "popular": popular, 'seen_equipments': seen_equipments}
    else:
        context = {"categories": categories, 'filter': f, "popular": popular}
    return render(request, 'all_categories.html', context)


def subcategories(request, pk):
    # q = Q(title='Tents') | Q(title='Skiing')
    # s = Subcategory.objects.filter(q)
    # print(s)
    # for a in s:
    #     print(a.title)

    subcategories = Subcategory.objects.filter(category=pk)
    context = {"subcategories": subcategories}
    return render(request, 'subcategories.html', context)


def subcategory_equipment(request, pk):
    equipments = Equipment.objects.filter(subcategory=pk)
    context = {"equipments": equipments}
    return render(request, 'subcategory_equipment.html', context)


def detail_equipment(request, pk):
    equipment = Equipment.objects.select_related().get(pk=pk)

    equipment_id = str(equipment.id)
    if request.session.get('seen'):
        seen = request.session['seen']
        if equipment_id in request.session['seen']:
            print('есть')
        else:
            seen.append(str(equipment.id))
            print(seen, 'добавлено')
    else:
        seen = request.session['seen'] = []
        seen.append(str(equipment.id))
        print(seen, 'создано и добавлено')
    request.session.save()
    # request.session.modified = True
    brand = Brand.objects.filter(pk=pk)
    stores = Store.objects.filter(equipments=pk)
    cities = City.objects.filter(pk=pk)
    comments = Comment.objects.filter(equipment=pk)
    form = CommentForm()
    wishform = WishesForm()
    user = request.user
    cart_equipment_form = CartAddEquipmentForm()
    obj, created = EquipmentStatistic.objects.get_or_create(equipment=equipment,
                                                            date=timezone.now() - timezone.timedelta(1))
    obj.views += 1
    obj.save()

    context = {"equipment": equipment, "brand": brand, 'stores': stores, "cities": cities, "form": form,
               "cart_equipment_form": cart_equipment_form, "comments": comments, "wishform": wishform}

    if request.method == 'POST':

        if request.POST.get('Add to wishes'):
            wish, created = Wishes.objects.get_or_create(user=user)
            wish.equipments.add(equipment)
            wish.save()

        if user.is_authenticated:
            if request.POST.get('text'):
                comment = Comment.objects.create(user=user, text=request.POST.get('text'))
                equipment.comments.add(comment)
        else:
            return redirect('/accounts/login/')

    return render(request, 'detail_equipment.html', context)


# ----------------------------------------------------------------------------------------------------------------------


def all_posts(request):
    posts = Post.objects.exclude(title='About us')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {"page": page, "page_obj": page_obj}

    return render(request, 'all_posts.html', context)


def post_details(request, pk):
    form = CommentForm()
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=pk)
    b = Post.objects.aggregate(count_comments=Count('comments'))
    print(b)
    a = Post.objects.annotate(count_comments=Count('comments'))
    for i in a:
        print(i.title, i.count_comments)
    paginator = Paginator(comments, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    user = request.user

    context = {"form": form, "post": post, "page": page, "page_obj": page_obj}
    if request.method == 'POST':
        if user.is_authenticated:
            comment = Comment.objects.create(user=user, text=request.POST.get('text'))
            post.comments.add(comment)
        else:
            return redirect('/accounts/login/')

    return render(request, 'post_details.html', context)


# ----------------------------------------------------------------------------------------------------------------------


CHANNEL_ID = '-100743045696'


def send_tele(request):
    form = SendForm()
    if request.POST.get('send'):
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        send = f"{phone}, Hello {name}!"
        bot.send_message(chat_id=CHANNEL_ID, text=send)
    context = {"form": form}
    return render(request, 'send.html', context)


# ----------------------------------------------------------------------------------------------------------------------




