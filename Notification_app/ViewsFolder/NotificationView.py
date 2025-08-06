from Notification_app.models import Ntfymessage, Messagecategory
from django.http import JsonResponse,HttpRequest
from django.db.models import Count, Subquery, OuterRef, Q, Case, When, IntegerField
from BaseApp.library.tools import DateTools
from django.utils.dateparse import parse_datetime
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
    
def getDate(request:HttpRequest):
    dateObj = DateTools.now().date()
    dateStr = request.GET.get("date","")
    try:
        dateObj = DateTools.parsef(dateStr, '%Y-%m-%d')
    except Exception as e:
        pass
    return dateObj    

def mesg_summary(request: HttpRequest):
    contact = request.GET.get("contact","")
    targetDate = getDate(request)
    
    queryset = queryset = (
        #Ntfymessage.objects.filter(receiver=contact, sent_time__date = targetDate)
        Ntfymessage.objects.extra(where=["id IN (SELECT id FROM V_NtfyMessage_Redup WHERE receiver = %s AND cast(sent_time as Date)=%s)"], params=[contact, targetDate])
        .values('category_id')
        .annotate(num=Count('id'))
        .annotate(category_name=Subquery(
            Messagecategory.objects.filter(id=OuterRef('category_id')).values('category_name')[:1]
        ))
        .values('category_name', 'category_id', 'num')
    )
    queryset_list = list(queryset)
    for item in queryset_list:
        if item.get('category_id',0)==10:
            new_count = queryset.filter(category_id='10').aggregate(
                num=Count(Case(
                    When(msg_createdate__date=targetDate, then='id'),
                    default=None,
                    output_field=IntegerField()
                ))
            )['num']
            item['num'] = new_count
    return JsonResponse(queryset_list, safe=False)

def get_message_list(request: HttpRequest):
    contact = request.GET.get("contact","")
    category_id = request.GET.get("category_id","")
    targetDate = getDate(request)
    #queryset = Ntfymessage.objects.filter(receiver = contact, category_id = category_id, sent_time__date = targetDate)
    if category_id == '10':
        queryset = Ntfymessage.objects.filter(category_id = category_id, msg_createdate__date = targetDate).extra(where=["id IN (SELECT id FROM V_NtfyMessage_Redup WHERE receiver = %s AND cast(msg_createdate as Date)=%s)"], params=[contact, targetDate])
    else:
        queryset = Ntfymessage.objects.filter(category_id = category_id).extra(where=["id IN (SELECT id FROM V_NtfyMessage_Redup WHERE receiver = %s AND cast(sent_time as Date)=%s)"], params=[contact, targetDate])

    return JsonResponse(list(queryset.values()), safe=False)

class DetailMessageTableView(DatatablesServerSideView):
    model = Ntfymessage
    columns = "__all__"

    def get_initial_queryset(self):
        contact = self.request.GET.get('contact', '')    
        category_id = self.request.GET.get('category_id', '')    
        targetDate = getDate(self.request)
        RID = self.request.GET.get('RID', '')    
        search_contact = self.request.GET.get('search_contact', '')
        search_date = self.request.GET.get('search_date', '')
        queryset = Ntfymessage.objects.all()
        if contact and targetDate:
            queryset = Ntfymessage.objects.extra(where=["id IN (SELECT id FROM V_NtfyMessage_Redup WHERE receiver = %s AND cast(sent_time as Date)=%s)"], params=[contact, targetDate])    
        if category_id == '10':
            queryset = Ntfymessage.objects.filter(category_id = category_id, msg_createdate__date = targetDate).extra(where=["id IN (SELECT id FROM V_NtfyMessage_Redup WHERE receiver = %s AND cast(sent_time as Date)=%s)"], params=[contact, targetDate])
        
        # 处理日期参数
        if search_date:
            date = DateTools.parsef(search_date, '%Y-%m-%d')  # 解析日期字符串
            if date:
                queryset = queryset.filter(sent_time__date=date)
        q = Q()
        if RID:
            q &= Q(message__contains=RID)
        if search_contact:
            q &= Q(title__contains=search_contact)
        if category_id:
            q &= Q(category_id=category_id)
            
        return queryset.filter(q)