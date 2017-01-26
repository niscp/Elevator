from django.shortcuts import render
from . import elevator_allocation as e
# Create your views here.


def index(request):
    c = {}
    if request.method == "POST":
        count = int(request.POST.get("count"))
        mylist = []
        alist = [request.POST.get("first0"),
                 request.POST.get("second0"),
                 request.POST.get("third0"),
                 request.POST.get("four0"),
                 ]
        mylist.append(alist)
        if count:
            for x in range(count):
                first = request.POST.get("first"+str(x))
                second = request.POST.get("second" + str(x))
                third = request.POST.get("third" + str(x))
                four = request.POST.get("four" + str(x))
                alist = [first,int(second),int(third),int(four)]
                mylist.append(alist)
        print mylist
        c['answer'],c['msg'] = e.start_work(mylist)
    return render(request, 'index.html', c)