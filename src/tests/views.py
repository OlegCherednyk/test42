from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.base import View
import datetime

from tests.models import Test, TestResult, Question, TestResultDetail, Variant


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

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        context['title'] = "Leaderboard"
        return context


class TestRunView(View):
    PREFIX = 'answer_'

    def get(self, request, pk, seq_nr):
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        variant = [
            variant.text
            for variant in question.variants.all()
        ]
        return render(
            request=request,
            template_name='test_run.html',
            context={
                'question': question,
                'variant': variant
            }
        )

    def post(self, request, pk, seq_nr):

        test = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        variants = Variant.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))

        current_test_result = TestResult.objects.filter(
            test=test,
            user=request.user,
            is_completed=False).last()

        for idx, answer in enumerate(variants, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            return redirect(reverse('testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr+1}))
        else:
            current_test_result.finish()
            current_test_result.save()
            return render(
                request=request,
                template_name='testrun_end.html',
                context={
                    'avr_score': f'{current_test_result.avr_score:.1f}',
                    'percent': f'{current_test_result.avr_score/ test.questions_count()*100:.1f}',
                    'question_count': test.questions_count(),
                    'test_result': current_test_result,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None)
                }
            )


class StartTestView(View):

    def get(self, request, pk):
        test = Test.objects.get(pk=pk)

        test_result = TestResult.objects.create(
            user=request.user,
            test=test
        )
        num_run = test.test_results.count()
        best_result = test.test_results.order_by('-avr_score').first()
        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'num_run': num_run,
                'best_result': best_result,
                'test': test,
                'test_result': test_result
            },
        )
