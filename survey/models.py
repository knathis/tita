#encoding: utf-8
from django.db import models
from django.core.exceptions import ValidationError
from campus.models import InstitucionEducativa
from convocat.models import Municipio

class Survey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    def __unicode__(self):
        return (self.name)

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None

class Category(models.Model):
    class Meta:
        ordering = ('number',)

    name = models.CharField(max_length=400)
    number = models.IntegerField(null=True)
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return (self.name)

def validate_list(value):
    '''takes a text value and verifies that there is at least one comma '''
    values = value.split('\n')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
    class Meta:
        ordering = ('number',)
        unique_together = (('survey','number') ,)

    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
    )
    
    number = models.CharField(max_length=10)

    text = models.TextField()
    required = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True,) 
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    # the choices field is only used if the question type 
    choices = models.TextField(blank=True, null=True,
        help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT 
            or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.'''
        choices = self.choices.split('\n')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c,c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return "%s - %s"%(self.id,self.text)


class Response(models.Model):
    # a response object is just a collection of questions and answers with a
    # unique interview uuid
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)
    
    #jornada = models.CharField(max_length=1, choices=(('M',u'(1) Mañana'),('T', '(2) Tarde')))
    #numero_documento = models.BigIntegerField()
    #nombre = models.CharField(max_length=300, verbose_name=u'Nombres y Apellidos')
    #institucion = models.ForeignKey(InstitucionEducativa)
    #fecha_nacimiento = models.DateField()
    #municipio_nacimiento = models.ForeignKey(Municipio, null=True, blank=True)    
    #barrio = models.CharField(max_length=100, verbose_name=u'Barrio donde reside actualmente')
    
   
    def __unicode__(self):
        return ("response %s" % self.id)

class AnswerBase(models.Model):
    class Meta:
        abstract=True
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)








