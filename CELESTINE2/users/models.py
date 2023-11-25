from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator, int_list_validator
from datetime import date
# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=13)
    unit=models.CharField(max_length=100,default='Null')


class Units(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Clubs(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Students(models.Model):
    name=models.CharField(max_length=50)
    units=models.ManyToManyField(Units)
    clubs=models.ManyToManyField(Clubs)
    phone_no = models.CharField(verbose_name="Phone number", max_length=10,
    validators=[int_list_validator(sep=''),MinLengthValidator(10),], 
    default='07xxx')
    email=models.EmailField(max_length = 254)
    def __str__(self):
        return self.name


      
class Python(models.Model):
    name=models.OneToOneField(Students, on_delete=models.CASCADE)
    reg=models.IntegerField(default=0,primary_key=True)
    cat1=models.IntegerField(default=0)
    cat2=models.IntegerField(default=0)
    cat3=models.IntegerField(default=0)
    
    hours=models.IntegerField(default=0)
    prediction=models.CharField(max_length=4,default='NULL')
    @property
    def total(self):
        return (self.cat1+self.cat2+self.cat3)
    def __str__(self):
        return str(self.name)
class Java(models.Model):
    name=models.OneToOneField(Students, on_delete=models.CASCADE)
    reg=models.IntegerField(default=0,primary_key=True)
    cat1=models.IntegerField(default=0)
    cat2=models.IntegerField(default=0)
    cat3=models.IntegerField(default=0)
    hours=models.IntegerField(default=0)
    prediction=models.CharField(max_length=4,default='NULL')
    @property
    def total(self):
        return (self.cat1+self.cat2+self.cat3)
    def __str__(self):
        return str(self.name)
class Sql(models.Model):
    name=models.OneToOneField(Students, on_delete=models.CASCADE)
    reg=models.IntegerField(default=0,primary_key=True)
    cat1=models.IntegerField(default=0)
    cat2=models.IntegerField(default=0)
    cat3=models.IntegerField(default=0)
    hours=models.IntegerField(default=0)
    prediction=models.CharField(max_length=4,default='NULL')
    @property
    def total(self):
        return (self.cat1+self.cat2+self.cat3)
    def __str__(self):
        return str(self.name)
class Javascript(models.Model):
    name=models.OneToOneField(Students, on_delete=models.CASCADE)
    reg=models.IntegerField(default=0,primary_key=True)
    cat1=models.IntegerField(default=0)
    cat2=models.IntegerField(default=0)
    cat3=models.IntegerField(default=0)
    hours=models.IntegerField(default=0)
    prediction=models.CharField(max_length=4,default='NULL')
    @property
    def total(self):
        return (self.cat1+self.cat2+self.cat3)
    def __str__(self):
        return str(self.name)
class Php(models.Model):
    name=models.OneToOneField(Students, on_delete=models.CASCADE)
    reg=models.IntegerField(default=0,primary_key=True)
    cat1=models.IntegerField(default=0)
    cat2=models.IntegerField(default=0)
    cat3=models.IntegerField(default=0)
    hours=models.IntegerField(default=0)
    prediction=models.CharField(max_length=4,default='NULL')
    @property
    def total(self):
        return (self.cat1+self.cat2+self.cat3)
    def __str__(self):
        return str(self.name)
class pythonAttendance(models.Model):
    reg=models.IntegerField(default=0)
    name=models.CharField(max_length=300)
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
    SEVEN=7
    EIGHT=8
    NINE=9
    TEN=10
    ELEVEN=11
    TWELVE=12
    TIMEHRS=[
        (ONE,1),
        (TWO,2),
        (THREE,3),
        (FOUR,4),
        (FIVE,5),
        (SIX,6),
        (SEVEN,7),
        (EIGHT,8),
        (NINE,9),
        (TEN,10),
        (ELEVEN,11),
        (TWELVE,12)
    ]
    YES='YES'
    NO='NO'
    PRESENT=[
        (YES,'YES'),
        (NO,'NO')
    ]
    From_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    To_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    present=models.CharField(max_length=50,choices=PRESENT,default=YES)
    sumhrs=models.IntegerField(default=0)
    date=models.DateField(blank=True, null=True)
    # @property
    def save(self):
        self.sumhrs=self.To_hrs-self.From_hrs
        return super(pythonAttendance, self).save()
class jsAttendance(models.Model):
    reg=models.IntegerField(default=0)
    name=models.CharField(max_length=300)
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
    SEVEN=7
    EIGHT=8
    NINE=9
    TEN=10
    ELEVEN=11
    TWELVE=12
    TIMEHRS=[
        (ONE,1),
        (TWO,2),
        (THREE,3),
        (FOUR,4),
        (FIVE,5),
        (SIX,6),
        (SEVEN,7),
        (EIGHT,8),
        (NINE,9),
        (TEN,10),
        (ELEVEN,11),
        (TWELVE,12)
    ]
    YES='YES'
    NO='NO'
    PRESENT=[
        (YES,'YES'),
        (NO,'NO')
    ]
    From_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    To_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    present=models.CharField(max_length=50,choices=PRESENT,default=YES)
    sumhrs=models.IntegerField(default=0)
    date=models.DateField(blank=True, null=True)
    # @property
    def save(self):
        self.sumhrs=self.To_hrs-self.From_hrs
        return super(jsAttendance, self).save()
class sqlAttendance(models.Model):
    reg=models.IntegerField(default=0)
    name=models.CharField(max_length=300)
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
    SEVEN=7
    EIGHT=8
    NINE=9
    TEN=10
    ELEVEN=11
    TWELVE=12
    TIMEHRS=[
        (ONE,1),
        (TWO,2),
        (THREE,3),
        (FOUR,4),
        (FIVE,5),
        (SIX,6),
        (SEVEN,7),
        (EIGHT,8),
        (NINE,9),
        (TEN,10),
        (ELEVEN,11),
        (TWELVE,12)
    ]
    YES='YES'
    NO='NO'
    PRESENT=[
        (YES,'YES'),
        (NO,'NO')
    ]
    From_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    To_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    present=models.CharField(max_length=50,choices=PRESENT,default=YES)
    sumhrs=models.IntegerField(default=0)
    date=models.DateField(blank=True, null=True)
    # @property
    def save(self):
        self.sumhrs=self.To_hrs-self.From_hrs
        return super(sqlAttendance, self).save()
class phpAttendance(models.Model):
    reg=models.IntegerField(default=0)
    name=models.CharField(max_length=300)
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
    SEVEN=7
    EIGHT=8
    NINE=9
    TEN=10
    ELEVEN=11
    TWELVE=12
    
    TIMEHRS=[
        (ONE,1),
        (TWO,2),
        (THREE,3),
        (FOUR,4),
        (FIVE,5),
        (SIX,6),
        (SEVEN,7),
        (EIGHT,8),
        (NINE,9),
        (TEN,10),
        (ELEVEN,11),
        (TWELVE,12)
    ]
    YES='YES'
    NO='NO'
    PRESENT=[
        (YES,'YES'),
        (NO,'NO')
    ]
    From_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    To_hrs=models.IntegerField(choices=TIMEHRS,default=ONE)
    present=models.CharField(max_length=50,choices=PRESENT,default=YES)
    sumhrs=models.IntegerField(default=0)
    date=models.DateField(blank=True, null=True)
    # @property
    def save(self):
        self.sumhrs=self.To_hrs-self.From_hrs
        return super(phpAttendance, self).save()



def studentPostSave(sender, instance,created,*args,**kwargs):
    if created:
        print(instance.units.count())
        # r=Results(name=instance)
        # r.save()
        # a=Attendance(name=instance)
        # a.save()
        # print(instance.name + "created successfully.")
post_save.connect(studentPostSave,sender=Students)