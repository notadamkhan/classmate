from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from home.models import Class, Profile, StudySession, Message, User
import requests, json, datetime
from home.forms import StudySessionForm
from algoliasearch_django import raw_search
from datetime import datetime as dtc

def index(request):
    return render(request, 'home.html')

def onboarding(request):
    if not request.user.is_authenticated:
        return redirect('index')
    foundClasses = []
    curUser = request.user.Profile
    enrolled_classes = list(curUser.classes.all())
    if (request.method == "POST") and not (request.POST.get('dept').upper() == "") and not (request.POST.get('classNum') == ""):
        responseURL = "http://luthers-list.herokuapp.com/api/dept/" + request.POST.get('dept').upper() + "/?format=json"
        response_API = requests.get(responseURL)
        responseAPIText = response_API.text
        responseAPIJson = json.loads(responseAPIText)
        for foundClass in responseAPIJson:
            if (foundClass["catalog_number"] == request.POST.get('classNum')):
                classInfo = []
                classInfo.append(foundClass["instructor"]['name'])
                classInfo.append(foundClass["description"])
                classInfo.append(foundClass["meetings"][0]['days'])
                classInfo.append(foundClass["meetings"][0]['start_time'][:5].replace(".",":"))
                classInfo.append(foundClass["meetings"][0]['end_time'][:5].replace(".",":"))
                classInfo.append(foundClass["meetings"][0]['facility_description'])
                classInfo.append(foundClass["component"])
                foundClasses.append(classInfo)
    return render(request, 'onboarding.html', {'classes': foundClasses, 'department': request.POST.get('dept'), 'catalog_number':request.POST.get('classNum'), 'enrolledclasses': enrolled_classes, 'preferencesSet': curUser.preferencesSet})


