from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from tests.models import Test, TestResult


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'test_list.html'
    context_object_name = 'test_list'
    login_url = reverse_lazy('login')
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        context['title'] = "Tests"
        return context


class LeaderBoardListView(ListView):
    model = TestResult
    template_name = 'leaderboard_list.html'
    paginate_by = 20
    context_object_name = 'leaderboard_list'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-avr_score')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        context['title'] = "Leaderboard"
        return context
