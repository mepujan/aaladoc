from django.urls import path, include
from rest_framework.routers import DefaultRouter

from plasmadonation.views import PlasmaDonorAPIView
from .api_views import (
    AddPaymentMethod,
    CategoriesView,
    GetArticleView,
    QuestionView,
    QuestionCommentView,
    CityView,
    LocalityView,
    ClinicInfoView,
    DoctorCityView,
    DoctorDegreeView,
    DoctorInstitutionView,
    DoctorSpecializationView,
    DoctorRegistrationCouncilView,
    DoctorInfoView,
    ServiceView,
    PatientInformationView,
    UserRegistrationViewSet,
    ValidateUserViewSet,
    UserLoginViewset,
    BloodDonorInformationAPIView,
    ChangePasswordView,
    ValidateEmailViewSet,
    ValidateCodeViewSet,
    LogoutApiView,
    CarouselAPIView,
    DoctorRegistrationViewSet,
    NMCNumberChecker,
    DistrictsAPIView,
    GeneralSettingAPIView,
    DoctorPrescriptionAPI,
    LastLoginAPIView,
    PaymentAPIView,
    FrontViewCarouselAPIView,
    FrontViewServiceView,
    FrontViewQuestionView,
    FrontViewArticleView,
    FrontViewCategoriesView,
    # FrontViewDoctorAppointmentView,
    FrontMultipleAPIView,
    # DoctorFilterListView,
    ArticleFilterView,
    QuestionFilterView,
    PropertiesView,
    QuestionCommentFilterView,
    ArticleCommentFilterView,
    NotificationAPIView,
    PostArticle,
    PostArticleComment,
    PostRatingView,
    CallAPIView,
    GetQuestionView,
    PostQuestionComment,
    PostQuestion,
    UserUpdateViewSet,
    SinglePatientPrescriptionList,
    DoctorPrescriptionHistory,
    ResetPasswordAPIView,
    ValidateResetPasswordAPIView,
    DoctorProfileAPIView,
    DoctorProfileUpdate,
    AppointmentCountAPIView,
    CallEndedAPI,
    UpdateFCMTokenAPIView,
    ContactInfoAPIView,
    PrivacyPolicyAPIView,
    LikeArticleAPIView,
    MyAppointmentsAPIView,
    ScheduleView,
    DoctorInfosView
)

router = DefaultRouter()
router.register(r"doctorInfos", DoctorInfosView, basename="doctorInfos")
router.register(r"schedule", ScheduleView, basename="schedule")
# router.register(
#     r"doctor_appointment", DoctorAppointmentView, basename="Doctor_appointment"
# )
router.register(r"categories", CategoriesView, basename="categories")
# router.register(r'article', ArticleView, basename='article')
# router.register(r'articleComment', ArticleCommentsView, basename='articleComment')
router.register(r"question", QuestionView, basename="question")
router.register(r"questionComment", QuestionCommentView, basename="questionComment")
router.register(r"city", CityView, basename="city")
router.register(r"locality", LocalityView, basename="locality")
router.register(r"clinicInformation", ClinicInfoView, basename="clinicInformation")
router.register(r"doctorCities", DoctorCityView, basename="doctorCities")
router.register(r"doctorDegree", DoctorDegreeView, basename="doctorDegree")
router.register(
    r"doctorInstitution", DoctorInstitutionView, basename="doctorInstitution"
)
router.register(
    r"doctor_specialization", DoctorSpecializationView, basename="doctor_specialization"
)
router.register(
    r"doctorRegistrationCouncil",
    DoctorRegistrationCouncilView,
    basename="doctorRegistrationCouncil",
)
# router.register(r'doctorInfo', DoctorInfoView, basename='doctorInfo')
router.register(r"services", ServiceView, basename="services")
router.register(
    r"patientInformation", PatientInformationView, basename="patientInformation"
)
# router.register(r'bloodDonor', PlasmaDonorAPIView, basename="bloodDonor")
router.register(r"carousel", CarouselAPIView, basename="carousel")
# router.register(r'notification',NotificationAPIView, basename = "notification")
# router.register(r'notificationType',NotificationTypeAPIView,basename="notificationType")
router.register(r"generalSettings", GeneralSettingAPIView, basename="generalSettings")
router.register(r"lastLogin", LastLoginAPIView, basename="lastLogin")
router.register(r"payment", PaymentAPIView, basename="payment")
router.register(r"addpayment", AddPaymentMethod, basename="addpayment")


# FontPage API Url

router.register(r"front_carousel", FrontViewCarouselAPIView, basename="front_carousel")
router.register(r"front_service", FrontViewServiceView, basename="front_service")
router.register(r"front_question", FrontViewQuestionView, basename="front_question")
router.register(r"front_article", FrontViewArticleView, basename="front_article")
router.register(
    r"front_categories", FrontViewCategoriesView, basename="front_tcategories"
)
# router.register(
#     r"front_doctorInfo", FrontViewDoctorAppointmentView, basename="front_doctorInfo"
# )
router.register(r"properties", PropertiesView, basename="properties")

