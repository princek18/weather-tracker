from django.shortcuts import render, redirect
from Train_app.forms import PassengerForm
from django.forms import formset_factory
from random import randint
from Train_app.models import TicketModel, PassengerModel
from bs4 import BeautifulSoup
import urllib.request
import re
import datetime
import calendar

# Create your views here.
def index(request):

    def findDay(date):
        date1 = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return (calendar.day_name[date1])


    day_count = {"Sunday":1, "Monday":2, "Tuesday":3, "Wednesday":4, "Thursday":5, "Friday":6, "Saturday":7}

    if request.method == "POST":
        origin = request.POST.get("origin")
        destination = request.POST.get("destination")
        date = request.POST.get("date")
        day = findDay(date)
        try:
            url = "https://etrain.info/trains/" + origin.upper() + "-to-" + destination.upper()
            r = urllib.request.urlopen(url)
            soup = BeautifulSoup(r.read(), 'html5lib')
            tag = soup.find_all("tr", {"class": "odd"})
            tag1 = soup.find_all("tr", {"class": "even"})
            a = []
            b = []
            c = []
            f = []
            cl = []
            ch = {}
            price = {}

            for i in tag:
                for j in i.find_all("a"):
                    k = re.findall(">(.*)<", str(j))
                    if len(k[0]) == 2:
                        cl.append(k[0])
                    else:
                        a.append(k[0])
                count = 0
                for j in i.find_all('td'):
                    k = re.findall(">(.*)<", str(j))
                    if k[0] == "X" or k[0] == "Y":
                        count += 1
                    if count == 8:
                        break
                    else:
                        if len(k[0]) < 20:
                            a.append(k[0])
                        if k[0] == 'UNRESERVED TRAIN':
                            a.pop(len(a)-1)
                for j in i.find_all("td", {"class": 'wd19'}):
                    y = re.findall(";₹ ([0-9]*)&", str(j))
                    if len(y) != 0:
                        c.append(y)
                if len(cl) == len(c):
                    for g in range(len(cl)):
                        ch[cl[g]] = c[g]
                else:
                    for g in range(len(c)):
                        ch[cl[g]] = c[g]
                price[a[0]] = ch
                b.append(a)
                a = []
                c = []
                cl = []
                ch = {}

            for i in tag1:
                for j in i.find_all("a"):
                    k = re.findall(">(.*)<", str(j))
                    if len(k[0]) == 2:
                        cl.append(k[0])
                    else:
                        a.append(k[0])
                count = 0
                for j in i.find_all('td'):
                    k = re.findall(">(.*)<", str(j))
                    if k[0] == "X" or k[0] == "Y":
                        count += 1
                    if count == 8:
                        break
                    else:
                        if len(k[0]) < 20:
                            a.append(k[0])
                        if k[0] == 'UNRESERVED TRAIN':
                            a.pop(len(a)-1)
                for j in i.find_all("td", {"class": 'wd19'}):
                    y = re.findall(";₹ ([0-9]*)&", str(j))
                    if len(y) != 0:
                        c.append(y)
                if len(cl) == len(c):
                    for g in range(len(cl)):
                        ch[cl[g]] = c[g]
                else:
                    for g in range(len(c)):
                        ch[cl[g]] = c[g]
                price[a[0]] = ch
                b.append(a)
                a = []
                c = []
                cl = []
                ch = {}
            for i in b:
                if i[6+day_count[day]] == "Y":
                    f.append(i)
        except:
            f = []
            price = {}
            date = ""
            day = ""
    else:
        f = []
        price = {}
        date = ""
        day = ""
    datev = []
    datev.append(date)
    datev.append(day)
    request.session['my'] = f
    request.session['my1'] = price
    request.session['my2'] = datev
    return render(request, "Train_app/index.html", {'b': f})


def PassView(request, pk):
    f = request.session['my']
    price = request.session['my1']
    datev = request.session['my2']
    k = []
    p = {}
    if len(str(pk)) == 4:
        pk = '0'+str(pk)
    for i in f:
        if i[0] == str(pk):
            k.extend(i)
            break
    k.extend(datev)
    for i in price:
        if i == str(pk):
            p = price[i]

    if request.method == "POST":
        number = request.POST.get("number")
        classp = request.POST.get("classp")
        if number != None:
            request.session['num'] = number
            request.session['cla'] = classp
        request.session['data'] = k
        request.session['data1'] = p

        return redirect('ticketView')

    return render(request, "Train_app/passView.html", {"k":k, "p":p})


def ticketView(request):
    number = request.session['num']
    classp = request.session['cla']
    k = request.session['data']
    p = request.session['data1']
    PassengerFormSet = formset_factory(PassengerForm, extra=int(number))
    form = PassengerFormSet()

    if request.method == "POST":
        id = randint(11111,99999)
        form = PassengerFormSet(request.POST)
        t = TicketModel(Ticket_id=id,Train_number=k[0], Train_name=k[1], Origin=k[2], Departure=k[3],
                        Destination=k[4], Arrival=k[5], Travel_time=k[6], Date=k[14],
                        Day=k[15], Class=classp, Price=str(int(number)*int(p[classp][0])))
        t.save()

        if form.is_valid():
            for i in form:
                dumy = i.save(commit=False)
                dumy.ticket = t
                dumy.save()

            request.session['ii'] = id
            return redirect('reviewView')


    return render(request, 'Train_app/ticket.html', {"k":k, "p":p, 'form':form, 'number':number, 'classp':classp} )

def reviewView(request):
    passengers_t = []
    id = request.session['ii']
    ticket = TicketModel.objects.get(Ticket_id=id)
    passengers = PassengerModel.objects.all()
    for i in passengers:
        if str(i.ticket) == str(id):
            passengers_t.append(i)
    if request.method == "POST":
        payment = request.POST.get("payment")
        ticket.Status = "Booked"
        ticket.Payment = payment
        ticket.save()

        return redirect('booked')


    return render(request, "Train_app/review.html", {'ticket':ticket, 'passengers':passengers_t})

def booked(request):
    id = request.session['ii']
    passengers_t = []
    ticket = TicketModel.objects.get(Ticket_id=id)
    passengers = PassengerModel.objects.all()
    for i in passengers:
        if str(i.ticket) == str(id):
            passengers_t.append(i)

    return render(request, "Train_app/booked.html", {'ticket':ticket, "passengers":passengers_t})

def history(request):
    ticket = TicketModel.objects.all().order_by("Date")
    return render(request, "Train_app/history.html", {'ticket': ticket})


def bookhis(request, pk):
    passengers = PassengerModel.objects.all()
    ticket = TicketModel.objects.get(Ticket_id=pk)
    passenger = []
    for i in passengers:
        if str(i.ticket) == str(pk):
            passenger.append(i)

    return render(request, "Train_app/bookhis.html", {"passenger": passenger, "ticket": ticket})
