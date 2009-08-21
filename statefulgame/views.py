from statefulgame.models import Submission, Turn

# saves an assignment blob to the database
def save_assignment(request):
    data = request.POST['data']
    turn_id = request.POST['turn_id']
    turn = Turn.objects.get(id=turn_id)
    submission = Submission.objects.get_or_create(turn=turn_id)
    submission.data = data
    submission.save()