from django.db import models
# 模型Model 用于定义数据库结构
# 类名 对应数据库表名
# 类属性 对应表字段
# 类方法 对应数据库操作
# 对象 对应数据库记录
# models表结构一旦改变，需要重新迁移数据库
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:  # 元数据 用于配置模型类
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ProblemData(models.Model):
    ID = models.CharField(max_length=255, primary_key=True)
    Title = models.CharField(max_length=255, blank=True, null=True)
    Tags = models.CharField(max_length=255, blank=True, null=True)
    Rating = models.IntegerField(null=True, blank=True)
    Solved = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'problem_set'
        verbose_name_plural = verbose_name = '题目表'  # 设置后台显示的名称

    def __str__(self):  # 重写__str__方法 使得后台显示的是name字段 而不是object
        ID = str(self.ID)
        Title = str(self.Title)
        Tags = str(self.Tags)
        Rating = str(self.Rating)
        return '-'.join([ID, Title, Tags, Rating])  # 显示该表的字段 以-分割
    def __getitem__(self, key):
        return getattr(self, key)

class SendList(models.Model):
    send_id = models.AutoField(primary_key=True)
    problem = models.ForeignKey('problemData', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserList', models.DO_NOTHING, blank=True, null=True)
    submission_count = models.IntegerField(default=0)  # 图片中的submission counting
    ac_count = models.IntegerField(default=0)  # 图片中的ac COUNT
    class Meta:
        managed = False
        db_table = 'accept_list'
        verbose_name_plural = verbose_name = '提交信息表'  # 设置后台显示的名称

    def __str__(self):
        send_id = str(self.send_id)
        problem = str(self.problem)
        user = str(self.user)
        return '-'.join([send_id, problem, user])  # 显示该表的字段



class SpiderInfo(models.Model):
    spider_id = models.AutoField(primary_key=True)
    spider_name = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spider_info'


class UserExpect(models.Model):
    expect_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserList', models.DO_NOTHING, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_expect'
        verbose_name_plural = verbose_name = '用户期望表'  # 设置后台显示的名称

    def __str__(self):
        expect_id = str(self.expect_id)
        user = str(self.user)
        tag = str(self.tag)
        return '-'.join([expect_id, user, tag])


class UserList(models.Model):
    user_id = models.CharField(primary_key=True, max_length=11)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    pass_word = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False  # 指示 Django 是否应该管理该模型的数据库表。由于设置为 False，Django 将不会为该模型创建数据库表，也不会对其进行数据库迁移操作
        db_table = 'user_list'  # 指定数据库表的名称
        verbose_name_plural = verbose_name = '用户信息表'  # 设置后台显示的名称

    def __str__(self):  # 重写__str__方法 ，用于返回模型对象的字符串表示 将用户的 user_id 和 user_name 拼接起来，以 - 分隔，作为模型对象的字符串表示
        user_id = str(self.user_id)
        user_name = str(self.user_name)
        rating = str(self.rating)
        return '-'.join([user_id, user_name, rating])
