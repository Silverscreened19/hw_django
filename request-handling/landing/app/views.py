from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()
counter_show['original'] = 0
counter_show['test'] = 0
counter_click['original'] = 0
counter_click['test'] = 0


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    if from_landing == 'original':
        counter_click['original'] += 1
        # print(f'кол-во переходов {counter_click}')
        return render(request, 'index.html')
    elif from_landing == 'test':
        counter_click['test'] += 1
        # print(f'кол-во переходов {counter_click}')
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'original':
        counter_show['original'] += 1
        # print(counter_show['original'])
        # print(f'количество ПОКАЗОВ {counter_show}')
        return render(request, 'landing.html')
    elif ab_test_arg == 'test':
        counter_show['test'] += 1
        # print(counter_show['test'])
        # print(f'кол-во ПОКАЗОВ {counter_show}')
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion = round(
            counter_click['test'] / counter_show['test'], 1)
    except ZeroDivisionError:
        test_conversion = 0
    try:
        original_conversion = round(
            counter_click['original'] / counter_show['original'], 1)
    except ZeroDivisionError:
        original_conversion = 0
    print(f'статистика тестового лэндинга {test_conversion}\n'
          f'статистика базового лэндинга {original_conversion}')
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })


# http://127.0.0.1:8000/landing/?ab-test-arg=test
# http://127.0.0.1:8000/landing/?ab-test-arg=original
