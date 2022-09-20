import urllib.request
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from bs4 import BeautifulSoup
from django.contrib import auth
from django.contrib.auth import get_user_model, logout
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, authentication, serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.authtoken.models import Token
from Appointment.models import DoctorAppointment
from rest_framework import filters

from Appointment.serializers import DoctorAppointmentSerializers,ScheduleSerializers
from Appointment.models import Schedule
from Clinic.models import City as Cty, Locality, ClinicInfo
from Clinic.serializers import CitySerializers, LocalitySerializers, ClinicSerializers
from Doctor.models import (
    City,
    Degree,
    Institution,
    BasicInfo,
    Specialization,
    RegistrationCouncil,
    DoctorRating,
)
from Doctor.serializers import (
    CitiesSerializers,
    DegreeSerializers,
    InstitutionSerializers,
    SpecializationSerializers,
    RegistrationCouncilSerializers,
    DoctorInfoSerializers,
    DoctorMedicalNumberChecker,
    DoctorRatingSerializers,
    DoctorProfileSerializers,
    DoctorProfileUpdate,
    CallEndingSerializer,


)
from Forum.models import Question, QuestionComments, Article, ArticleComments, Category,ArticleLiked
from Forum.serializers import (
    QuestionSerializers,
    QuestionCommentSerializers,
    CategoriesSerializers,
    ArticleSerializers,
    ArticleCommentSerializers,
    ArticleLikedSerializer
)
from Services.models import Service
from Services.serializers import ServiceSerializers
from SiteContents.models import (
    PaymentMethod,
    CallDetail,
    Properties,
    Carousel,
    GeneralSetting,
    Payment,
    ContactInformation,
    Privacy_Policy,
    AboutUs
)
from SiteContents.serializers import (
    PropertiesSerializers,
    CarouselSerializers,
    NotificationSerializer,
    GeneralSettingSerializer,
    PaymentSerializer,
    CallDetailSerializer,
    ContactInfoSerializers,
    PrivcyPolicySerializer,
    AboutUsSerializer,
    AddPaymentMethodSerializers,

)
from accounts.models import UserFCMToken
from accounts.serializers import (
    UserRegistrationSerializers,
    UserLoginSerializers,
    ChangePasswordSerializer,
    DoctorRegistrationSerializers,
    LastLoginSerializers,
    UserValidationSerializers,
    ValidateUser,
    CodeValidationSerializers,
    BloodDonorInfoSerializers,
    UserUpdateSerialiazers,
    ResetPasswordSerializers,
    DoctorInfosSerializers
)
from patient.models import Information, Prescription
from patient.serializers import (
    PatientInformationSerializers,
    DoctorPrescriptionSerializer,
    DoctorPrescriptionListSerializers,
)

User = get_user_model()


# Appointment API
class ScheduleView(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializers


# class DoctorAppointmentView(ModelViewSet):
#     queryset = DoctorAppointment.objects.all()
#     serializer_class = DoctorAppointmentSerializers


# Forum API
class CategoriesView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers


class GetArticleView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permissions_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, id=None):
        if id is not None:
            queryset_article = get_object_or_404(Article, id=id)
            serializer_article = ArticleSerializers(queryset_article, context={"request": request})
            articles = {}
            queryset_article.views += 1
            queryset_article.save()
            articles.update(serializer_article.data)
            is_liked = ArticleLiked.objects.filter(user=request.user,is_liked=True,article__id=queryset_article.id)
            if is_liked:
                articles['is_liked'] = True
            else:
                articles['is_liked'] = False
            queryset_comment = ArticleComments.objects.filter(
                comment_feed_id__exact=queryset_article.id
            )
            serializer_comments = ArticleCommentSerializers(queryset_comment, many=True,context = {"request":request})
            total_comments = len(queryset_comment)
           
            return Response(
                {
                    "article": articles,
                    "comments": serializer_comments.data,
                    "total_comment": total_comments,
                }
            )
        else:
            queryset = Article.objects.all()
            serializer = ArticleSerializers(queryset, many=True, context={"request": request})
            return Response(serializer.data)


