# 导入pymysql模块
import pymysql
import json
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

# name='武汉新洲万达文旅项目B地块户内及公区精装修工程标段三'
# project_id = '3209e90a-6705-cd2b-ce30-67c54bcea55d'
num="QS2025-LY-SG006"

sql="select b.id,b.name from Contracts a INNER JOIN Project b on a.id=b.contract_id where a.num='%s'"%(num)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
project_id = data[0]  # 计划金额
name = data[1]  # 销项税


# 工程收入--计划金额、销项税
sql = "select income, output_tax from Project_Budgets  where project_id=(select id from project where name = '%s')" % (
    name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
gcsr_jhje = float(data[0] or 0)  # 计划金额
gcsr_jhje_xxs = float(data[1] or 0)  # 销项税


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
gcsr_dsje = round(gcsr_htje - gcsr_ssje, 2)
gcsr_jxxs = round((gcsr_jhje_xxs - gcsr_ssje_xxs), 2)


print(gcsr_jhje, gcsr_jhje_xxs, gcsr_htje, gcsr_htje_xxs, gcsr_ssje, gcsr_ssje_xxs, gcsr_dsje, gcsr_jxxs)


# 专项分包金额-计划金额、进项税
sql = "select amount,vat from subcontract_budgets  where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_jhje = float(data[0] or 0)  # 专项分包金额-计划金额
zxfbje_jhje_jjx = float(data[1] or 0)  # 专项分包金额-进项税

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


# sql="select sum(amount),sum(tax) from Purchase_Orders where  project_id='%s'"% (project_id)
# cursor.execute(sql)
# result = cursor.fetchall()
# if result == ():
#     result = (('0', '0'), ())
# data = result[0]
# cgje_sfje= float(data[0] or 0)
# cgje_sfje_jxs= float(data[1] or 0)



# 专项分包金额-待付款金额、待抵扣进项税
sql = "select sum(payment_balance) from APs where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxfbje_dfje = float(data[0] or 0)

zxfbje_ddkjxs = round((zxfbje_htje_jxs - zxfbje_sfje_jxs), 2)

print(zxfbje_jhje, zxfbje_jhje_jjx, zxfbje_htje, zxfbje_htje_jxs, zxfbje_sfje, zxfbje_sfje_jxs, zxfbje_dfje, zxfbje_ddkjxs)

# 项目管理费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='Management' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
xmglf_jhje = float(data[0] or 0)
xmglf_jhje_jxs = float(data[1] or 0)


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

print(xmglf_jhje, xmglf_jhje_jxs, "  ", "   ", xmglf_sfje, xmglf_sfje_jxs)

# 业务费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='business' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ywf_jhje = float(data[0] or 0)
ywf_jhje_jxs = float(data[1] or 0)


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

print(ywf_jhje, ywf_jhje_jxs, "  ", "   ", ywf_sfje, ywf_sfje_jxs)

# 平台服务费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='PlatformService' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
ptfwf_jhje = float(data[0] or 0)
ptfwf_jhje_jxs = float(data[1] or 0)




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


print(ptfwf_jhje, ptfwf_jhje_jxs, "  ", "   ", ptfwf_sfje, ptfwf_sfje_jxs)

# 综合税额（含附加税）-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='additionalTax' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zhse_jhje = float(data[0] or 0)
zhse_jhje_jxs = float(data[1] or 0)


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



print(zhse_jhje, zhse_jhje_jxs, "  ", "   ", zhse_sfje, zhse_sfje_jxs)

# 财务费用-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='financialexpenses' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
cwfy_jhje = float(data[0] or 0)
cwfy_jhje_jxs = float(data[1] or 0)

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


print(cwfy_jhje, cwfy_jhje_jxs, "  ", "   ", cwfy_sfje, cwfy_sfje_jxs)

# 维保费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='maintenance' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
wbf_jhje = float(data[0] or 0)
wbf_jhje_jxs = float(data[1] or 0)




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

print(wbf_jhje, wbf_jhje_jxs, "  ", "   ", wbf_sfje, wbf_sfje_jxs)

# 其他支出-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='others' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
qt_jhje = float(data[0] or 0)
qt_jhje_jxs = float(data[1] or 0)

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

print(qt_jhje, qt_jhje_jxs, "  ", "   ", qt_sfje, qt_sfje_jxs)

# 措施费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='precaution' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
csf_jhje = float(data[0] or 0)
csf_jhje_jxs = float(data[1] or 0)

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

print(csf_jhje, csf_jhje_jxs, "  ", "   ", csf_sfje, csf_sfje_jxs)

# 利润分配-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='lirunfenpei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
lrfp_jhje = float(data[0] or 0)
lrfp_jhje_jxs = float(data[1] or 0)

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

print(lrfp_jhje, lrfp_jhje_jxs, "  ", "   ", lrfp_sfje, lrfp_sfje_jxs)

# 居间费-计划金额、进项税
sql = "select b.amount,ifnull(b.vat,0) from Project_Budgets a inner join project_budget_costs b on a.id=b.parent_id and b.name='jujianfei' and a.project_id='%s'" % (
    project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
jjf_jhje = float(data[0] or 0)
jjf_jhje_jxs = float(data[1] or 0)

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

print(jjf_jhje, jjf_jhje_jxs, "  ", "   ", jjf_sfje, jjf_sfje_jxs)

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
    zxfbje_jhje + xmglf_jhje + ywf_jhje + ptfwf_jhje + zhse_jhje + cwfy_jhje + wbf_jhje + qt_jhje + csf_jhje + lrfp_jhje + jjf_jhje,
    2)
jhje_jxs_xj = round(
    zxfbje_jhje_jjx + xmglf_jhje_jxs + ywf_jhje_jxs + ptfwf_jhje_jxs + zhse_jhje_jxs + cwfy_jhje_jxs + wbf_jhje_jxs + qt_jhje_jxs + csf_jhje_jxs + lrfp_jhje_jxs + jjf_jhje_jxs,
    2)

htje_xj = zxfbje_htje
htje_jxs_xj = zxfbje_htje_jxs

sfje_xj = round(
    zxfbje_sfje + xmglf_sfje + ywf_sfje + ptfwf_sfje + zhse_sfje + cwfy_sfje + wbf_sfje + qt_sfje + csf_sfje + lrfp_sfje + jjf_sfje + jkye_sfje,
    2)
sfje_jxs_xj = round(
    zxfbje_sfje_jxs + xmglf_sfje_jxs + ywf_sfje_jxs + ptfwf_sfje_jxs + zhse_sfje_jxs + cwfy_sfje_jxs + wbf_sfje_jxs + qt_sfje_jxs + csf_sfje_jxs + lrfp_sfje_jxs + jjf_sfje_jxs,
    2)
dfje_xj=zxfbje_dfje
djkjjs_xj = zxfbje_ddkjxs


print(jhje_xj, jhje_jxs_xj, htje_xj, htje_jxs_xj, sfje_xj, sfje_jxs_xj,dfje_xj ,djkjjs_xj)

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
kb_sb_zxfbjhsl = int(data[0] or 0)




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
kb_sb_xmhkl = f"{xmhk}%"  # 结果为 "96.49%"



#3.形象进度
sql="select progress from Project_Week_Logs  where project_id='%s' order by date_end desc limit 1"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
a = data[0]  # 计划金额
kb_sb_xxjd = f"{a}%"

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
kb_sb_jhjeysjjebfb=f"{(kb_ssje/kb_jhje)*100:.2f}%"


#5.所有计划的计划税额与所有实际税额的百分比
sql = "select input_tax from Project_Budgets where project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kb_5_jhse = float(data[0] or 0)

kb_sb_jhseysjsebfb=f"{(sfje_jxs_xj/kb_5_jhse)*100:.2f}%"


#6.项目倒计时
sql="SELECT CASE WHEN end_date <= CURDATE() THEN '已到达完工时间' ELSE CONCAT('剩余', DATEDIFF(end_date, CURDATE()), '天') END AS days_status FROM Project_Starts where project_id='%s'"% (project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
kb_sb_xmdjs = data[0]
if kb_sb_xmdjs==None:
    kb_sb_xmdjs="用户未填写完工日期"

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

kb_sb_jhxjcsysjxjcsdb=f"{jhxjcs}:{sjxjcs}"


print(kb_sb_zxfbjhsl, kb_sb_xmhkl,kb_sb_xxjd,kb_sb_jhjeysjjebfb,kb_sb_jhseysjsebfb,kb_sb_xmdjs,kb_sb_jhxjcsysjxjcsdb)



#资金预览--项目收入--项目收入、其他收入
zjyl_xmsr_xmsr=zxfbje_sfje  #项目收入


sql="select ifnull(sum(amount),0) from Other_ARs where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjyl_xmsr_qtsr = float(data[0])


#资金预览--项目支出--分包合同已付金额、分包合同未付金额、费用报销金额、开票税费、借款单余额
zjyl_xmzc_fbhtyfje=zxfbje_sfje #分包合同已付金额

sql="select sum(recent_amount) from Subcontracts where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zxhj = float(data[0])
xmzc_fbhtwfje_str=f"{(zxhj-zjyl_xmzc_fbhtyfje):.2f}" #分包合同未付金额
zjyl_xmzc_fbhtwfje=float(xmzc_fbhtwfje_str)

sql="select ifnull(sum(expense_amount),0) from Expenses where project_id='%s' and approval_status='Approval'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjyl_xmzc_fybxje = float(data[0])#费用报销金额

sql="select sum(zksf) from ARs where project_id='%s' and approval_status='Approval'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjyl_xmzc_kpsf = float(data[0])#开票税费

sql="select ifnull(sum(balance),2) from Loans where  project_id='%s' and approval_status='Approval' "%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjyl_xmzc_jkdye = float(data[0])#借款单余额

#资金预览--项目暂扣费--风险押金、履约保证金、资料押金、其他押金、居间费
sql="select risk,deposit,other_deposit,pay_management_fee from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
fxyj_bfb = data[0]
xmzkf_fxyj_str = f"{(zjyl_xmsr_xmsr * (fxyj_bfb / 100)):.2f}"
zjyl_xmzkf_fxyj=float(xmzkf_fxyj_str)#风险押金
a = data[1] # 资料押金
b = data[2]# 其他押金
zjyl_xmzkf_xmglf = data[3]# 项目管理费

zjyl_xmzkf_lybzj=0 #履约保证金

xmzkf_zlyj_str=f"{(zjyl_xmsr_xmsr * (a / 100)):.2f}"
zjyl_xmzkf_zlyj=float(xmzkf_zlyj_str)#资料押金
xmzkf_qtyj_str=f"{(zjyl_xmsr_xmsr * (b / 100)):.2f}"
zjyl_xmzkf_qtyj=float(xmzkf_qtyj_str)#其他押金



sql="select zkywf from project where name='%s' "%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
fxyj_jjf_bfb = data[0]
xmzkf_xmsr=zxfbje_sfje
xmzkf_fxyj_ze = f"{(xmzkf_xmsr * (fxyj_jjf_bfb / 100)):.2f}"

zjyl_xmzkf_jjf=float(xmzkf_fxyj_ze)-float(jjf_sfje)#居间费

#资金预览--项目垫资款-垫资款余额
sql="select sum(balance) from entrusted_collections where parent_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjyl_xmdzk_dzkye = float(data[0])#垫资款余额


#资金预览--进项税-已登记进项税
zjyl_jxs_ydjjxs=sfje_jxs_xj


#资金预览--管理费-已收管理费
glf_xmsr_bfb=zjyl_xmzkf_xmglf
glf_xmsr=zxfbje_sfje
glf_ysglf_str = f"{(glf_xmsr * (glf_xmsr_bfb / 100)):.2f}"#风险押金
zjyl_glf_ysglf=float(glf_ysglf_str)


#资金预览--项目可用额度
zjyl_xmkyed=f"{(zjyl_xmsr_xmsr+zjyl_xmsr_qtsr+(zjyl_xmzc_fbhtyfje+zjyl_xmzc_fbhtwfje+zjyl_xmzc_fybxje+zjyl_xmzc_kpsf+zjyl_xmzc_jkdye)-(zjyl_xmzkf_fxyj+zjyl_xmzkf_lybzj+zjyl_xmzkf_zlyj+zjyl_xmzkf_qtyj+zjyl_xmzkf_jjf)+zjyl_xmdzk_dzkye+zjyl_jxs_ydjjxs-zjyl_glf_ysglf):.2f}"



print(zjyl_xmsr_xmsr,zjyl_xmsr_qtsr,zjyl_xmzc_fbhtyfje,zjyl_xmzc_fbhtwfje,zjyl_xmzc_fybxje,zjyl_xmzc_kpsf,zjyl_xmzc_jkdye,zjyl_xmzkf_fxyj,zjyl_xmzkf_lybzj,zjyl_xmzkf_zlyj,zjyl_xmzkf_qtyj,zjyl_xmzkf_jjf,zjyl_xmdzk_dzkye,zjyl_jxs_ydjjxs,zjyl_glf_ysglf,zjyl_xmkyed)

#看板下部_项目状态
sql="select stage from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_xmzt_status =data[0]
zjxq_xmzt=""#项目状态
if zjxq_xmzt_status =="started":
    zjxq_xmzt="已开始"
if zjxq_xmzt_status =="not_started":
    zjxq_xmzt = "未开始"
if zjxq_xmzt_status =="seal":
    zjxq_xmz = "已封账"
if zjxq_xmzt_status =="ended":
    zjxq_xmzt= "已竣工"
if zjxq_xmzt_status =="settled":
    zjxq_xmzt= "已结算"
if zjxq_xmzt_status =="checked":
    zjxq_xmzt= "已完工"


#分包合同已付比例
zjxq_htje=zxfbje_htje
zjxq_yfje=zxfbje_sfje

zjxq_fbhtyfbl=f"{(zjxq_yfje/zjxq_htje)*100:.2f}%"#分包合同已付比例

#借款余额
sql="select ifnull(sum(balance),0) from Loans where project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_jkye = float(data[0])#借款余额

#计税方式
sql="select tax_calculation_method from project where name='%s'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_jsfs_code = float(data[0])
zjxq_jsfs=""#计税方式
if zjxq_jsfs_code ==1:
    zjxq_jsfs='简易计税'
if zjxq_jsfs_code ==2:
    zjxq_jsfs='一般计税'

# #劳务合同比例
sql="select count(*) from Subcontracts a inner join subcontract_items b on a.id=b.parent_id where approval_status='Approval' and a.project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_htzs=float(data[0]) #合同总数

sql="select count(b.tax_rate) from Subcontracts a inner join subcontract_items b on a.id=b.parent_id where approval_status='Approval' and a.project_id='%s' and tax_rate =3.00 GROUP BY b.tax_rate ORDER BY tax_rate"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_lw_ht_sl=float(data[0]) #%3劳务合同数量

zjxq_lwhtbl=f"{(zjxq_lw_ht_sl/zjxq_htzs)*100:.2f}%"



#应收甲方质保金
sql="select ifnull(sum(invoice_balance),0) from ARs where project_id='%s' and zhibaojin=1"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_ysjfzbj=float(data[0]) #应收甲方质保金

#材料合同（13%）比例
sql="select count(b.tax_rate) from Subcontracts a inner join subcontract_items b on a.id=b.parent_id where approval_status='Approval' and a.project_id='%s' and tax_rate =13.00 GROUP BY b.tax_rate ORDER BY tax_rate"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_cl_ht_sl=float(data[0]) #%13材料合同数量

zjxq_clhtbl=f"{(zjxq_cl_ht_sl/zjxq_htzs)*100:.2f}%"

#实际注册占计划比值：
zjxq_sjzczjbbz=f"{(sfje_xj/jhje_xj)*100:.2f}%"#实际注册占计划比值：

#累计开票金额
sql="select sum(amount) from Purchase_Invoices where approval_status='Approval' and project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('0', '0'), ())
data = result[0]
zjxq_jlkpje=float(data[0])#累计开票金额

#质保金到期日
sql="select b.date_plan from Contracts a inner join contract_collection_plans b on a.id=b.parent_id and a.name='%s' and b.phase='zhibaojin'"%(name)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('-', '0'), ())
data = result[0]
zjxq_zbjdqr=data[0]#质保金到期日

#已收款比例
zjxq_yskbl = f"{(gcsr_ssje / gcsr_htje * 100):.2f}%" if gcsr_htje != 0 else "0.00%"#已收款比例

#应付质保金、未付质保金
sql="select ifnull(sum(amount),0),ifnull(sum(payment_balance),0) from APs where project_id='%s' and approval_status='Approval' and zhibaojin=1"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
if result == ():
    result = (('-', '0'), ())
data = result[0]
zjxq_yfzbj=data[0]#应付质保金
zjxq_wfzbj=data[0]#未付质保金



print(zjxq_xmzt,zjxq_fbhtyfbl,zjxq_jkye,zjxq_jsfs,zjxq_lwhtbl,zjxq_ysjfzbj,zjxq_clhtbl,zjxq_sjzczjbbz,zjxq_jlkpje,zjxq_zbjdqr,zjxq_yskbl,zjxq_yfzbj,zjxq_wfzbj)


