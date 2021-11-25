from urllib import parse # 转码
import hashlib # hash md5
from database.mysql import MysqlHelper # 操作数据库
import requests # 请求URL
import xlrd # 读取表格

class Index:
    # 链接数据库
    def __init__(self):
        self.helper = MysqlHelper()
        self.helper.connect()

    # 组装url
    def get_url(self, address = None):
        # 已get请求为例：http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
        queryStr = '/geocoder/v2/?address=%s&output=json&ak=Y6F597W87rrsWrmuwUGgEFjy' % address
        # 对queryStr进行转码，safe内保留字符不转换
        encodeStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        # 最后追加yoursk
        rawStr = encodeStr + '7r58bdiCoh6PGpkoEQ544PljySwn9sMI'
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        # 由于URL里面还有中文，所以需要parse.quote进行处理，然后返回最终可调用的url
        url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="/:=&?#+!$,;'@()*[]")
        return url

    # 读取excel表格 组装数组
    def read_excel(self):
        # 读取excel
        data = xlrd.open_workbook(r'F:\python\coordinate\tests.xls')
        table = data.sheets()[0]
        # 组装tables
        tables = []
        for rown in range(table.nrows):
            array = {'name': '', 'number': '', 'school': '', 'device': ''}
            array['name'] = table.cell_value(rown, 0)  # 第一列数据 位置名称
            array['number'] = table.cell_value(rown, 1)  # 第二列数据 设备序列号
            array['school'] = table.cell_value(rown, 2)  # 第二列数据 学校名称
            array['device'] = table.cell_value(rown, 3)  # 第二列数据 设备名称
            tables.append(array)
        return tables

    # 访问url获取返回信息
    def go_url(self):
        tables = self.read_excel() # 拿到表格数组
        for index in range(len(tables)):
            if index != 0: # 排除第一行
                # get请求url获取返回数据
                url = self.get_url(tables[index]['name'])
                res = requests.get(url)
                res.encoding = 'utf-8'
                data = res.json()
                # 请求成功进行组装修改数据库
                if data['status'] == 0:
                    # 组装坐标
                    coordinate = str(data['result']['location']['lng']) + ',' + str(data['result']['location']['lat'])
                    number = tables[index]['number']
                    # 组装sql 并执行
                    sql = "update t_device set coordinate = %s where serial_number = %s and is_delete = %s"
                    params = [
                        coordinate,
                        number,
                        0
                    ]
                    end = self.helper.update(sql, params)
                    if end == 1:
                        print(tables[index]['school'] + '的' + tables[index]['device'] + ' 更新成功')
                    else:
                        print(tables[index]['school'] + '的' + tables[index]['device'] + ' 更新失败或数据和数据库值重复，坐标为：' + coordinate)
                else:
                    print(tables[index]['school'] + '的' + tables[index]['device'] + ' 坐标搜索不到')
        self.helper.close() # 执行完毕关闭数据库连接

def main():
    index = Index()
    index.go_url()

if __name__ == "__main__":
    main()