def namingChanges(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        if request.user.first_name and request.user.last_name:
            return render(request, "naming_change.html", {'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
        else:
            return render(request, "naming_change.html", {'username': "username", 'first_name': "First Name", 'last_name': "Last Name"})
    if request.method == 'POST':
        if ((request.POST.get("first_name") == "") or (request.POST.get("last_name") == "") or (request.POST.get("username") == "") or ((User.objects.filter(username=request.POST.get("username")).exists()) and (request.POST.get("username") != request.user.username))):
            return redirect('namingChanges')
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.username = request.POST.get("username")
        request.user.Profile.nameSet = True
        request.user.save()
        if not (request.user.Profile.editProfile):
            return redirect('dashboard')
        else:
            return redirect('getProfile', request.user.Profile.id)


def addClass(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    className = request.GET.get('department') + " " + request.GET.get('catalogNum')
    newClass = Class.objects.get_or_create(class_name=className,department=request.GET.get('department'), catalog_number = request.GET.get('catalogNum'), instructor=request.GET.get('instr'), description=request.GET.get('desc'), days=request.GET.get('days'), start_time=request.GET.get('start'), end_time=request.GET.get('end'), location=request.GET.get('loc'), component=request.GET.get('comp'))
    user.classes.add(newClass[0])
    user.classesSet=True
    user.save()
    return redirect('setClasses')

def removeClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    foundClass = Class.objects.get(id=pk)
    user.classes.remove(foundClass)
    user.save()
    return redirect('setClasses')

def Friend(request):
    if not request.user.is_authenticated:
        return redirect('index')
    foundFriends = []
    user = request.user.Profile
    curUserID = user.id
    friend_list = list(user.friendsList.all())
    if request.POST.get('friendz'):
        foundUsers = Profile.objects.all().filter(user__username__icontains = request.POST.get('friendz'))
        currentFriends = user.friendsList.all()
        for profile in foundUsers:
            if profile not in currentFriends:
                if not profile == user:
                    foundFriends.append(profile)
    return render(request, 'friends.html', {'cur_user_id': curUserID, 'friends': foundFriends, 'friendz':request.POST.get('friendz'), 'username' : request.POST.get('username'),'found': friend_list })

def makeFriend(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    newFriend = Profile.objects.all().filter(user__username = request.GET.get('username'))
    user.friendsList.add(newFriend[0].id)
    user.save()
    return redirect('getFriends')

def setPreferences(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    user.favorite_location = request.POST.get('favorite_location')
    user.in_person = request.POST.get('in_person')
    user.cramming = request.POST.get('cramming')
    user.preferencesSet=True
    user.save()
    return redirect('setBio')

def getPreferencesPage(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    if not(user.classesSet):
        return redirect('setClasses')
    return render(request, 'detailed_onboarding.html')

def setBio(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    user.year = request.POST.get('year')
    user.school = request.POST.get('school')
    user.major = request.POST.get('major')
    user.about_you = request.POST.get('about_you')
    user.bioSet = True
    user.save()
    return redirect('namingChanges')

def getBioPage(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    if not(user.classesSet):
        return redirect('setClasses')
    return render(request, 'bio_onboarding.html')

def getProfile(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    if not(user.classesSet):
        return redirect("setClasses")
    if not(user.preferencesSet):
        return redirect("setPreferences")
    if not(user.bioSet):
        return redirect("setBio")
    else:
        ownedProfile = False
        curUserID = request.user.Profile.id
        requestedProfile = Profile.objects.get(id=pk)
        requestedUser = requestedProfile.user
        if requestedProfile == request.user.Profile:
            ownedProfile = True
        enrolled_classes = list(requestedProfile.classes.all())
        friend_list = list(requestedProfile.friendsList.all())
        major = requestedProfile.major
        bio = requestedProfile.about_you
        year = requestedProfile.year
        school = requestedProfile.school
        user.editProfile = True
        user.save()
    return render(request, 'profiles.html', {'cur_user_id': curUserID,  'num_classes': len(enrolled_classes), 'favorite_location': requestedProfile.favorite_location,  'num_friends': len(friend_list),  'major': major,  'year': year, 'school': school, 'bio': bio, 'in_person': requestedProfile.in_person, 'cramming': requestedProfile.cramming, 'found_user': requestedUser, 'owned_profile': ownedProfile})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    if not(user.classesSet):
        return redirect("setClasses")
    if not(user.preferencesSet):
        return redirect("setPreferences")
    if not(user.bioSet):
        return redirect("setBio")
    if not (user.nameSet):
        return redirect("namingChanges")
    else:
        curUser = request.user.Profile
        curUserID = curUser.id
        enrolled_classes = list(curUser.classes.all())
        inactive_classes = list(curUser.inactiveClasses.all())
        friend_list = list(curUser.friendsList.all())
        mySessions = StudySession.objects.filter(attendees__in=[curUser.id])
        return render(request, 'dashboard.html', {'cur_user_id': curUserID,'enrolledclasses': enrolled_classes, 'inactiveclasses': inactive_classes,'in_person': curUser.in_person, 'cramming': curUser.cramming, 'favorite_location': curUser.favorite_location, 'found': friend_list, 'enrolledSessions': mySessions})

def viewClasses(request):
    if not request.user.is_authenticated:
        return redirect('index')
    curUserID = request.user.Profile.id
    userCurrentClasses = list(request.user.Profile.classes.all().values_list('id', flat=True)) + list(request.user.Profile.inactiveClasses.all().values_list('id', flat=True))
    foundClasses = Class.objects.all()
    params = { "hitsPerPage": 10 }
    search_param = request.POST.get('class_search')
    response = raw_search(Class, search_param, params) 
    #get object ids from algolia raw search response
    object_ids = [hit['objectID'] for hit in response['hits']]
    return render(request, 'classes_view.html', {'current_classes': userCurrentClasses,'cur_user_id': curUserID,'classes': foundClasses, 'response': response, 'objectIDs': object_ids})

def viewClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    curUserID = request.user.Profile.id
    curClass = Class.objects.all().filter(id = pk)[0]
    return render(request, 'class_view.html', {'cur_user_id': curUserID, 'classID': curClass.id,'className': curClass.class_name, 'classInstructor': curClass.instructor, 'classDescription': curClass.description, "classDays": curClass.days, "classStartTime": curClass.start_time, 'classEndTime': curClass.end_time, 'classLocation': curClass.location, 'classType': curClass.component})

def inactivateClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    foundClass = Class.objects.get(id=pk)
    user.classes.remove(foundClass)
    user.inactiveClasses.add(foundClass)
    user.save()
    return redirect('dashboard')

def activateClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user.Profile
    foundClass = Class.objects.get(id=pk)
    user.classes.add(foundClass)
    user.inactiveClasses.remove(foundClass)
    user.save()
    return redirect('dashboard')

def viewStudySessions(request):
    if not request.user.is_authenticated:
        return redirect('index')
    curUserID = request.user.Profile.id
    foundSessions = StudySession.objects.all()
    classIDList = []
    for foundClass in request.user.Profile.classes.all():
        classIDList.append(foundClass.id)
    foundRelevantSessions = StudySession.objects.filter(associatedClass__in=classIDList)
    return render(request, 'groups_view.html', {'cur_user_id': curUserID,'sessions': foundSessions, 'relevantSessions': foundRelevantSessions})

def setDiscussionPage(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        user = request.user.Profile
        user.message = request.GET.get('message')
        user.date = request.GET.get('date')
        return render(request, 'group_view.html')
    if request.method == 'POST':
        curSes = StudySession.objects.all().filter(id=pk)[0]
        user = request.user.Profile
        currentDate = str(datetime.datetime.now())
        print(currentDate)
        newBoard = Message(message= curSes, sender=user, date=request.POST.get('date'))
        newBoard.save()
        disKey = newBoard.id
        user.save()
        return redirect('viewStudySession', pk)


def deleteMessage(request, pk):
    targetMessage = Message.objects.all().filter(id=pk)[0]
    studyGroup = targetMessage.group
    if request.user.Profile == targetMessage.sender:
        targetMessage.delete()
    return redirect("viewStudySession", studyGroup.id)

def viewStudySession(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        curUserID = request.user.Profile.id
        curSession = StudySession.objects.all().filter(id = pk)[0]
        messages = Message.objects.filter(group=curSession)
        for message in messages:
            message.date = dtc.strptime(message.date, '%Y-%m-%d %H:%M:%S.%f')
            #convert utc to est
            message.date = message.date - datetime.timedelta(hours=5)
        inSession = request.user.Profile in curSession.attendees.all()
        return render(request, 'group_view.html', {'cur_user_id': curUserID, 'foundSession':curSession, 'discussionBoard': messages, 'inSession':inSession})
    if request.method == 'POST':
        user = request.user.Profile
        currentDate = str(datetime.datetime.now())
        print(currentDate)
        newMessage = Message(message=request.POST.get('message'), sender=user, date=currentDate, group=StudySession.objects.filter(id=pk)[0])
        newMessage.save()
        return redirect('viewStudySession', pk)

def createStudySession(request,pk):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        context = {}
        context['form'] = StudySessionForm()
        context['cur_user_id'] = request.user.id
        return render(request, "create_study_session.html", context)
    if request.method == 'POST':
        curClass = Class.objects.all().filter(id = pk)[0]
        curUser = request.user.Profile
        newStudySession = StudySession(associatedClass = curClass, organizer=curUser, location=request.POST.get('location'), startTime=request.POST.get('startTime'), endTime = request.POST.get('endTime'), description = request.POST.get('description'), title = request.POST.get('title'))
        newStudySession.save()
        newStudySession.attendees.add(curUser)
        newStudySession.save()
        sessionKey = newStudySession.id
        return redirect('viewStudySession', sessionKey)


def editStudySession(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    foundSession = StudySession.objects.all().filter(id=pk)[0]
    if not (foundSession.organizer.id == request.user.Profile.id):
        return redirect('viewStudySession', pk)
    if request.method == 'GET':
        context = {}
        newStartTime = foundSession.startTime.strftime("%Y-%m-%dT%H:%M")
        newEndTime = foundSession.endTime.strftime("%Y-%m-%dT%H:%M")
        sessionData = {'title': foundSession.title, 'location': foundSession.location,
                       'startTime': newStartTime, 'endTime': newEndTime, 'description': foundSession.description}
        context['form'] = StudySessionForm(initial=sessionData)
        context['cur_user_id'] = request.user.id
        return render(request, "edit_study_session.html", context)
    if request.method == 'POST':
        foundSession.location = request.POST.get('location')
        foundSession.startTime = request.POST.get('startTime')
        foundSession.endTime = request.POST.get('endTime')
        foundSession.description = request.POST.get('description')
        foundSession.title = request.POST.get('title')
        foundSession.save()
        return redirect('viewStudySession', pk)

def joinStudySession(request,pk):
    if not request.user.is_authenticated:
        return redirect('index')
    curSession = StudySession.objects.all().filter(id = pk)[0]
    curUser = request.user.Profile
    curSession.attendees.add(curUser)
    curSession.save()
    return redirect('viewStudySession', pk)

def leaveStudySession(request,pk):
    if not request.user.is_authenticated:
        return redirect('index')
    curSession = StudySession.objects.all().filter(id = pk)[0]
    curUser = request.user.Profile
    curSession.attendees.remove(curUser)
    curSession.save()
    return redirect('viewStudySession', pk)

def joinExistingClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    curUser = request.user.Profile
    inactiveClasses = list(
        request.user.Profile.inactiveClasses.all().values_list('id', flat=True))
    if pk not in inactiveClasses:
        foundClass = Class.objects.all().filter(id=pk)[0]
        curUser.classes.add(foundClass)
    return redirect('viewClasses')

def leaveExistingClass(request, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    curUser = request.user.Profile
    inactiveClasses = list(request.user.Profile.inactiveClasses.all().values_list('id', flat=True))
    activeClasses = list(request.user.Profile.classes.all().values_list('id', flat=True))
    if pk in inactiveClasses:
        foundClass = Class.objects.all().filter(id = pk)[0]
        curUser.inactiveClasses.remove(foundClass)
    if pk in activeClasses:
        foundClass = Class.objects.all().filter(id = pk)[0]
        curUser.classes.remove(foundClass)
    return redirect('viewClasses')


def confirmLogout(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "confirm_logout.html")
