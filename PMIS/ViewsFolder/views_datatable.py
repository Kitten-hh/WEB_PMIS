from __future__ import absolute_import, unicode_literals
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
import six
from DataBase_MPMS import models
import json

DATATABLES_SERVERSIDE_MAX_COLUMNS = 30

class Column(object):
    def __init__(self, model_field, allow_choices_lookup=True):
        self.name = model_field.name
        choices = model_field.choices

        if allow_choices_lookup and choices:
            self._choices_lookup = self.parse_choices(choices)
            self._search_choices_lookup =\
                {v: k for k, v in six.iteritems(self._choices_lookup)}
            self._allow_choices_lookup = True
        else:
            self._allow_choices_lookup = False

    @property
    def has_choices_available(self):
        return self._allow_choices_lookup

    def get_field_search_path(self):
        return self.name

    def parse_choices(self, choices):
        choices_dict = {}

        for choice in choices:
            try:
                choices_dict[choice[0]] = choice[1]
            except IndexError:
                choices_dict[choice[0]] = choice[0]
            except UnicodeDecodeError:
                choices_dict[choice[0]] = choice[1].decode('utf-8')

        return choices_dict

    def render_column(self, obj):
        value = getattr(obj, self.name)

        if self._allow_choices_lookup:
            return self._choices_lookup[value]

        return value

    def search_in_choices(self, value):
        if not self._allow_choices_lookup:
            return []
        return [matching_value for key, matching_value in six.iteritems(
            self._search_choices_lookup) if key.startswith(value)]


class DatatablesServerSideView(View):
    columns = []
    searchable_columns = []
    model = None

    def __init__(self, *args, **kwargs):
        super(DatatablesServerSideView, self).__init__(*args, **kwargs)
        fields = {f.name: f for f in self.model._meta.get_fields()}

        model_columns = {}
        for col_name in self.columns:
            new_column = Column(fields[col_name])
            model_columns[col_name] = new_column

        self._model_columns = model_columns

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        try:
            params = self.read_parameters(request.GET)
        except ValueError:
            return HttpResponseBadRequest()

        # Prepare the queryset and apply the search and order filters
        qs = self.get_initial_queryset()

        if 'search_value' in params:
            qs = self.filter_queryset(params['search_value'], qs)

        '''if len(params['orders']):
            qs = qs.order_by(
                *[order.get_order_mode() for order in params['orders']])'''

        paginator = Paginator(qs, params['length'])
        return HttpResponse(
            json.dumps(
                self.get_response_dict(paginator, params['draw'],
                                       params['start']),
                cls=DjangoJSONEncoder
            ),
            content_type="application/json")

    def read_parameters(self, query_dict):
        """ Converts and cleans up the GET parameters. """
        params = {field: int(query_dict[field]) for field
                  in ['draw', 'start', 'length']}

        search_value = query_dict.get('search[value]')
        if search_value:
            params['search_value'] = search_value

        return params

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        return self._model_columns[column].render_column(row)

    def prepare_results(self, qs):
        json_data = []

        for cur_object in qs:
            retdict = {fieldname: self.render_column(cur_object, fieldname)
                       for fieldname in self.columns}
            self.customize_row(retdict, cur_object)
            json_data.append(retdict)
        return json_data

    def get_response_dict(self, paginator, draw_idx, start_pos):
        page_id = (start_pos // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        objects = self.prepare_results(paginator.page(page_id))
        return {"draw": draw_idx,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": objects}

    def customize_row(self, row, obj):
        pass

    def filter_queryset(self, search_value, qs):
        search_filters = Q()
        for col in self.searchable_columns:
            model_column = self._model_columns[col]

            if model_column.has_choices_available:
                search_filters |=\
                    Q(**{col + '__in': model_column.search_in_choices(
                        search_value)})
            else:
                query_param_name = model_column.get_field_search_path()

                search_filters |=\
                    Q(**{query_param_name+'__istartswith': search_value})

        return qs.filter(search_filters)

class Task_Datatable_Demo(DatatablesServerSideView):
    model = models.VTask
    columns = ['taskno','task','contact','planbdate','planedate','progress']
    searchable_columns = columns