from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count

class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem']) #Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        amount_entry = Author.objects.annotate(count_entry=Count('entries')).order_by('-count_entry').values('username')
        self.answer2 = amount_entry.first()# TODO Какой автор имеет наибольшее количество опубликованных статей?
        self.answer3 = Entry.objects.filter(Q(tags__name='Кино') | Q(tags__name='Музыка')).distinct()  # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer4 = Author.objects.filter(gender='ж').count()  # TODO Сколько авторов женского пола зарегистрировано в системе?
        self.answer5 = Author.objects.filter(status_rule__isnull=False).count() / Author.objects.count() * 100  # TODO Какой процент авторов согласился с правилами при регистрации?
        self.answer6 = Author.objects.filter(authorprofile__stage__range=(1,5))  # TODO Какие авторы имеют стаж от 1 до 5 лет?
        max_self_age = Author.objects.aggregate(max_self_age=Max('age'))
        self.answer7 = Author.objects.filter(age=max_self_age['max_self_age'])  # TODO Какой автор имеет наибольший возраст?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()  # TODO Сколько авторов указали свой номер телефона?
        self.answer9 = Author.objects.filter(age__lte=25)  # TODO Какие авторы имеют возраст младше 25 лет?
        self.answer10 = Author.objects.annotate(count= Count('entries')).order_by('-count').values('username', 'count')  # TODO Сколько статей написано каждым автором?


        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)