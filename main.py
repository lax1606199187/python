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

name = '金银湖大厦五层餐饮中心、六层会议中心及包房室内装饰土建安装工程'
project_id = 'acd2a89d-cbc7-29c1-9fcd-63772c33f81a'
# name='湖北省体育产业集团办公楼装修工程'
# project_id='110619cf-e20e-24f9-c880-627b63ad3702'

# name = '软件园C6栋5楼东侧防水维修工程'

# 1.专项分包计划数量
sql = "select num from Contracts  where name='%s'" % (name)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
nvbh = data[0]
Contracts_number=""
if nvbh is not None:
    Contracts_num = nvbh + "-%"
    sql2 = "select count(*) from subcontract_budget_items  where name like '%s'" % (Contracts_num)
    cursor.execute(sql2)
    result = cursor.fetchall()
    data = result[0]
    Contracts_number = data[0]
else:
    Contracts_number=0


#项目回款率
sql = "select income from Project_Budgets where Project_id='%s'"%(project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
sr = data[0]

sql = "select sum(amount) as amount   from Collections  where project_id='%s' and ar_type='ARs'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
ysje = data[0]
a=ysje/sr
xmhk = int(a * 10000) / 100
xmhkl = f"{xmhk}%"  # 结果为 "96.49%"
print(Contracts_number,xmhkl)
# 工程收入--计划金额、销项税
sql = "select income, output_tax from Project_Budgets  where project_id=(select id from project where name = '%s')" % (
    name)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
income = data[0]  # 计划金额
output_tax = data[1]  # 销项税

# 工程收入--合同金额、销项税
sql = "select recent_amount from Contracts where  name='%s'" % (name)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
recent_amount = data[0]  # 合同金额
# 销项税

# 工程收入--实收金额、销项税
sql = "select sum(amount) as amount   from Collections  where project_id='%s' and ar_type='ARs'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
gcsr_ssje = data[0]  # 实收金额

sql = "select sum(tax) from ARs where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
gcsr_xxs = data[0]  # 销项税

# 工程收入--代收金额、待缴销项税
dsje = recent_amount - gcsr_ssje  # 代收金额

print(income, output_tax, recent_amount, "销项税", gcsr_ssje, gcsr_xxs, dsje, "待缴销项税")

# 专项分包金额-计划金额、进项税
sql = "select amount,vat from subcontract_budgets  where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
zxfbge_jhje = data[0]  # 专项分包金额-计划金额
zxfbge_jhje_vat = data[1]  # 专项分包金额-进项税

# 专项分包金额-合同金额、进项税
sql = "select sum(recent_amount) as recent_amount from Subcontracts  where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
zxfbje_htje = data[0]  # 专项分包金额-合同金额
# 专项分包金额-进项税

# 专项分包金额-待付款金额、带抵扣进项税
sql = "select sum(payment_balance) from APs where project_id='%s'" % (project_id)
cursor.execute(sql)
result = cursor.fetchall()
data = result[0]
zxfbje_dfkje = data[0]

print(zxfbge_jhje, zxfbge_jhje_vat, zxfbje_htje, "进项税", "实付金额", "进项税", zxfbje_dfkje, "待抵扣进项税")
