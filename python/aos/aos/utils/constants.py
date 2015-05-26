# -*- coding:utf-8 -*-

# 日志级别字典
log_level_dict = {0:u'DEBUG', 1:u'INFO', 2:u'WARN', 3:u'ERROR'}

# 权限类型
permission_type_dict = {1:u'系统管理', 2:u'配置管理', 3:u'工作台', 4:u'其他'}

# 日志类型
log_type_dict = {0:u'其他日志', 1:u'用户管理日志', 2:u'角色管理日志'}

# 监控类型
alarm_type_dict = {0:u'否', 1:u'是'}

# yes_no
yes_no_dict = {0:u'否', 1:u'是'}

# 优先级
priority_dict = {1:u'紧急', 2:u'普通'}

# 权重
weight_dict = {1:'1', 2:'2', 3:'3', 4:'4', 5:'5', \
               6:'6', 7:'7', 8:'8', 9:'9', 10:'10' }
               
# 工单状态
# 由于工单一创建就被分配了，事实上不会出现未接受的情况
order_status_dict = {1:u'未接受', 2:u'已接受', 3:u'已解决', 4:u'已升级', 5:u'已评价'}

# 工单流转记录动作
wander_action_dict = {1:u'创建&分配', 2:u'升级', 3:u'已解决&待评级', 4:u'评级完成&关闭'}

# 工单从创建到解决耗时
consume_time_dict = {1:u'<30分钟', 2:u'<1小时', 3:u'<２小时', 4:u'<1天', 5:u'>1天'}

# 来源
source_dict = {1:u'电话', 2:u'网络'}

# 满意度(反馈评级)
feedback_rate_dict = {1:u'非常不满意', 2:u'不满意', 3:u'满意', 4:u'比较满意', 5:u'非常满意'}

# 反馈表状态
feedback_status_dict = {0:u'提交', 1:u'已回复', 2:u'已关闭'}

# 服务器类型
server_type_dict = {0:u'虚拟机', 1:u'物理机'}

# 申请单状单
#apply_status_dict = {0:u'领导未批示', 1:u'资源处理中', 2:u'已处理'}
apply_status_dict = {0:u'初始化申请', 1:u'已审批', 2:u'已处理', 3:u'已关闭'}

# 申请单优先级
apply_priority_dict = {0:u'普通', 1:u'重要', 2:u'紧急'}

# 申请单流转记录动作
order_wander_dict = {0:u'创建&申请', 1:u'审核&批准', 2:u'处理&完成', 3:u'转发', 4:u'关闭'}

# 线路类型字典
link_type_dict = {0:u'移动', 1:u'联通', 2:u'电信', 3:'BGP', 4:u'阿里云'}

# 操作系统类型字典
os_type_dict = {0:'CentOS5.8_32', 1:'CentOS6.4_64', 2:'CentOS6.4_32', 3:'Win08R2_64', 4:'Win03R2_64', 5:u'其他'}