# for question and articles
router.register(r"question_comment", QuestionCommentView, basename="question_comment")
# router.register(r'article_comment', ArticleCommentView, basename='article_comment')

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", UserRegistrationViewSet.as_view(), name="signup"),
    path("validate_email/", ValidateEmailViewSet.as_view(), name="validate_email"),
    path("validate_code/", ValidateCodeViewSet.as_view(), name="validate_code"),
    path("validate_user/<int:id>", ValidateUserViewSet.as_view(), name="validate_user"),
    path("login/", UserLoginViewset.as_view(), name="login"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("password_reset/", ResetPasswordAPIView.as_view(), name="password_reset"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("doctorSignup/", DoctorRegistrationViewSet.as_view(), name="doctorSignup"),
    path("nmcChecker/", NMCNumberChecker.as_view(), name="nmcChecker"),
    path("districts/", DistrictsAPIView.as_view(), name="districts"),
    path("front_all_api", FrontMultipleAPIView.as_view(), name="front_all_api"),
    # path("filter_doctor", DoctorFilterListView.as_view(), name="filter_doctor"),
    path("filter_article", ArticleFilterView.as_view(), name="filter_article"),
    path("filter_question", QuestionFilterView.as_view(), name="filter_question"),
    path(
        "filter_question_comment",
        QuestionCommentFilterView.as_view(),
        name="filter_question_comment",
    ),
    path(
        "filter_article_comment",
        ArticleCommentFilterView.as_view(),
        name="filter_article_comment",
    ),
    # path('articleComment/', ArticleCommentView.as_view(), name="article_comment"),
    path("notification/", NotificationAPIView.as_view(), name="notification"),
    path("articleView/", GetArticleView.as_view(), name="articleview"),
    path("articleView/<int:id>/", GetArticleView.as_view(), name="articleviewWithId"),
    path("postArticle/", PostArticle.as_view(), name="postArticle"),
    path(
        "postArticleComment/", PostArticleComment.as_view(), name="postArticleComment"
    ),
    path("questionView/", GetQuestionView.as_view(), name="questionView"),
    path("questionView/<int:id>", GetQuestionView.as_view(), name="questionViewWithId"),
    path("postQuestion/", PostQuestion.as_view(), name="postQuestion"),
    path(
        "postQuestionComment/",
        PostQuestionComment.as_view(),
        name="postQuestionComment",
    ),
    # path("doctorRating/<int:id>/", RatingView.as_view(), name='doctorRating'),
    path("doctorRating/", PostRatingView.as_view(), name="doctorRatingPost"),
    path("callDetails/", CallAPIView.as_view(), name="callDetails"),
    path(
        "doctorInfo/",
        DoctorInfoView.as_view(),
        name="doctorInfos",
    ),
    path("doctorInfo/<int:id>/", DoctorInfoView.as_view(), name="doctorInfo"),
    path("bloodDonor/", BloodDonorInformationAPIView.as_view(), name="bloodDonor"),
    path("updateProfile/<int:pk>/", UserUpdateViewSet.as_view(), name="updateProfile"),
    path(
        "doctorPrescription/",
        DoctorPrescriptionAPI.as_view(),
        name="doctorPrescription",
    ),
    path(
        "doctorPrescription/<int:pk>/",
        SinglePatientPrescriptionList.as_view(),
        name="doctorPrescriptions",
    ),
    path(
        "doctorPrescriptionHistory/<int:pk>/",
        DoctorPrescriptionHistory.as_view(),
        name="doctorPrescriptionHistory",
    ),
    path(
        "get-password-reset-code/",
        ValidateResetPasswordAPIView.as_view(),
        name="get-password-reset-code",
    ),
    path("doctor-profile", DoctorProfileAPIView.as_view(), name="doctor-profile"),
    path(
        "doctor-profile/<int:pk>/", DoctorProfileUpdate.as_view(), name="doctor-profile"
    ),
    path(
        "appointmentCount/", AppointmentCountAPIView.as_view(), name="appointmentCount"
    ),
    path("call_end/",CallEndedAPI.as_view(), name='call_end'),
    path("update_fcm_token/",UpdateFCMTokenAPIView.as_view(), name='update_fcm_token'),
    path("contact_info/",ContactInfoAPIView.as_view(),name = "contact_info"),
    path("privacy_policy/",PrivacyPolicyAPIView.as_view(),name="privacy_policy"),
    path("like_article/",LikeArticleAPIView.as_view(),name= "like_article"),
    path("my_appointments/",MyAppointmentsAPIView.as_view(),name="my_appointments")
]
