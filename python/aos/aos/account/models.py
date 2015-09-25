# -*- coding:utf-8 -*-
# django library
from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.sessions.models import Session

#our own code
from role.models import Role
from authority.models import Permission

class UserProfile(models.Model):
    #重新定义表名
    class Meta:
        db_table = 'user_profile'
    # 用户对象，使用django 默认User对象
    user = models.OneToOneField(User)
    # 部门
    department = models.CharField(max_length=128, blank=True)
    # 电话
    phone = models.CharField(max_length=15, blank=True)
    # 真实姓名
    realname = models.CharField(max_length=32)
    # 审批领导登录帐号
    leader_username = models.CharField(max_length=64)
    # 审批领导真实姓名
    leader_realname = models.CharField(max_length=64)
    # 审批领导邮件地址
    leader_email = models.CharField(max_length=75)
    # 审批领导联系方式
    leader_phone = models.CharField(max_length=15)

# 仅用于页面显示
class UserExtend():
    def __init__(self):
        # 序号
        self.id = None
        # 用户名
        self.username = None
        # 电子邮件
        self.email = None
        # 角色
        self.roles = None
        # 角色ID 列表
        self.role_ids = None
        # 部门 
        self.department = None
        # 联系方式
        self.phone = None
        # 真实姓名
        self.realname = None
        # 审批领导登录帐号
        self.leader_username = None
        # 审批领导真实姓名
        self.leader_realname = None
        # 审批领导邮件地址
        self.leader_email = None
        # 审批领导联系方式
        self.leader_phone = None
        # 审批领导角色
        self.leader_roles = None
        # 审批领导角色ID 列表
        self.leader_role_ids = None


def user2Extend(users):
    user_list = []
    for item in users:
        user_list.append(getUser(item.id))
    return user_list

# 获取用户
def getUser(user_id):
    auth_user = User.objects.get(id=user_id)
    if not auth_user:
        return None
    user = UserExtend()
    user.id = auth_user.id
    user.username = auth_user.username
    user.email = auth_user.email
    user.department = auth_user.userprofile.department 
    user.phone = auth_user.userprofile.phone
    user.realname = auth_user.userprofile.realname
    user.leader_username = auth_user.userprofile.leader_username
    user.leader_realname = auth_user.userprofile.leader_realname
    user.leader_email = auth_user.userprofile.leader_email
    user.leader_phone = auth_user.userprofile.leader_phone
    
    role_list = auth_user.role_set.all()
    user.roles = ",".join([item.name for item in role_list])
    user.role_ids = [item.id for item in role_list]
    
    leader_users = User.objects.filter(username__iexact=auth_user.userprofile.leader_username)
    if leader_users:
        leader_user = leader_users[0]
        leader_role_list = leader_user.role_set.all()
        user.leader_roles = ",".join([item.name for item in leader_role_list])
        user.leader_role_ids = [item.id for item in leader_role_list]
    
    return user
    
