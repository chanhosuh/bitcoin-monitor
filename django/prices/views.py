from django.views.generic import TemplateView


class TickerView(TemplateView):
    template_name = 'prices/tickers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticker_codes'] = [
            'BTCUSD',
        ]
        return context
