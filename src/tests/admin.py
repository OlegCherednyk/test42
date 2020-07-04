from django.contrib import admin

from tests.forms import TestForm, QuestionsInlineFormSet, VariantInlineFormset, QuestionForm
from tests.models import Question, Test, Variant


class VariantInline(admin.TabularInline):
    model = Variant
    fields = ('text', 'is_correct')
    show_change_link = False
    formset = VariantInlineFormset
    extra = 0


class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test')
    list_select_related = ('test',)
    list_per_page = 5
    search_fields = ('first_name',)
    inlines = (VariantInline,)
    form = QuestionForm


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'number')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet



class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)
    form = TestForm


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
