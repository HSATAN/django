需求见最下：

① trade_base transport_company 不规则，不好判断。 会导致 部分快递无法获取详细信息
   具体匹配见 “快递匹配测试” 未匹配到的，直接返回原始数据。在 transport_company_code 表中 做 like 查询。

② 本来想做 While True 循环，可能存在较多问题。最好做成 定时任务执行脚本。

③ 期间遇到一个问题： 相同的url，两次请求返回结果不一致，json key 也有所差别。（应该是偶然事件）

④ 另需处理的： port78, USPS

当前数据格式：

{"data": [{
          "context": "\u5df2\u7b7e\u6536,\u611f\u8c22\u4f7f\u7528\u987a\u4e30,\u671f\u5f85\u518d\u6b21\u4e3a\u60a8\u670d\u52a1",
          "time": "2015-04-14 14:24:23"}, {
          "context": "\u5728\u5b98\u7f51\"\u8fd0\u5355\u8d44\u6599&\u7b7e\u6536\u56fe\",\u53ef\u67e5\u770b\u7b7e\u6536\u4eba\u4fe1\u606f",
          "time": "2015-04-14 14:24:23"}, {
          "context": "\u6b63\u5728\u6d3e\u9001\u9014\u4e2d,\u8bf7\u60a8\u51c6\u5907\u7b7e\u6536<br/>(\u6d3e\u4ef6\u4eba:\u738b\u4e91\u5408,\u7535\u8bdd:13910637068)",
          "time": "2015-04-14 13:55:14"}, {
          "context": "\u7531\u4e8e\u6536\u4ef6\u5730\u5740\u8ddd\u670d\u52a1\u70b9\u8f83\u8fdc,\u9700\u52a0\u5de5\u4f5c\u65e5\u6d3e\u9001,\u8bf7\u8010\u5fc3\u7b49\u5019",
          "time": "2015-04-14 13:52:49"}, {
          "context": "[\u3010\u5317\u4eac\u53f0\u6e56\u670d\u52a1\u70b9\u3011]\u5feb\u4ef6\u5230\u8fbe \u3010\u5317\u4eac\u53f0\u6e56\u670d\u52a1\u70b9\u3011",
          "time": "2015-04-14 10:26:03"}, {
          "context": "\u5feb\u4ef6\u5230\u8fbe \u3010\u5317\u4eac\u5927\u5174\u96c6\u6563\u4e2d\u5fc3\u3011",
          "time": "2015-04-14 08:19:27"}, {
          "context": "\u5feb\u4ef6\u5230\u8fbe \u3010\u5317\u4eac\u987a\u4e49\u96c6\u6563\u4e2d\u5fc3\u3011",
          "time": "2015-04-14 06:23:22"}
          ],
 "package_no": "660593498897",
 "transport_state": "3",
 "transport_company": "\u987a\u4e30"}




 以下是物流信息抓取流程：

一、流程：
1. 根据trade_logistics_info表中：package_no, transport_company从快递100抓取物流信息，
2. 将数据转换为如下格式，填到transport_detail字段，并将update_time更新为当前时间。

{
    "package_no": "912097532087",  //
    "transport_company": "顺丰",
    "transport_state": "3",
    "data": [
        {
            "time": "2015-04-13 14:55:59",
            "context": "签收人是：已签收"
        },
        {
            "time": "2015-04-12 18:46:26",
            "context": "快件到达 【长春长青集散中心】"
        }
    ]
}

二、爬取策略：
1. 对于同一个订单， 2小时重爬一次（根据update_time确认）
2. 相邻两次爬取时间间隔：20s。
3. url拼接规则：
url前缀：http://www.kuaidi100.com/query
参数：
type: 快递公司名称（需要归一化为英文名称或者拼音：具体见表： transport_company_code）
postid:快递单号

例子：
http://www.kuaidi100.com/query?type=shunfeng&postid=660593498897

4. --user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
三、测试数据库
121.201.15.204（root, mfashion）

四，上线（待确认）