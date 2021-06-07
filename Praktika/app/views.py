"""
Definition of views.
"""

from datetime import datetime
from datetime import date
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import workers
from .models import spec
from .models import empl
from .models import company
#from .forms import market_form

# получение данных из бд
class work_vivod:
	def __init__(self,name,surname,patr,sex,date,ed,school,spec,stage,jobs):
		self.name=name
		self.fam=surname
		self.otch=patr
		self.sex=sex
		self.date=date
		self.ed= ed
		self.school=school
		self.spec=spec
		self.stage=stage
		self.jobs=jobs

def Workers(request):
    specs = spec.objects.all()   
    people = workers.objects.all()
    return render(
        request, 
        'app/Workers.html', 
        {
            'title':'Workers Page',
            'people': people,
            'specs' : specs
        }
    )


def Works(request):
    IWork()
    people = workers.objects.all() 
    vivod=[]
    for i in people:
      works = empl.objects.get(person_id=i.id).spec_id
      jobs=[]
      for j in works:
        strocka=""
        strocka+=spec.objects.get(id_spec=j).name
        if j!=0:
          comp=company.objects.all()
          for com in comp:
            if j in com.spec_id:
              strocka+=" "+'-'+" "+"'"+com.name+"'"
        jobs.append(strocka)
      new=work_vivod(i.name,i.fam,i.otch,i.sex,HowOld(date.today(),i.date),i.ed,i.school,i.spec,i.stage,jobs)
      vivod.append(new)
    return render(
        request, 
        'app/Works.html', 
        {
            'title':'Works Page',
            'people': people,
			'vivod' : vivod,
        }
    )
 
# сохранение данных в бд
def create(request):
    if request.method == "POST":
        worker = workers()
        worker.fam = request.POST.get("fam").capitalize()
        worker.name = request.POST.get("name").capitalize()
        worker.otch = request.POST.get("otch").capitalize()
        worker.sex = request.POST.get("sex").capitalize()
        worker.date = request.POST.get("date")
        worker.adres = request.POST.get("adres").capitalize()
        worker.ed = request.POST.get("ed").capitalize()
        worker.school = request.POST.get("school").capitalize()
        worker.spec = request.POST.get("spec").capitalize()
        worker.stage = request.POST.get("stage")
        worker.add_abil = request.POST.get("add_abil").lower()
        worker.reasons = request.POST.get("reasons").lower()
        worker.save()
        Jobs()
    return HttpResponseRedirect("/work")


class Firma:
	def __init__(self,name,adr,job_info):
		self.name=name
		self.adr=adr
		self.job=job_info

def Home(request):
    Firm=[]
    compan = company.objects.all()
    for i in compan:
     job=[]
     for j in i.spec_id:
      strocka=""
      work_name=spec.objects.get(id_spec=j)
      strocka+=work_name.name
      strocka+=" "+"-"+" "+str(work_name.price)
      #if (j!=len(i.spec_id)):
       #job+=""
      job.append(strocka)
     new=Firma(i.name,i.adres,job)
     Firm.append(new)
    return render(
        request, 
        'app/HomePage.html', 
        {
            'title':'Firms Page',
            'firms': Firm
        }
    )

def HowOld(now,birth):
	age=now.year - birth.year
	if now.month < birth.month:
		age -=1
	elif now.month == birth.month and now.day < birth.day:
		age -= 1
	return age

education_position={"Нет":0,"Неполное среднее":1,"Среднее":2,"Неполное высшее":3,"Высшее":4}

def JobList(jobs,people):
	JobsList=[];
	for i in jobs:
		Ready=True #флаг подходит ли нам работа
		for k in i.conditions: #кондиция это массив строк, смотрим по каждей
			k=k.capitalize() #приводим к формату большая буква
			if(k.find("Age")!=-1): #проверка по возрасту 
				age = HowOld(date.today(),people.date)
				age_need=int(k[4:])
				if (k[3:4]==">"):
					if (age<age_need): 
						Ready=False #слишком старый, работать не будет
						break
				else:
					if (age>age_need): 
						Ready=False #слишком молодой, работать не будет
						break
			if(k.find("Sex")!=-1): #Если параметр это пол человека
				if(k[4:].capitalize()!=people.sex):
						Ready=False
						break
			if(k.find("Education")!=-1):#Если нужно иметь опеределнное образование
				if(education_position[k[10:].capitalize()]>education_position[people.ed.capitalize()]):
						Ready=False
						break
			if(k.find("Speciality")!=-1):#Если нужно иметь специальность 
				if(k[11:].capitalize()!=people.spec):
						Ready=False
						break
			if(k.find("Experience")!=-1):
					if people.stage is None:#стажа нет
						Ready=False
						break
					elif(int(k[11:])>int(people.stage)):#стаж меньше нужного
						Ready=False
						break
			if(k.find("School")!=-1):#Если нужно окончить специальное заведение
				if(k[7:].capitalize()!=people.school):
						Ready=False
						break
			if((k.find("Other")!=-1)and(not(people.reasons is None))):#строка other содержит вредные привычки, с которыми человек не может работать в данной компании
				Bad_behaiv=k[6:].split(';')#если человек имеет данные привычки - он не получает рабочее место 
				for habits in Bad_behaiv:
					if(people.reasons.find(habits.lower())!=-1):
						Ready=False
						break
			if((k.find("Perks")!=-1)and(people.add_abil is None)):#Если на работе требуются особые навыки, а у человека их совсем нет
				Ready=False
				break
			if((k.find("Perks")!=-1)and(not(people.add_abil is None))):#Если на работе требуются особые навыки, тоже самое что и с привычками
				abilities=k[6:].split(';')
				for perk in abilities:
					if(people.add_abil.find(perk.lower())==-1):
						Ready=False
						break
		if (Ready):
			JobsList.append(i.id_spec)
	if len(JobsList)==0:
	 JobsList.append(0)
	return JobsList

def IWork():
    jobs= spec.objects.all()
    emplor=empl.objects.all()
    for i in emplor:
        people=workers.objects.get(id=i.person_id)
        i.spec_id=JobList(jobs,people)
        i.save()
        
def Jobs():
	Error=''
	people = workers.objects.last() #получаем информацию о последнем работнике
	jobs= spec.objects.all()
	emplor=empl()
	emplor.person_id=people.id
	emplor.spec_id=JobList(jobs,people); 
	emplor.save()
	return HttpResponse("Ты красавчик!")

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
