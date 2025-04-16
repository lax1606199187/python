# 导入pymysql模块
import pymysql

# 建立数据库连接
conn = pymysql.connect(
    host='120.26.141.56',  # 主机名（或IP地址）
    port=3306,  # 端口号，默认为3306
    user='test',  # 用户名
    password='HgSs9op0',  # 密码
    charset='utf8mb4'  # 设置字符编码
)

# 创建游标对象
cursor = conn.cursor()

# 选择数据库
conn.select_db("test")

# name = '金银湖大厦五层餐饮中心、六层会议中心及包房室内装饰土建安装工程'
# project_id = 'acd2a89d-cbc7-29c1-9fcd-63772c33f81a'

# name = '湖北省体育产业集团办公楼装修工程'
# project_id = '110619cf-e20e-24f9-c880-627b63ad3702'

name='武汉新洲万达文旅项目B地块户内及公区精装修工程标段三'
project_id = '3209e90a-6705-cd2b-ce30-67c54bcea55d'

# 工程收入--计划金额、销项税
sql = "select income, output_tax from Project_Budgets  where project_id=(select id from project where name = '%s')" % (
    name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_jhje = float(data[0] or 0)  # 计划金额
gcsr_xxs = float(data[1] or 0)  # 销项税

# 工程收入--合同金额、销项税
sql = "select recent_amount from Contracts where  name='%s'" % (name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_htje = float(data[0] or 0)  # 合同金额

sql = "select output_tax from Project_Budgets where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_htje_xxs = float(data[0] or 0)  # 合同金额

# 工程收入--实收金额、销项税
sql = "select sum(amount) as amount   from Collections  where project_id='%s' and ar_type='ARs'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_ssje = float(data[0] or 0)  # 实收金额

sql = "select sum(tax) from ARs where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_ssje_xxs = float(data[0] or 0)  # 销项税

# 工程收入--代收金额、待缴销项税
dsje = round(gcsr_htje - gcsr_ssje, 2)
djxxs = round((gcsr_xxs - gcsr_ssje_xxs), 2)

print(gcsr_jhje, gcsr_xxs, gcsr_htje, gcsr_htje_xxs, gcsr_ssje, gcsr_ssje_xxs, dsje, djxxs)

# 专项分包金额-计划金额、进项税
sql = "select amount,vat from subcontract_budgets  where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbge_jhje = float(data[0] or 0)  # 专项分包金额-计划金额
zxfbge_jhje_jjx = float(data[1] or 0)  # 专项分包金额-进项税

# 专项分包金额-合同金额、进项税
sql = "select sum(recent_amount) as recent_amount from Subcontracts  where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_htje = float(data[0] or 0)  # 专项分包金额-合同金额
# 专项分包金额-进项税
sql = "select sum(tax) from Subcontracts where project_id='%s' " % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_htje_jxs = float(data[0] or 0)

# 专项分包金额-实付金额、进项税
sql = "select sum(amount) from Payments where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_sfje = float(data[0] or 0)



sql = "select sum(vat) from Purchase_Invoices where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_sfje_jxs = float(data[0] or 0)


sql="select sum(amount),sum(tax) from Purchase_Orders where  project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
cgje_sfje= float(data[0] or 0)
cgje_sfje_jxs= float(data[1] or 0)


# 专项分包金额-待付款金额、待抵扣进项税
sql = "select sum(payment_balance) from APs where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_dfkje = float(data[0] or 0)

ddkjxs = round((zxfbje_htje_jxs - zxfbje_sfje_jxs), 2)

print(zxfbge_jhje, zxfbge_jhje_jjx, zxfbje_htje, zxfbje_htje_jxs, zxfbje_sfje, zxfbje_sfje_jxs, zxfbje_dfkje, ddkjxs)

# 项目管理费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='Management' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmglf_jhje = float(data[0] or 0)
xmglf_jxs = float(data[1] or 0)

# 项目管理费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) vat from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects'  and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_management' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmglf_sfje = float(data[0] or 0)
xmglf_sfje_jxs = float(data[1] or 0)

print(xmglf_jhje, xmglf_jxs, "  ", "   ", xmglf_sfje, xmglf_sfje_jxs)

# 业务费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='business' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ywf_jhje = float(data[0] or 0)
ywf_jxs = float(data[1] or 0)

# 业务费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_business' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ywf_sfje = float(data[0] or 0)
ywf_sfje_jxs = float(data[1] or 0)

print(ywf_jhje, ywf_jxs, "  ", "   ", ywf_sfje, ywf_sfje_jxs)

# 平台服务费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='PlatformService' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ptfwf_jhje = float(data[0] or 0)
ptfwf_jxs = float(data[1] or 0)

# 平台服务费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_PlatformService' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ptfwf_sfje = float(data[0] or 0)
ptfwf_sfje_jxs = float(data[1] or 0)

print(ptfwf_jhje, ptfwf_jxs, "  ", "   ", ptfwf_sfje, ptfwf_sfje_jxs)

# 综合税额（含附加税）-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='additionalTax' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zhse_jhje = float(data[0] or 0)
zhse_jxs = float(data[1] or 0)

# 综合税额（含附加税）-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_additionalTax' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zhse_sfje = float(data[0] or 0)
zhse_sfje_jxs = float(data[1] or 0)

print(zhse_jhje, zhse_jxs, "  ", "   ", zhse_sfje, zhse_sfje_jxs)

# 财务费用-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='financialexpenses' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
cwfy_jhje = float(data[0] or 0)
cwfy_jxs = float(data[1] or 0)

# 财务费用-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_financialexpenses' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
cwfy_sfje = float(data[0] or 0)
cwfy_sfje_jxs = float(data[1] or 0)

print(cwfy_jhje, cwfy_jxs, "  ", "   ", cwfy_sfje, cwfy_sfje_jxs)

# 维保费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='maintenance' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
wbf_jhje = float(data[0] or 0)
wbf_jxs = float(data[1] or 0)

# 维保费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_maintenance' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
wbf_sfje = float(data[0] or 0)
wbf_sfje_jxs = float(data[1] or 0)

print(wbf_jhje, wbf_jxs, "  ", "   ", wbf_sfje, wbf_sfje_jxs)

# 其他支出-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='others' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
qt_jhje = float(data[0] or 0)
qt_jxs = float(data[1] or 0)

# 其他支出-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_others' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
qt_sfje = float(data[0] or 0)
qt_sfje_jxs = float(data[1] or 0)

print(qt_jhje, qt_jxs, "  ", "   ", qt_sfje, qt_sfje_jxs)

# 措施费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='precaution' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
csf_jhje = float(data[0] or 0)
csf_jxs = float(data[1] or 0)

# 措施费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_precaution' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
csf_sfje = float(data[0] or 0)
csf_sfje_jxs = float(data[1] or 0)

print(csf_jhje, csf_jxs, "  ", "   ", csf_sfje, csf_sfje_jxs)

# 利润分配-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='lirunfenpei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
lrfp_jhje = float(data[0] or 0)
lrfp_jxs = float(data[1] or 0)

# 利润分配-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_lirunfenpei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
lrfp_sfje = float(data[0] or 0)
lrfp_sfje_jxs = float(data[1] or 0)

print(lrfp_jhje, lrfp_jxs, "  ", "   ", lrfp_sfje, lrfp_sfje_jxs)

# 居间费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='jujianfei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
jjf_jhje = float(data[0] or 0)
jjf_jxs = float(data[1] or 0)

# 居间费-实付金额、进项税
sql = "select sum(b.amount) amount,ifnull(sum(b.vat),0) from Expenses a inner join expense_items b on a.id=b.parent_id  where a.type='Projects' and a.approval_status='Approval'  and b.deleted=0 and b.type like 'projects_jujianfei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
jjf_sfje = float(data[0] or 0)
jjf_sfje_jxs = float(data[1] or 0)

print(jjf_jhje, jjf_jxs, "  ", "   ", jjf_sfje, jjf_sfje_jxs)

# 借款余额-实付金额
sql = "select sum((amount-expense_amount-repayment_amount)) from Loans where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
jkye_sfje = float(data[0] or 0)

print(" ", "  ", "   ", jkye_sfje, "  ")

# 小计
jhje_xj = round(
    zxfbge_jhje + xmglf_jhje + ywf_jhje + ptfwf_jhje + zhse_jhje + cwfy_jhje + wbf_jhje + qt_jhje + csf_jhje + lrfp_jhje + jjf_jhje,
    2)
jhje_jxs_xj = round(
    zxfbge_jhje_jjx + xmglf_jxs + ywf_jxs + ptfwf_jxs + zhse_jxs + cwfy_jxs + wbf_jxs + qt_jxs + csf_jxs + lrfp_jxs + jjf_jxs,
    2)

htje_xj = zxfbje_htje
htje_jxs_xj = zxfbje_htje_jxs

sfje_xj = round(
    zxfbje_sfje + xmglf_sfje + ywf_sfje + ptfwf_sfje + zhse_sfje + cwfy_sfje + wbf_sfje + qt_sfje + csf_sfje + lrfp_sfje + jjf_sfje + jkye_sfje,
    2)
sfje_jxs_xj = round(
    zxfbje_sfje_jxs + xmglf_sfje_jxs + ywf_sfje_jxs + ptfwf_sfje_jxs + zhse_sfje_jxs + cwfy_sfje_jxs + wbf_sfje_jxs + qt_sfje_jxs + csf_sfje_jxs + lrfp_sfje_jxs + jjf_sfje_jxs,
    2)

djkjjs_xj = ddkjxs

print(jhje_xj, jhje_jxs_xj, htje_xj, htje_jxs_xj, sfje_xj, sfje_jxs_xj, djkjjs_xj)

print("===========================")
# 1.专项分包计划数量
sql = "select ifnull(num,0) from Contracts  where name='%s'" % (name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
nvbh = data[0]
Contracts_number = ""
Contracts_num = nvbh + "-%"
sql2 = "select count(*) from subcontract_budget_items  where name like '%s'" % (Contracts_num)
cursor.execute(sql2)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
Contracts_number = int(data[0] or 0)

# 2.项目回款率
sql = "select income from Project_Budgets where Project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
sr = int(data[0] or 0)

sql = "select sum(amount) as amount   from Collections  where project_id='%s' and ar_type='ARs'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ysje = int(data[0] or 0)
a = ysje / sr
xmhk = int(a * 10000) / 100
xmhkl = f"{xmhk}%"  # 结果为 "96.49%"



#3.形象进度
sql="select progress from Project_Week_Logs  where project_id='%s' order by date_end desc limit 1"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
a = data[0]  # 计划金额
xxjd = f"{a}%"

#4.计划金额与实际金额百分百
sql = "select income, output_tax from Project_Budgets  where project_id=(select id from project where name = '%s')" % (
    name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kb_jhje = float(data[0] or 0)  # 计划金额

sql = "select sum(amount) as amount   from Collections  where project_id='%s' and ar_type='ARs'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kb_ssje = float(data[0] or 0)  # 实收金额
jhje_sjje_bfb=f"{(kb_ssje/kb_jhje)*100:.2f}%"


#5.所有计划的计划税额与所有实际税额的百分比
sql = "select input_tax from Project_Budgets where project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kb_5_jhse = float(data[0] or 0)

jhse_sjse_bfb=f"{(sfje_jxs_xj/kb_5_jhse)*100:.2f}%"


#6.项目倒计时
sql="SELECT CASE WHEN end_date <= CURDATE() THEN '已到达完工时间' ELSE CONCAT('剩余', DATEDIFF(end_date, CURDATE()), '天') END AS days_status FROM Project_Starts where project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmdjs = data[0]
if xmdjs==None:
    xmdjs="用户未填写完工日期"

#7.计划巡检次数与实际巡检次数对比
sql="select count(*) from project_check_plans a INNER JOIN project_check_plan_items b on a.id=b.parent_id where a.project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
jhxjcs = data[0]

sql="select count(*) from project_checks where project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
sjxjcs = data[0]

jhxjcs_sjxjcs=f"{jhxjcs}:{sjxjcs}"


print(Contracts_number, xmhkl,xxjd,jhje_sjje_bfb,jhse_sjse_bfb,xmdjs,jhxjcs_sjxjcs)

print("=============================")

#项目收入--项目收入、其他收入
xmsr_xmsr=zxfbje_sfje  #项目收入


sql="select ifnull(sum(amount),0) from Other_ARs where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmsr_qtsr = float(data[0])


#项目支出--分包合同已付金额、分包合同未付金额、费用报销金额、开票税费、借款单余额
xmzc_fbhtyfje=zxfbje_sfje #分包合同已付金额

sql="select sum(recent_amount) from Subcontracts where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxhj = float(data[0])
xmzc_fbhtwfje_str=f"{(zxhj-xmzc_fbhtyfje):.2f}" #分包合同未付金额
xmzc_fbhtwfje=float(xmzc_fbhtwfje_str)

sql="select ifnull(sum(expense_amount),0) from Expenses where project_id='%s' and approval_status='Approval'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmzc_fybxje = float(data[0])#费用报销金额

sql="select sum(zksf) from ARs where project_id='%s' and approval_status='Approval'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmzc_kpsf = float(data[0])#开票税费

sql="select ifnull(sum(balance),2) from Loans where  project_id='%s' and approval_status='Approval' "%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmzc_jkdye = float(data[0])#借款单余额

#项目暂扣费--风险押金、履约保证金、资料押金、其他押金、居间费
sql="select risk,deposit,other_deposit,pay_management_fee from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
fxyj_bfb = data[0]
xmzkf_fxyj_str = f"{(xmsr_xmsr * (fxyj_bfb / 100)):.2f}"#风险押金
xmzkf_fxyj=float(xmzkf_fxyj_str)
fxyj_zlyj = data[1] # 资料押金
fxyj_qtyj = data[2]# 其他押金
fxyj_qtyj = data[3]# 项目管理费

xmzkf_lybzj=0 #履约保证金

xmzkf_zlyj_str=f"{(xmsr_xmsr * (fxyj_zlyj / 100)):.2f}"#资料押金
xmzkf_zlyj=float(xmzkf_zlyj_str)
xmzkf_qtyj_str=f"{(xmsr_xmsr * (fxyj_qtyj / 100)):.2f}"#其他押金
xmzkf_qtyj=float(xmzkf_qtyj_str)



sql="select zkywf from project where name='%s' "%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
fxyj_jjf_bfb = data[0]
xmzkf_xmsr=zxfbje_sfje
xmzkf_fxyj_ze = f"{(xmzkf_xmsr * (fxyj_jjf_bfb / 100)):.2f}"

xmzkf_jjf=float(xmzkf_fxyj_ze)-float(jjf_sfje)#居间费

#项目垫资款-垫资款余额
sql="select sum(balance) from entrusted_collections where parent_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmdzk_dzkye = float(data[0])#垫资款余额


#进项税-已登记进项税
jxs_ydjjxs=sfje_jxs_xj


#管理费-已收管理费
glf_xmsr_bfb=fxyj_qtyj
glf_xmsr=zxfbje_sfje
glf_ysglf_str = f"{(glf_xmsr * (glf_xmsr_bfb / 100)):.2f}"#风险押金
glf_ysglf=float(glf_ysglf_str)


#项目可用额度
xmkyed=f"{(xmsr_xmsr+xmsr_qtsr+(xmzc_fbhtyfje+xmzc_fbhtwfje+xmzc_fybxje+xmzc_kpsf+xmzc_jkdye)-(xmzkf_fxyj+xmzkf_lybzj+xmzkf_zlyj+xmzkf_qtyj+xmzkf_jjf)+xmdzk_dzkye+jxs_ydjjxs-glf_ysglf):.2f}"



print(xmsr_xmsr,xmsr_qtsr,xmzc_fbhtyfje,xmzc_fbhtwfje,xmzc_fybxje,xmzc_kpsf,xmzc_jkdye,xmzkf_fxyj,xmzkf_lybzj,xmzkf_zlyj,xmzkf_qtyj,xmzkf_jjf,xmdzk_dzkye,jxs_ydjjxs,glf_ysglf,xmkyed)

#看板下部_项目状态
sql="select stage from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kbxb_xmzt_status =data[0]#项目状态
kbxb_xmzt=""
if kbxb_xmzt_status =="started":
    kbxb_xmzt="已开始"
if kbxb_xmzt_status =="not_started":
    kbxb_xmzt = "未开始"
if kbxb_xmzt_status =="seal":
    kbxb_xmz = "已封账"
if kbxb_xmzt_status =="ended":
    kbxb_xmzt= "已竣工"
if kbxb_xmzt_status =="settled":
    kbxb_xmzt= "已结算"
if kbxb_xmzt_status =="checked":
    kbxb_xmzt= "已完工"


#分包合同已付比例
kbxb_htje=zxfbje_htje
kbxb_yfje=zxfbje_sfje


kbxb_fbhtyfbl=f"{(kbxb_yfje/kbxb_htje)*100:.2f}%"

#借款余额
sql="select ifnull(sum(balance),0) from Loans where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kbxb_jkye = float(data[0])#借款余额

#计税方式
sql="select tax_calculation_method from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kbxb_jsfs_code = float(data[0])
kbxb_jsfs=""#计税方式
if kbxb_jsfs_code ==1:
    kbxb_jsfs='简易计税'
if kbxb_jsfs_code ==2:
    kbxb_jsfs='一般计税'

# #劳务合同比例
sql="select count(*) from Subcontracts a inner join subcontract_items b on a.id=b.parent_id where approval_status='Approval' and a.project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kbxb_htzs=float(data[0]) #合同总数

sql="select count(b.tax_rate) from Subcontracts a inner join subcontract_items b on a.id=b.parent_id where approval_status='Approval' and a.project_id='%s' and tax_rate =3.00 GROUP BY b.tax_rate ORDER BY tax_rate"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kbxb_lw_ht_sl=float(data[0]) #%3劳务合同数量

kbxb_lw_ht=f"{(kbxb_lw_ht_sl/kbxb_htzs)*100:.2f}%"






print(kbxb_xmzt,kbxb_fbhtyfbl,kbxb_jkye,kbxb_jsfs,kbxb_lw_ht)