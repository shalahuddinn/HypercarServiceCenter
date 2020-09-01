from django.views import View
from django.http.response import HttpResponse
from collections import deque
from django.shortcuts import render, redirect



class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        html = "<html><body><h2>Welcome to the Hypercar Service!</h2></body></html>"
        return HttpResponse(html)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', {})


class GetTicketView(View):
    counter = list()
    queue = list()

    def get(self, request, *args, **kwargs):
        self.counter.append(1)
        if request.path == "/get_ticket/change_oil":
            element = {
                "service": 2,
                "ticket_number": len(self.counter)
            }
            self.queue.append(element)
        elif request.path == "/get_ticket/inflate_tires":
            element = {
                "service": 5,
                "ticket_number": len(self.counter)
            }
            self.queue.append(element)
        elif request.path == "/get_ticket/diagnostic":
            element = {
                "service": 30,
                "ticket_number": len(self.counter)
            }
            self.queue.append(element)

        lengthQueue = len(self.queue)

        if lengthQueue <= 2:
            time = 0
        elif lengthQueue == 3:
            time = min(self.queue[0]['service'], self.queue[1]['service'])
        else:
            time = 0
            for x in self.queue:
                time += x['service']
                
        context = {
            "number": element['ticket_number'],
            "time": time
        }
        print(self.counter)

        return render(request, 'tickets/ticket.html', context)


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        change_oil = 0
        inflate_tires = 0
        get_diagnostic = 0

        for x in GetTicketView.queue:
            if x['service'] == 2:
                change_oil += 1
            elif x['service'] == 5:
                inflate_tires += 1
            elif x['service'] == 30:
                get_diagnostic += 1

        context = {
            "change_oil": change_oil,
            "inflate_tires": inflate_tires,
            "get_diagnostic": get_diagnostic
        }

        return render(request, 'tickets/process.html', context)

    def post(self, request, *args, **kwargs):
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        if len(GetTicketView.queue) > 2:
            try:
                next_Ticket = next(item for item in GetTicketView.queue if item["service"] == 2)
                html = f"<html><body><div>Next ticket #{next_Ticket['ticket_number']}</div></body></html>"
                GetTicketView.queue.remove(next_Ticket)
            except:
                try:
                    next_Ticket = next(item for item in GetTicketView.queue if item["service"] == 5)
                    html = f"<html><body><div>Next ticket #{next_Ticket['ticket_number']}</div></body></html>"
                    GetTicketView.queue.remove(next_Ticket)
                except:
                    try:
                        next_Ticket = next(item for item in GetTicketView.queue if item["service"] == 30)
                        html = f"<html><body><div>Next ticket #{next_Ticket['ticket_number']}</div></body></html>"
                        GetTicketView.queue.remove(next_Ticket)
                    except:
                        html = ""
                #
                #
                # if x['service'] == 2:
                #     change_oil += 1
                # elif x['service'] == 5:
                #     inflate_tires += 1
                # elif x['service'] == 30:
                #     get_diagnostic += 1
            # if GetTicketView.queue.count(2) != 0:
            #     next = GetTicketView.queue.index(2)
            # elif GetTicketView.queue.count(5) != 0:
            #     next = GetTicketView.queue.index(5)
            # elif GetTicketView.queue.count(30) != 0:
            #     next = GetTicketView.queue.index(30)
            # GetTicketView.queue.pop(next)
            # html = f"<html><body><div>Next ticket #</div></body></html>"
        else:
            html = "<html><body><div>Waiting for the next client</div></body></html>"
        return HttpResponse(html)





