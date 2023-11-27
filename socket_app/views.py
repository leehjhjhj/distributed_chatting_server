from django.shortcuts import render



def test_index(request, chat_id, token):
    return render(request, "example.html", {
        "chat_id": chat_id,
        "token": token
    })