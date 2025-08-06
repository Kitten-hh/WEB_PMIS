from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from ..models import Aisummaryrecord

class UpdateAiSummaryRecordView(SWUpdateView):
    model = Aisummaryrecord

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("review_isempty","false") == "true":
            local = request.POST.copy()
            local['review'] = ""
            request.POST = local
        return super(UpdateAiSummaryRecordView, self).post(request, *args, **kwargs)
