# 导入pymysql模块
import pymysql

# 建立数据库连接
conn = pymysql.connect(
    host='120.26.141.56',		# 主机名（或IP地址）
    port=3306,				# 端口号，默认为3306
    user='test',			# 用户名
    password='HgSs9op0',	# 密码
    charset='utf8mb4'  		# 设置字符编码
)


# 创建游标对象
cursor = conn.cursor()

# 选择数据库
conn.select_db("test")

# 工程收入--计划金额、销项税
sql = "select income, output_tax from Project_Budgets  where project_id=(select id from project where name = '金银湖大厦五层餐饮中心、六层会议中心及包房室内装饰土建安装工程')"
cursor.execute(sql)
result = cursor.fetchall()
data=result[0]
income=data[0] #计划金额
output_tax=data[1]  #销项税

#工程收入--合同金额、销项税
sql = "select recent_amount from Contracts where  name='金银湖大厦五层餐饮中心、六层会议中心及包房室内装饰土建安装工程'"
cursor.execute(sql)
result = cursor.fetchall()
data=result[0]
recent_amount=data[0] #合同金额
                    #销项税

#工程收入--实收金额、销项税
sql = "select sum(amount) as amount   from Collections  where project_id='acd2a89d-cbc7-29c1-9fcd-63772c33f81a' and ar_type='ARs'"
cursor.execute(sql)
result = cursor.fetchall()
data=result[0]
gcsr_amount=data[0] # 实收金额
                #销项税

#工程收入--代收金额、待缴销项税
dsje=recent_amount-gcsr_amount #代收金额

#专项分包金额-计划金额、进项税
sql="select amount,vat from subcontract_budgets  where project_id='acd2a89d-cbc7-29c1-9fcd-63772c33f81a'"
cursor.execute(sql)
result = cursor.fetchall()
data=result[0]
zxfbge_jhje=data[0] #专项分包金额-计划金额
zxfbge_jhje_vat=data[1]  #专项分包金额-进项税

#专项分包金额-合同金额、进项税
sql="select sum(recent_amount) as recent_amount from Subcontracts  where project_id='acd2a89d-cbc7-29c1-9fcd-63772c33f81a'"
cursor.execute(sql)
result = cursor.fetchall()
data=result[0]
zxfbje_htje=data[0]#专项分包金额-合同金额
# zxfbje_htje_vat=data[1]#专项分包金额-进项税

print(income,output_tax,recent_amount,gcsr_amount,dsje,zxfbge_jhje,zxfbje_htje)



