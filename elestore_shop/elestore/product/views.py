from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from product.models import CommentForm, Comment
def index(request):
    return HttpResponse("My product pâgw")
def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.comment = form.cleaned_data['comment']

         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Bài đánh giá của bạn đã được duyệt,Cảm ơn vì đã gửi đánh giá.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)