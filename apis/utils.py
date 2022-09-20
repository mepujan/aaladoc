import os

import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate(os.getcwd() + "/notify.json")
firebase_admin.initialize_app(cred)


def send_push(title, msg, registration_token, data_object):
    message = messaging.MulticastMessage(
        tokens=registration_token,
        # apns=messaging.APNSConfig(
        #     headers={
        #         "apns_priority": '10'
        #     },
        #     payload=messaging.APNSPayload(
        #         aps=messaging.Aps(
        #             alert=messaging.ApsAlert(
        #                 title=title,
        #                 body=msg,
        #             ),
        #             mutable_content=True,
        #             content_available=True
        #         ),
        #         data=data_object,
        #         token=registration_token
        #     ),
        # ),
        android=messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                title=title,
                body=msg,
                priority="high",
                click_action="FLUTTER_NOTIFICATION_CLICK",
                default_sound=True,
                color="#AFEEEE",
                default_light_settings=True,
                ticker="AALADOC",
                # image="http://www.aaladoc.com/"+data_object['sender_image'],
                # icon= "favicon.ico"
                vibrate_timings_millis=[30, 50000, 400, 10000, 400, 100, 400],
                # sound=os.getcwd() + '/sound.mp3',
                # sticky=True
            ),
            data=data_object,
        ),
    )
    messaging.send_multicast(message)
