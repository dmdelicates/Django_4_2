from django.contrib import admin
from django.forms import BaseInlineFormSet
from .models import Article, TagTable, Scope
from django.core.exceptions import ValidationError




@admin.register(TagTable)
class TagAdmin(admin.ModelAdmin):
    pass


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            # if not form.cleaned_data['is_main']:
            #     raise ValidationError('Укажите основной раздел ')
            if 'is_main' in form.cleaned_data and form.cleaned_data['is_main']:
                counter += 1
            # print(form.cleaned_data['is_main'])
             # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if counter == 0:
            raise ValidationError('Укажите основной раздел')
        elif counter > 1:
            raise ValidationError('Основной раздел может быть только один')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleTagInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTagInline, ]
