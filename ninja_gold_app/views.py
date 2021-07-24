from django.shortcuts import render, HttpResponse, redirect
import random
from time import localtime, strftime, gmtime

def index(request):
    if 'gold_amt' not in request.session or 'gold' not in request.session or 'activities' not in request.session:
        request.session['gold_amt'] = 0
        request.session['activities'] = []
        request.session['gold'] = { 'farm':0,
                                    'cave':0,
                                    'house':0,
                                    'casino':0,
                                }
    
    context = {
        'gold' : request.session['gold'],
        # next line is from me testing what would work and didn't
        # 'farm': request.session['random.randint(0,50)'],
    }
    return render(request, 'index.html', context ) 

def process_money(request):
    request.session['gold'] = {
        'farm' :  random.randint(10,20),
        'cave' : random.randint(5, 10),
        'house' : random.randint(2,5),
        'casino' : random.randint(-50,50),
    }
    # to utilize the POST item it needs to be in the method processing the POST item
    casino_sign = True
    if request.method == "POST":
        if request.POST['area'] == 'farm':
            earned_money = request.session['gold']['farm']
            current_area = request.POST['area']
        if request.POST['area'] == 'cave':
            earned_money = request.session['gold']['cave']
            current_area = request.POST['area']
        if request.POST['area'] == 'house':
            earned_money = request.session['gold']['house']
            current_area = request.POST['area']
        if request.POST['area'] == 'casino':
            earned_money = request.session['gold']['casino']
            current_area = request.POST['area']
            if request.session['gold']['casino'] < 0:
                casino_sign = False
    request.session['gold_amt'] += earned_money 
    time = strftime('%A %B %d %H:%M %p')
    
    if casino_sign == True:
        update = f"You gained {earned_money} Gold at the {current_area} on {time} "
        
    if casino_sign == False:
        update = f"You lost {earned_money} Gold at the {current_area} on {time}"
    
    request.session['activities'].append(update)
    return  redirect('/')


def reset(request):
    request.session.flush()
    return redirect('/')