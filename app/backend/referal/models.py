from django.db import models
from loginregister.models import User

# Create your models here.

class Referal(models.Model):
    id = models.BigIntegerField(primary_key = True)
    # The user that created it
    user_id = models.BigIntegerField(null = False, blank = False)
    date_created = models.DateTimeField(null = False, blank = False)
    value = models.CharField(null = False, blank = False, max_length = 10)
    userid_redeem = models.ForeignKey(User, null = True, blank = False, default = None, on_delete = models.SET_NULL)

    class Meta:
        db_table = 'referals'
        indexes = [models.Index(fields = ['user_id'])]