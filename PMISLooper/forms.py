from DataBase_MPMS import forms_base as fb


class Tec_mindmap_Form(fb.Tecmindmap_Form):
    class Meta(fb.Tecmindmap_Form.Meta):
        fields = ['inc_id','parentid','sdesc']
        labels = dict((key,value) for key, value in fb.Tecmindmap_Form.Meta.labels.items() if key in
        ['inc_id','parentid','sdesc'])


class Tecmindmap_detail_Form(fb.Tecmindmapdetail_Form):
    class Meta(fb.Tecmindmapdetail_Form.Meta):
        fields = ['inc_id','mindmapid','technicid','ftime','etime']
        labels = dict((key,value) for key, value in fb.Tecmindmapdetail_Form.Meta.labels.items() if key in
        ['inc_id','mindmapid','technicid','ftime','etime'])
