from django.shortcuts import render
from django.http import Http404
from .models import Entity, Officer, Intermediary, get_all_countries
from django.views.generic import TemplateView

# Create your views here.
class Index(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self, *args, **kwargs):
        context   = super(Index, self).get_context_data(*args, **kwargs)
        countries = get_all_countries()
        context   = {
            'countries': countries[0]
        }

        return context

class ResultPage(TemplateView):
    template_name = 'search/lookup.html'

    def get_context_data(self, *args, **kwargs):
        context     = super(ResultPage, self).get_context_data(*args, **kwargs)
        node_type   = self.request.GET.get('node')
        country     = self.request.GET.get('country-selected')
        entity_name = self.request.GET.get('wordsearch')
        countries   = get_all_countries()

        country_selected = (country, '')[country == 'allcountry']

        #entities that cointains that name
        entity_nodes = Entity.nodes.filter(name__icontains=entity_name).filter(countries__icontains=country_selected)

        #officers that contains that name
        officer_nodes = Officer.nodes.filter(name__icontains=entity_name).filter(countries__icontains=country_selected)

        #Intermediary that contains that name
        intermediary_nodes = Intermediary.nodes.filter(name__icontains=entity_name).filter(countries__icontains=country_selected)

        context = {
            'countries': countries[0],
            'word_searched': entity_name,
            'entities': entity_nodes,
            'officers': officer_nodes,
            'intermediaries' : intermediary_nodes,
            'country_selected': country_selected,
            'node_type': node_type
        }

        return context

def nodes(request, node_id):
    try:
        node_info = Entity.nodes.get(node_id=node_id)
        intermediaries = node_info.Intermediaries.all()
        officers = node_info.Officers.all()
        addressess = node_info.Addressess.all()
        others = node_info.Others.all()
        context = {
            'node_info': node_info,
            'intermediaries': intermediaries,
            'officers' : officers,
            'addressess' : addressess,
            'nodeType' : 'entity',
            'others' : 'others',
        }
    except Entity.DoesNotExist:
            pass
    try:
        node_info = Officer.nodes.get(node_id=node_id)
        entities = node_info.Entities.all()
        addressess = node_info.Addressess.all()
        context = {
            'node_info': node_info,
            'entities' :entities,
            'addressess': addressess,
            'nodeType': 'officer',
        }
    except Officer.DoesNotExist:
            pass

    try:
        node_info = Intermediary.nodes.get(node_id=node_id)
        context = {
            'node_info': node_info,
            'nodeType': 'intermediary',
        }
    except Intermediary.DoesNotExist:
        pass

    return render(request , 'search/nodeSearch.html', context);