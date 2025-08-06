from BaseApp.library.tools import DateTools

def getCurPeriod():
    period = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))    
    return period