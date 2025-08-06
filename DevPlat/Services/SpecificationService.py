from DataBase_MPMS.models import Docma,Docmb

class SpecificationService(object):

    @staticmethod
    def get_max_verno(spec_no:str):
        '''
        功能描述:根據程序編號,獲取最大版本號
        '''
        qs = Docma.objects.values('ma002').filter(ma001=spec_no).order_by('-ma002')[:1]
        if len(qs) > 0:
            return str(int(qs[0]['ma002']) + 1).rjust(5,'0')
        else:
            return '00001'

