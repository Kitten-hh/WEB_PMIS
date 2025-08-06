from ..models import AiFollowupTbl
from django.db.models import Sum,Count,Max,Min,Avg,Q
from BaseApp.library.tools import DateTools
from time import sleep
class AiFollowService:
    def saveFollowUp(self, session, categories, user_input):
        category = categories[session['current_category_index']]
        questions = category['questions']
        if session['current_question_index'] >= len(questions)  or len(questions) == 0: ##已經問完了所有問題, 是用戶自己問題的問題暫時不記錄
            return
        else:
            followupid = session['current_topic_followup_id']
            if not followupid:
                followupid = self.get_max_followupid()
            context = session['context']
            question = context[len(context) - 1]['content']
            #如果在问子问题
            sub_question = None
            if session['in_sub_question']:
                sub_question = questions[session['current_question_index']]['sub_questions_objects'][session['current_sub_question_index']]
            main_question = questions[session['current_question_index']]['main_question']
            max_itemno = self.get_max_itemno(followupid)
            followup = AiFollowupTbl(
                followup_id = followupid, 
                item_no = max_itemno,
                category_id = category['id'],
                main_question_id=main_question.id,
                sub_question_id=None if not sub_question else sub_question.id,
                question = question,
                reply = user_input,
                create_date=DateTools.now()
            )
            save_qty = 0
            while save_qty < 15:
                try:
                    followup.save()
                    break
                except Exception as e:
                    print(str(e))
                sleep(0.09)
                if not session['current_topic_followup_id']:
                    followupid = self.get_max_followupid
                    followup.followup_id = followupid
                else:
                    max_itemno = self.get_max_followupid(followupid)
                    followup.item_no = max_itemno
                save_qty += 1            
            if not session['current_topic_followup_id']:
                session['current_topic_followup_id'] = followupid

    def get_max_followupid(self):
        '''
        功能描述：獲取最大單號
        '''
        max_followup_id = (
            AiFollowupTbl.objects.all()
            .aggregate(max_followup_id=Max('followup_id'))['max_followup_id'] or 0
        )
        return max_followup_id + 10
    
    def get_max_itemno(self, followupid):
        """
        功能描述：獲取最大單號
        參數說明:
            followupid: 跟進 ID
        """
        max_item_no = (
            AiFollowupTbl.objects.filter(followup_id=followupid)
            .aggregate(max_item_no=Max('item_no'))['max_item_no'] or 0
        )
        return max_item_no + 10
