'''
从数据库里查询邀请码
'''
import pymysql.cursors

# 和数据库相连接
con = pymysql.connect(
    host='localhost',
    user='django',
    password='**********',
    db='SS',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)


try:
    with con.cursor() as cursor:
        sql = "select code from ss_invite_code where user_id=484;"
        cursor.execute(sql)
        # 获取一个结果
        result = cursor.fetchone()
finally:
    con.close()

# 增加一个简单的判断
if result:
    invite_code = result['code']
else:
    invite_code='当前邀请码已经彻底用完，请在后台联系我'

print(invite_code)
