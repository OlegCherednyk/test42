from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.base import View
import datetime

from tests.models import Test, TestResult, Question, TestResultDetail, Variant
from user_account.models import User


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
    model = User
    template_name = 'leaderboard_list.html'
    queryset = User.objects.order_by('-avr_score').all()
    paginate_by = 10
    context_object_name = 'leaderboard_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        context['title'] = "Leaderboard"
        return context


class TestRunView(View):
    PREFIX = 'answer_'

    def get(self, request, pk):
        if 'testresult' not in request.session:
            return HttpResponseNotAllowed('ERROR')

        test_result_step = request.session.get('testresult_step', 1)
        request.session['testresult_step'] = test_result_step

        question = Question.objects.filter(test__id=pk, number=test_result_step).first()

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

    def post(self, request, pk):
        if 'testresult' not in request.session:
            return HttpResponseNotAllowed('ERROR')

        test_result_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=test_result_step).first()

        variants = Variant.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('next', kwargs={'pk': pk}))

        if len(choices) == len(variants):
            messages.error(self.request, extra_tags='danger', message="ERROR: You can`t select at least all answers!")
            return redirect(reverse('next', kwargs={'pk': pk}))

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
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = test_result_step + 1
            return redirect(reverse('next', kwargs={'pk': pk}))
        else:
            del request.session['testresult']
            del request.session['testresult_step']

            current_test_result.finish()
            current_test_result.save()

            user = User.objects.get(pk=request.user.pk)
            user.last_run = current_test_result.datetime_run
            user.sum_score = float(user.sum_score) + float(current_test_result.avr_score)
            user.score()
            user.save()
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

        test_result_id = request.session.get('testresult')
        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test,
            )

        request.session['testresult'] = test_result.id

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
