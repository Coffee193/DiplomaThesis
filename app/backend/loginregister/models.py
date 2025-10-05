from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

USER_STATUS = [
    ('A', 'ACTIVE'),
    ('D', 'DELETED'),
]

class User(models.Model):
    email = models.CharField(max_length = 255, null = True, blank = True)
    phone = models.CharField(null = True, blank = True, max_length = 25)
    password = models.CharField(max_length = 97, null = False)
    id = models.BigIntegerField(primary_key = True)

    #date_created = models.DateTimeField(default = datetime.datetime.utcnow().replace(tzinfo=None), null = False)
    date_created = models.DateTimeField(null = False)
    status = models.CharField(max_length = 1, null = False, choices = USER_STATUS, default = 'A')

    name = models.CharField(max_length = 7, default = None, null = True)

    # CHANGE id AND date_created. Django default IS RUN ONCE WHEN SERVER STARTS python manage.py runserver!!! default
    # DOES NOT RUN WHEN MODEL IS CREATED! AS A RESULT YOU'LL GET  ERRORS THAT PRIMARY KEY id ALREADY EXISTS
    # THESE CURRENTLY ARE:
    # id = models.BigIntegerField(primary_key = True, default = GenerateSnowflake())
    # date_created = models.DateTimeField(default = datetime.datetime.utcnow(), null = False)

    is_admin = models.BooleanField(null = False, blank = False, default = False)

    img = models.BooleanField(blank = False, default = False, null = False)

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.phone
        
    class Meta:
        db_table = 'users'
        indexes = [models.Index(fields = ['id', 'phone', 'email'])]

class Referal(models.Model):
    referal_code = models.CharField(max_length = 10, validators = [MinLengthValidator(10)], null = False, primary_key = True)
    # UK Gov suggests 35 # https://webarchive.nationalarchives.gov.uk/ukgwa/20100407120701/http://cabinetoffice.gov.uk/govtalk/schemasstandards/e-gif/datastandards.aspx
    # https://www.researchgate.net/figure/First-names-and-last-names-lengths-distributions_fig1_328894441 # this paper suggest the below vals
    first_name = models.CharField(max_length = 20, null = False, blank = False)
    last_name = models.CharField(max_length = 30, null = False, blank = False)
    status = models.CharField(max_length = 1, null = False, choices = USER_STATUS)
    date_created = models.DateTimeField(null = False)

    def __str__(self):
        return self.referal_code + '_' + self.first_name + '_' + self.last_name + '_' + self.status
    
    class Meta:
        db_table = 'referal_codes'