class PostArticle(generics.CreateAPIView):
    serializer_class = ArticleSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostArticleComment(generics.CreateAPIView):
    serializer_class = ArticleCommentSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetQuestionView(APIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers

    def get(self, request, id=None):
        if id is not None:
            queryset_question = get_object_or_404(Question, id=id)
            queryset_question.views += 1
            queryset_question.save()
            serializer_question = QuestionSerializers(queryset_question)
            queryset_comment = QuestionComments.objects.filter(
                comment_feed_id__exact=queryset_question.id
            )
            serializer_comments = QuestionCommentSerializers(
                queryset_comment, many=True
            )
            total_comments = len(queryset_comment)
            return Response(
                {
                    "questions": serializer_question.data,
                    "comments": serializer_comments.data,
                    "total_comment": total_comments,
                }
            )
        else:
            queryset = Question.objects.all()
            serializer = QuestionSerializers(queryset, many=True)
            return Response(serializer.data)


class PostQuestion(generics.CreateAPIView):
    serializer_class = QuestionSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostQuestionComment(generics.CreateAPIView):
    serializer_class = QuestionCommentSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionView(ModelViewSet):
    queryset = Question.objects.filter(verify=True).all().order_by("-updated")
    serializer_class = QuestionSerializers


class QuestionCommentView(ModelViewSet):
    queryset = QuestionComments.objects.all().order_by("-updated")
    serializer_class = QuestionCommentSerializers
    filterset_fields = ["question"]


# Clinic API


class CityView(ModelViewSet):
    queryset = Cty.objects.all()
    serializer_class = CitySerializers


class LocalityView(ModelViewSet):
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializers


class ClinicInfoView(ModelViewSet):
    queryset = ClinicInfo.objects.all()
    serializer_class = ClinicSerializers


# Doctor API


class DoctorCityView(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitiesSerializers


class DoctorDegreeView(ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializers


class DoctorInstitutionView(ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializers


class DoctorSpecializationView(ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializers


class DoctorRegistrationCouncilView(ModelViewSet):
    queryset = RegistrationCouncil.objects.all()
    serializer_class = RegistrationCouncilSerializers

class DoctorInfosView(ModelViewSet):
    queryset = BasicInfo.objects.all()
    serializer_class = DoctorInfosSerializers

class DoctorInfoView(APIView):
    queryset = BasicInfo.objects.all()
    serializer_class = DoctorInfoSerializers
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = DoctorInfosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            doctor = BasicInfo.objects.filter(id=id).exists()
            if doctor:
                queryset = BasicInfo.objects.get(id=id)
                serializer = DoctorInfoSerializers(queryset,context = {"request":request})

                user_rating_query = DoctorRating.objects.filter(
                    doctor=request.user.id
                ).order_by("-updated")
                if len(user_rating_query) > 0:
                    user_rating = user_rating_query[0].rating
                else:
                    user_rating = 0
                data = {}
                data.update(serializer.data)
                data["user_rating"] = user_rating
                if Payment.objects.filter(user=self.request.user.id, doctor=id).exists():
                    data['payment_status'] = True
                else:
                    data['payment_status'] = False
                if len(serializer.data.get("call_to_doctor")) > 0:
                    for datas in serializer.data.get("call_to_doctor"):
                        if datas.get("user") == self.request.user.id:
                            print("data=", datas.get("call_to_doctor"))
                            data['call_to_doctor'] = datas.get("call_to_doctor")
                        else:
                            data['call_to_doctor'] = datas.get("call_to_doctor")
                else:
                    data['call_to_doctor'] = False
                return Response(data)
            else:
                return Response({"message": "No doctor Found"})
        else:
            if "specialization" in request.query_params:
                queryset = BasicInfo.objects.filter(
                    specialization__name__icontains=request.query_params[
                        "specialization"
                    ]
                )
                serializers = DoctorInfoSerializers(queryset, many=True,context = {"request":request})
                for data in serializers.data:
                    if len(data.get("call_to_doctor")) > 0:
                        for datas in data.get("call_to_doctor"):
                            if datas.get("user") == self.request.user.id:
                                data['call_to_doctor'] = datas.get("call_to_doctor")

                            if datas.get("call_successful") is False:
                                data['payment_status'] = True

                            else:
                                data['call_to_doctor'] = False
                                data['payment_status'] = False
                    else:
                        data['call_to_doctor'] = False
                        data['payment_status'] = False
                return Response(serializers.data)
            else:
                queryset = BasicInfo.objects.all()
                serializers = DoctorInfoSerializers(queryset, many=True,context = {"request":request})
                for data in serializers.data:
                    if len(data.get("call_to_doctor")) > 0:
                        for datas in data.get("call_to_doctor"):
                            if datas.get("user") == self.request.user.id:
                                data['call_to_doctor'] = datas.get("call_to_doctor")

                            if datas.get("call_successful") is False:
                                data['payment_status'] = True
                            else:
                                data['call_to_doctor'] = False
                                data['payment_status'] = False
                    else:
                        data['call_to_doctor'] = False
                        data['payment_status'] = False
                return Response(serializers.data)
    

class NMCNumberChecker(APIView):
    serializer_class = DoctorMedicalNumberChecker

    def post(self, request):
        name = request.data.get("full_name")
        nmc_no = request.data.get("medical_number")
        names = name.replace(" ", "+")
        url = (
                "https://www.nmc.org.np/searchPractitioner?name="
                + names
                + "&nmc_no="
                + nmc_no
        )
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        # result = soup.find_all("table", attrs={'class': 'table-result'})
        result = soup.find("th")
        if result.text.upper() == "PRACTITIONER NOT FOUND":
            return Response(
                {"is_authenticated_doctor": False}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                {"is_authenticated_doctor": True}, status=status.HTTP_200_OK
            )


# Service API


class ServiceView(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers


# patient Information API
class PatientInformationView(ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = PatientInformationSerializers


# User Account API
class ValidateResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = UserValidationSerializers

    def post(self, request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                ValidateUser.objects.update_or_create(
                    email=serializer.data["email"],
                    defaults={"email": serializer.data["email"]},
                )
                code = ValidateUser.objects.get(email=serializer.data["email"]).code
                html_file = get_template("reset_password_mail.html")
                html_content = html_file.render({"verification_code": code})
                subject = "Password Reset Verification Code"
                message = "Email Body"
                from_email = "info.aaladoc@gmail.com"
                recipient_list = [serializer.data["email"]]
                email = EmailMultiAlternatives(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return Response(
                    {"success": "Success! Check your email for the reset code."}
                )

        else:
            return Response({"error": "No Account Associated with this email"})


class ValidateEmailViewSet(generics.CreateAPIView):
    serializer_class = UserValidationSerializers

    def post(self, request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "This email is already used"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                ValidateUser.objects.update_or_create(
                    email=serializer.data["email"],
                    defaults={"email": serializer.data["email"]},
                )
                code = ValidateUser.objects.get(email=serializer.data["email"]).code
                html_file = get_template("verification_code.html")
                html_content = html_file.render({"verification_code": code})
                subject = "Email Verification Code"
                message = "Email Body"
                from_email = "info.aaladoc@gmail.com"
                recipient_list = [serializer.data["email"]]
                email = EmailMultiAlternatives(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return Response({"success": "Success! Check your email for the code."})


class ValidateCodeViewSet(generics.CreateAPIView):
    serializer_class = CodeValidationSerializers

    # queryset =ValidateUser.objects.all()
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        if ValidateUser.objects.filter(email=email, code=code).exists():
            return Response({"success": "Success! ."})
        else:
            return Response(
                {"error": "Code is incorrect."}, status=status.HTTP_400_BAD_REQUEST
            )


# Reset Password
class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializers

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data["email"])
            user.set_password(serializer.data["password"])
            user.save()
            return Response(
                {"success": "Password Reset Successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        else:
            return Response({"error": "Error in Reseting Password. Try Again"})


class ValidateUserViewSet(APIView):
    serializer_class = UserValidationSerializers
    queryset = User.objects.all()

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = UserValidationSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializers


class DoctorRegistrationViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = DoctorRegistrationSerializers


class UserLoginViewset(APIView):
    serializer_class = UserLoginSerializers

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        fcm_token = request.data.get("fcm_token")
        stat = request.data["status"].lower()
        usr = User.objects.filter(email=email).exists()
        if usr:
            if Token.objects.filter(user=usr).exists():
                username = User.objects.get(email=email).username

                # User.objects.get(email = email).username
                user = auth.authenticate(username=username, password=password)

                if user:
                    UserFCMToken.objects.update_or_create(
                        user=user, defaults={"user": user, "fcm_token": fcm_token}
                    )

                    id = User.objects.get(email=email).id
                    username = User.objects.get(email=email).username
                    first_name = User.objects.get(email=email).first_name
                    last_name = User.objects.get(email=email).last_name
                    is_staff = User.objects.get(email=email).is_staff
                    is_superuser = User.objects.get(email=email).is_superuser
                    last_login = User.objects.get(email=email).last_login
                    phone = User.objects.get(email=email).phone
                    profile_pic = User.objects.get(email=email).profile_pic
                    gender = User.objects.get(email=email).gender
                    height = User.objects.get(email=email).height
                    weight = User.objects.get(email=email).weight
                    uuid = User.objects.get(email=email).uuid
                    is_available = User.objects.get(email=email).is_available
                    blood_group = User.objects.get(email=email).blood_group
                    address = User.objects.get(email=email).address
                    dob = User.objects.get(email=email).dob
                    district = User.objects.get(email=email).district

                    if profile_pic != "":
                        profile_pic = f"http://aaladoc.com{profile_pic.url}"
                    else:
                        profile_pic = f"{profile_pic}"

                    if is_superuser:
                        return Response(
                            {
                                "username": username,
                                "id": id,
                                "email": email,
                                "first_name": first_name,
                                "last_name": last_name,
                                "last_login": last_login,
                                "Phone": phone,
                                "profile_pic": f"{profile_pic}",
                                "gender": gender,
                                "height": height,
                                "weight": weight,
                                "user_id": uuid,
                                "token": user.auth_token.key,
                            }
                        )
                    if is_staff and stat == "doctor":
                        doctor_specialization = BasicInfo.objects.get(
                            user=id
                        ).specialization

                        doctor = BasicInfo.objects.get(user_id=id)
                        return Response(
                            {
                                "id": id,
                                "token": user.auth_token.key,
                                "doctor_id": doctor.id,
                                "username": username,
                                "email": email,
                                "first_name": first_name,
                                "last_name": last_name,
                                "is_staff": is_staff,
                                "last_login": last_login,
                                "specialization": doctor_specialization.name,
                                "doctor_uuid": uuid,
                                "phone": phone,
                                "blood_group": blood_group,
                                "district":district,
                                "address": address,
                                "dob": dob,
                                "profile_pic": profile_pic,
                                "experience": doctor.experience,
                                "registration_no": doctor.registration_no,
                                "reg_council": doctor.reg_council.name,
                                "reg_year": doctor.reg_year,
                                "institution": doctor.institution.name,
                                "degree": doctor.degree.name,
                                "short_bio": doctor.short_bio,
                            }
                        )

                    if stat == "patient":
                        return Response(
                            {
                                "token": user.auth_token.key,
                                "username": username,
                                "id": id,
                                "email": email,
                                "first_name": first_name,
                                "last_name": last_name,
                                "last_login": last_login,
                                "phone": phone,
                                "blood_group": blood_group,
                                "district":district,
                                "address": address,
                                "dob": dob,
                                "profile_pic": profile_pic,
                                "gender": gender,
                                "height": height,
                                "weight": weight,
                                "user_id": uuid,
                                "is_available": is_available,
                                "is_staff": is_staff,
                            }
                        )
                    else:
                        return Response({"error": "wrong Credientials"},status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"error": "Wrong Credientials"},
                                   status = status.HTTP_401_UNAUTHORIZED
                                    )

            else:
                return Response({"error": "No Auth Token associated with user"},status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(
                {"error": "Wrong Credientials"},status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    """LoggedOut API View"""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def post(request):
        user = request.user
        fcm_token = "aaladocdummyfcmtoken"
        UserFCMToken.objects.update_or_create(
            user=user, defaults={"user": user, "fcm_token": fcm_token}
        )
        """Log out the login user"""
        logout(request)
        return Response(status=status.HTTP_200_OK)


# Carousel API View


class CarouselAPIView(ModelViewSet):
    serializer_class = CarouselSerializers
    queryset = Carousel.objects.all()


class DistrictsAPIView(APIView):
    def get(self, request):
        districts = [
            "Bhojpur",
            "Dhankuta",
            "Ilam",
            "Jhapa",
            "Khotang",
            "Morang",
            "Okhaldhunga",
            "Panchthar",
            "Sankhuwasabha",
            "Solukhumbu",
            "Sunsari",
            "Taplejung",
            "Terhathum",
            "Udayapur",
            "Bara",
            "Parsa",
            "Dhanusha",
            "Mahottari",
            "Rautahat",
            "Saptari",
            "Sarlahi",
            "Siraha",
            "Bhaktapur",
            "Chitwan",
            "Dhading",
            "Dolakha",
            "Kathmandu",
            "Kavrepalanchok",
            "Lalitpur",
            "Makwanpur",
            "Nuwakot",
            "Ramechhap",
            "Rasuwa",
            "Sindhuli",
            "Sindhupalchok",
            "Baglung",
            "Gorkha",
            "Kaski",
            "Lamjung",
            "Manang",
            "Mustang",
            "Myagdi",
            "Nawalpur",
            "Parbat",
            "Syangja",
            "Tanahun",
            "Arghakhanchi",
            "Banke",
            "Bardiya",
            "Dang",
            "Eastern Rukum",
            "Gulmi",
            "Kapilavastu",
            "Parasi",
            "Palpa",
            "Pyuthan",
            "Rolpa",
            "Rupandehi",
            "Dailekh",
            "Dolpa",
            "Humla",
            "Jajarkot",
            "Jumla",
            "Kalikot",
            "Mugu",
            "Salyan",
            "Surkhet",
            "Western Rukum",
            "Achham",
            "Baitadi",
            "Bajhang",
            "Bajura",
            "Dadeldhura",
            "Darchula",
            "Doti",
            "Kailali",
            "Kanchanpur",
        ]
        districts.sort()
        return Response({"districts": districts})


# General settings API


class GeneralSettingAPIView(ModelViewSet):
    queryset = GeneralSetting.objects.all()
    serializer_class = GeneralSettingSerializer


# Doctor Prescription API


class SinglePatientPrescriptionList(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = DoctorPrescriptionListSerializers
    http_method_names = [
        "get",
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = Prescription.objects.filter(user_id_id=self.kwargs["pk"])
        return queryset


class DoctorPrescriptionAPI(APIView):
    # queryset = Prescription.objects.all()
    serializer_class = DoctorPrescriptionSerializer

    def get(self, request):
        queryset = Prescription.objects.all()
        serializer = DoctorPrescriptionListSerializers(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# lastlogin Updating


class LastLoginAPIView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LastLoginSerializers


# Payment API View
class AddPaymentMethod(ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = AddPaymentMethodSerializers

class PaymentAPIView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ["user"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        user = request.user.id
        doctor = str(request.data.get('doctor'))
        # doctor = BasicInfo.objects.get(user = doctor).id
        # Payment.objects.filter(user=user, doctor=doctor, call_successful=False).update(is_verified = True)
        if Payment.objects.filter(user=user, doctor=doctor, call_successful=False).exists():
            return Response({"error": "Multiple Payment Attempt"})
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# For Front Page
class FrontViewCarouselAPIView(ModelViewSet):
    serializer_class = CarouselSerializers
    queryset = Carousel.objects.all()[:5]


class FrontViewServiceView(ModelViewSet):
    queryset = Service.objects.all()[:10]
    serializer_class = ServiceSerializers


class FrontViewQuestionView(ModelViewSet):
    queryset = Question.objects.filter(verify=True).all().order_by("-updated")[:5]
    serializer_class = QuestionSerializers


class FrontViewArticleView(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers


class FrontViewCategoriesView(ModelViewSet):
    queryset = Category.objects.all()[:10]
    serializer_class = CategoriesSerializers


# class FrontViewDoctorAppointmentView(ModelViewSet):
#     queryset = DoctorAppointment.objects.all()[:5]
#     serializer_class = DoctorAppointmentSerializers


from drf_multiple_model.views import ObjectMultipleModelAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class FrontMultipleAPIView(ObjectMultipleModelAPIView):
    querylist = [
        {
            "queryset": Carousel.objects.all()[:5],
            "serializer_class": CarouselSerializers,
        },
        {
            "queryset": Service.objects.all()[:10],
            "serializer_class": ServiceSerializers,
        },
        {"queryset": Article.objects.all(), "serializer_class": ArticleSerializers},
        {
            "queryset": Category.objects.all()[:10],
            "serializer_class": CategoriesSerializers,
        },
        {
            "queryset": BasicInfo.objects.all()[:5],
            "serializer_class": DoctorInfoSerializers,
        },
        {
            "queryset": Question.objects.filter(verify=True)
                            .all()
                            .order_by("-updated")[:5],
            "serializer_class": QuestionSerializers
        },
        {
            "queryset":  ContactInformation.objects.all()[:1],
            "serializer_class": ContactInfoSerializers,
        },
        {
            "queryset": Privacy_Policy.objects.all()[:1],
            "serializer_class": PrivcyPolicySerializer,
        },
        {
            "queryset": AboutUs.objects.all()[:1],
            "serializer_class": AboutUsSerializer,
        },

    ]


# class DoctorFilterListView(generics.ListAPIView):
#     queryset = BasicInfo.objects.all()
#     serializer_class = DoctorAppointmentSerializers

#     filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
#     filter_fields = ["id", "name", "is_online", "gender"]
#     ordering_fields = ["specialization", "gender", "is_online"]
#     search_fields = ["name", "degree"]


class DoctorFilterListView(generics.ListAPIView):
    queryset = BasicInfo.objects.all()
    serializer_class = DoctorInfoSerializers

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ["id", "name", "is_online", "gender", "specialization"]
    ordering_fields = ["specialization", "gender", "is_online"]
    search_fields = ["name", "degree"]


class ArticleFilterView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ["id", "category"]
    ordering_fields = ["id", "category"]
    search_fields = ["body", "title"]


class ArticleCommentFilterView(generics.ListAPIView):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentSerializers

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ["id", "article_id"]
    ordering_fields = ["id", "date"]
    search_fields = ["comments"]


# class QuestionCommentView(ModelViewSet):
#     queryset = QuestionComments.objects.all()
#     serializer_class = QuestionCommentSerializers


class QuestionFilterView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ["id", "verify", "isAnonymous"]
    ordering_fields = ["id", "category", "written_by", "date"]
    search_fields = ["question"]


class QuestionCommentFilterView(generics.ListAPIView):
    queryset = QuestionComments.objects.all()
    serializer_class = QuestionCommentSerializers

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ["id", "question"]
    ordering_fields = ["id", "created"]
    search_fields = ["question"]


class PropertiesView(ModelViewSet):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializers


class NotificationAPIView(APIView):
    serializer_class = NotificationSerializer

    def post(self, request):
        title = request.data.get("title")
        body = request.data.get("body")
        user = request.data.get("user")
        return Response({"Message": "Notification Sent", "status code": 200})


class CallAPIView(generics.CreateAPIView):
    serializer_class = CallDetailSerializer

    def post(self, request, *args, **kwargs):
        import apis.utils as fcm

        sender = User.objects.filter(id=request.data["sender_id"]).exists()
        receiver = User.objects.filter(id=request.data["receiver_id"]).exists()
        if receiver and sender:
            receiver_fcm = UserFCMToken.objects.filter(
                user_id__exact=request.data["receiver_id"]
            ).exists()
            if receiver_fcm:
                usr_token = UserFCMToken.objects.get(
                    user_id__exact=request.data["receiver_id"]
                ).fcm_token
                token = [usr_token]
                sender_name = User.objects.get(id=request.data["sender_id"]).username
                sender_image = User.objects.get(
                    id=request.data["sender_id"]
                ).profile_pic
                sender_email = User.objects.get(id=request.data["sender_id"]).email
                call_url = request.data["call_url"]
                title = f"{sender_name} is calling ...."
                msg = "Tap to Receive"
                data_obj = {
                    "title": sender_name + " is calling...",
                    "body": "Tap Join to Receive",
                    "sender_id": str(request.data["sender_id"]),
                    "sender_name": sender_name,
                    "sender_image": str(sender_image),
                    "sender_email": str(sender_email),
                    "call_url": str(call_url),
                    "click_action": "FLUTTER_NOTIFICATION_CLICK",
                    "sound": "default",
                    "status": "done",
                    "screen": "screenA",
                }
                fcm.send_push(title, msg, token, data_obj)
                #                 # Appointment
                # doctor_id = BasicInfo.objects.get(user=request.data["receiver_id"]).id
                # payment = Payment.objects.get(
                #     is_verified=True,
                #     call_to_doctor=False,
                #     doctor=doctor_id,
                #     user=request.data["sender_id"],
                # )
                # payment.call_to_doctor = True
                # payment.save()

                # Appointment end
                return self.create(request, *args, **kwargs)
            else:
                return Response(
                    {"message": "No FCM token associated with the receiver"}
                )
        else:
            if sender:
                return Response({"message": "No Receiver Details Available"})
            elif receiver:
                return Response({"message": "No Sender Details Available"})
            else:
                return Response({"message": "No User Available"})


class PostRatingView(generics.CreateAPIView):
    serializer_class = DoctorRatingSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BloodDonorInformationAPIView(generics.ListAPIView):
    serializer_class = BloodDonorInfoSerializers
    queryset = User.objects.exclude(blood_group= "",is_available=True)
    filter_backends = (DjangoFilterBackend, OrderingFilter, filters.SearchFilter)
    filter_fields = ["blood_group", "is_available", "search_keyword"]
    search_fields = [
        "district",
        "search_keyword"
    ]


class UserUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerialiazers


class DoctorPrescriptionHistory(generics.ListAPIView):
    lookup_field = "pk"
    serializer_class = DoctorPrescriptionListSerializers
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        queryset = Prescription.objects.filter(doctor_id_id=self.kwargs["pk"])
        return queryset


class DoctorProfileAPIView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DoctorProfileSerializers

    def get(self, request):
        queryset = BasicInfo.objects.get(user=request.user)
        serializer = self.serializer_class(queryset)
        profile_picture = "http://aaladoc.com" + serializer.data["profile_pic"]
        data = {}
        data.update(serializer.data)
        data.update(profile_pic=profile_picture)
        data["id"] = request.user.id
        return Response(data)


class DoctorProfileUpdate(generics.RetrieveUpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "pk"
    serializer_class = DoctorProfileUpdate

    def get_queryset(self):
        qs = BasicInfo.objects.filter(pk=self.kwargs["pk"])
        return qs

    def update(self, request, *args, **kwargs):
        user = BasicInfo.objects.get(pk=self.kwargs["pk"]).user
        instance = BasicInfo.objects.get(pk=self.kwargs["pk"])
        serializer = self.serializer_class(
            data=request.data, instance=instance, partial=True
        )

        profile_pic = BasicInfo.objects.get(pk=self.kwargs["pk"]).user.profile_pic
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.first_name = serializer.data["first_name"]
        user.last_name = serializer.data["last_name"]
        user.address = serializer.data["address"]
        user.phone = serializer.data["phone"]
        user.blood_group = serializer.data["blood_group"]
        user.gender = serializer.data["gender"]
        user.dob = datetime.strptime(serializer.data["dob"], "%Y-%m-%d").date()

        if "profile_pic" in request.data and request.data["profile_pic"] != "":
            user.profile_pic = request.data["profile_pic"]
        else:
            user.profile_pic = profile_pic
        user.save()
        updated_user = BasicInfo.objects.get(pk=self.kwargs["pk"])
        serializer_ = DoctorProfileSerializers(updated_user)
        profile_picture = "http://aaladoc.com" + str(serializer_.data["profile_pic"])
        data = {}
        data.update(serializer_.data)
        data["id"] = user.id
        data.update(profile_pic=profile_picture)
        return Response(data, status=status.HTTP_200_OK)


class AppointmentCountAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            doctor = BasicInfo.objects.get(user=request.user)
            appointment_pending = Payment.objects.filter(
                call_to_doctor=False, doctor=doctor, is_verified=True, call_successful=False
            ).count()
            completed_appointment = CallDetail.objects.filter(
                receiver_id=request.user.id
            ).count()
            articles = Article.objects.all()[:5]
            serialized_article = ArticleSerializers(articles, many=True)
            questions = Question.objects.all()[:5]
            serialized_questions = QuestionSerializers(questions, many=True)
            return Response(
                {
                    "pending_appointment": appointment_pending,
                    "completed_appointment": completed_appointment,
                    "total_appointment": appointment_pending + completed_appointment,
                    "Article": serialized_article.data,
                    "Questions": serialized_questions.data
                }
            )
        except BasicInfo.DoesNotExist:
            return Response({"error": "No Doctor Data Associated"})


class CallEndedAPI(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CallEndingSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        doctor = serializer.data['doctor']
        print("user=", user)
        print("doctor", doctor)
        try:
            payment_data = Payment.objects.get(user=user, doctor=doctor, is_verified=True, call_to_doctor=True,
                                               call_successful=False)
            payment_data.call_to_doctor = False
            payment_data.call_successful = True
            payment_data.save()
            payment_serializer = PaymentSerializer(payment_data)
            return Response(
                payment_serializer.data
            )
        except Payment.DoesNotExist:
            return Response(
                {'error': 'cannot end call without prior verified payment.'}
            )
        except:
            return Response(
                {"error": "Something went wrong..."},
                status = status.HTTP_401_
            )


class UpdateFCMTokenAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        fcm_token = self.request.data['fcm_token']
        try:
            get_token = UserFCMToken.objects.get(user=self.request.user)
            get_token.fcm_token = fcm_token
            get_token.save()
            return Response({'fcm_token': fcm_token})
        except UserFCMToken.DoesNotExist:
            return Response({'error': 'No Existing FCM Token to update'})


class ContactInfoAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = ContactInfoSerializers

    def get(self, request):
        queryset = ContactInformation.objects.last()
        serializer = self.serializer_class(queryset, context={"request": request})
        return Response(serializer.data)


class PrivacyPolicyAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PrivcyPolicySerializer

    def get(self, request):
        queryset = Privacy_Policy.objects.last()
        serializer = self.serializer_class(queryset, context={"request": request})
        return Response(serializer.data)


# Article Liked

class LikeArticleAPIView(generics.CreateAPIView):
    serializer_class = ArticleLikedSerializer
    queryset = ArticleLiked.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if ArticleLiked.objects.filter(user = request.user,article__id= request.data['article']).exists():
        #     return Response({"error":"Cannot Like an article multiple times."},status = status.HTTP_400_BAD_REQUEST)
        if ArticleLiked.objects.filter(user = request.user,article__id= request.data['article'],is_liked=True).exists():
            article = ArticleLiked.objects.filter(user = request.user,article__id= request.data['article'],is_liked=True)[0]
            article.is_liked = False
            article.save()
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        if ArticleLiked.objects.filter(user = request.user,article__id= request.data['article'],is_liked=False).exists():
            article = ArticleLiked.objects.filter(user = request.user,article__id= request.data['article'],is_liked=False)[0]
            article.is_liked = True
            article.save()
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        serializer.save(user=request.user,is_liked= True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyAppointmentsAPIView(APIView):

    def get(self,request):
        pass