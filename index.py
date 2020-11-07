""" 
腾讯云函数专用
"""


def main_handler(event, context):
    temp = __import__("xmly_speed")
    temp.run()
    return "hello world"


if __name__ == "__main__":
    event = {'Message': '', 'Time': '2019-02-21T11:49:00Z',
             'TriggerName': 'EveryDay', 'Type': 'Timer'}
    context = {'memory_limit_in_mb': 128, 'time_limit_in_ms': 500000, 'request_id': 'abcdefg', 'environment': '{"SCF_NAMESPACE":"default"}', 'environ': 'xxxxxxxxxx',
               'function_version': '$LATEST', 'function_name': 'jd', 'namespace': 'default', 'tencentcloud_region': 'ap-beijing', 'tencentcloud_appid': '1111111111', 'tencentcloud_uin': '111111111'}

    main_handler(event, context)
