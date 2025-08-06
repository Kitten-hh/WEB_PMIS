from django.db import models

# Create your models here.


class VSalesCustomerShipmentprogress(models.Model):
    custno = models.CharField(db_column='CustNo', max_length=10)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    orders = models.FloatField(db_column='Orders', blank=True, null=True)  # Field name made lowercase.
    shipment = models.FloatField(db_column='Shipment', blank=True, null=True)  # Field name made lowercase.
    progress = models.IntegerField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Customer_ShipmentProgress'


class VSalesWeeklyNeworder(models.Model):
    orderno = models.CharField(db_column='OrderNo', max_length=16)  # Field name made lowercase.
    orders = models.FloatField(db_column='Orders', blank=True, null=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CustNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=22, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.CharField(db_column='OrderDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reqdate = models.CharField(db_column='ReqDate', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Weekly_NewOrder'


class VSalesWeeklyShipment(models.Model):
    shipno = models.CharField(db_column='ShipNo',primary_key=True, max_length=16)  # Field name made lowercase.
    custno = models.CharField(db_column='CustNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=22, blank=True, null=True)  # Field name made lowercase.
    shipdate = models.CharField(db_column='Shipdate', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Weekly_Shipment'


class VSalesCustAnalysis(models.Model):
    custno = models.CharField(db_column='CustNo', primary_key = True, max_length=10)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tyorders = models.FloatField(db_column='TYOrders', blank=True, null=True)  # Field name made lowercase.
    lyorders = models.FloatField(db_column='LYOrders', blank=True, null=True)  # Field name made lowercase.
    increase = models.IntegerField(db_column='Increase', blank=True, null=True)  # Field name made lowercase.
    stype = models.CharField(db_column='SType', max_length=14)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Cust_Analysis'


class VSalesOrderlist(models.Model):
    tabtype = models.CharField(db_column='TabType', primary_key=True, max_length=5)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=16)  # Field name made lowercase.
    custno = models.CharField(db_column='CustNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=22, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.CharField(db_column='OrderDate', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_OrderList'


class VSalesPastyear(models.Model):
    order_month = models.CharField(db_column='Order_Month',primary_key=True, max_length=7)  # Field name made lowercase.
    order_qty = models.FloatField(db_column='Order_Qty', blank=True, null=True)  # Field name made lowercase.
    ship_qty = models.FloatField(db_column='Ship_Qty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_PastYear'


class VSalesPastyearCust(models.Model):
    custno = models.CharField(db_column='CustNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    total_qty = models.FloatField(db_column='Total_Qty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_PastYear_Cust'


class VSalesQuarter(models.Model):
    weekly = models.CharField(db_column='Weekly', max_length=6, primary_key=True)  # Field name made lowercase.
    order_qty = models.FloatField(db_column='Order_Qty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Quarter'

class VSalesTopProduct(models.Model):
    partno = models.CharField(db_column='PartNo',primary_key=True, max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    custpn = models.CharField(db_column='CustPn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    orders = models.FloatField(db_column='Orders', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_Top_Product'

class SwcProduct(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', primary_key=True, max_length=20)  # Field name made lowercase.
    indexno = models.IntegerField(db_column='IndexNo')  # Field name made lowercase.
    custpn = models.CharField(db_column='CustPn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CustNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=10, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    beforeprice = models.FloatField(db_column='BeforePrice', blank=True, null=True)  # Field name made lowercase.
    lastprice = models.FloatField(db_column='LastPrice', blank=True, null=True)  # Field name made lowercase.
    lowprice = models.FloatField(db_column='lowPrice', blank=True, null=True)  # Field name made lowercase.
    highprice = models.FloatField(db_column='HighPrice', blank=True, null=True)  # Field name made lowercase.
    revisedate = models.DateTimeField(db_column='ReviseDate', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    product_cat = models.CharField(db_column='Product_cat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spec = models.TextField(db_column='Spec', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reviseby = models.CharField(db_column='Reviseby', max_length=10, blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    netweight = models.FloatField(db_column='NetWeight', blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    moq = models.FloatField(db_column='MOQ', blank=True, null=True)  # Field name made lowercase.
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)  # Field name made lowercase.
    syncdate = models.DateTimeField(db_column='SyncDate', blank=True, null=True)  # Field name made lowercase.
    webflag = models.CharField(db_column='webFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    short_spec = models.CharField(db_column='Short_Spec', max_length=60, blank=True, null=True)  # Field name made lowercase.
    vsc_no = models.CharField(db_column='VSC_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    page_no = models.CharField(db_column='Page_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adjustno = models.CharField(db_column='AdjustNO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainstock = models.CharField(db_column='MainStock', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cbm = models.DecimalField(db_column='CBM', max_digits=11, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sp001 = models.CharField(db_column='SP001', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sp002 = models.CharField(db_column='SP002', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sp003 = models.CharField(db_column='SP003', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sp004 = models.CharField(db_column='SP004', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sp005 = models.DecimalField(db_column='SP005', max_digits=11, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sp006 = models.DecimalField(db_column='SP006', max_digits=11, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    poprice = models.FloatField(db_column='PoPrice', blank=True, null=True)  # Field name made lowercase.
    beensynced = models.CharField(db_column='BeenSynced', max_length=100, blank=True, null=True)  # Field name made lowercase.
    carb = models.CharField(db_column='CARB', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordermsg = models.CharField(db_column='OrderMsg', max_length=500, blank=True, null=True)  # Field name made lowercase.
    netprice = models.DecimalField(db_column='NetPrice', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    firstorderdate = models.CharField(db_column='FirstOrderDate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isbundle = models.CharField(db_column='IsBundle', max_length=1, blank=True, null=True)  # Field name made lowercase.
    productremark = models.CharField(db_column='ProductRemark', max_length=200, blank=True, null=True)  # Field name made lowercase.
    producttype = models.CharField(db_column='ProductType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    productsize = models.CharField(db_column='ProductSize', max_length=5, blank=True, null=True)  # Field name made lowercase.
    serialcode = models.CharField(db_column='SerialCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=20, blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SWC_Product'
        unique_together = (('partno', 'indexno'),)

class VSalesNewproduct(models.Model):
    partno = models.CharField(db_column='PartNo',primary_key=True, max_length=20)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    orders = models.FloatField(db_column='Orders', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Sales_NewProduct'
