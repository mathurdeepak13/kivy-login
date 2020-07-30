import os
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.utils import platform
# from database import DataBase


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                # db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    data_dir = App().user_data_dir
    store = JsonStore(os.path.join(data_dir, 'storage.json'))

    def loginBtn(self):
        cam = sm.get_screen("main").ids['camera']
        print("app camera: {}".format(cam))
        cam.play = True
        cam.resolution = Window.size
        # validate user here
        MainWindow.current = self.email.text
        self.reset()
        sm.current = "main"
        # else:
        #     invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def get_user(self):
        try:
            user = LoginWindow.store.get('credentials')['username']
        except KeyError:
            user = ""

        return user

    def get_pass(self):
        try:
            passwd = LoginWindow.store.get('credentials')['password']
        except KeyError:
            passwd = ""

        return passwd

    def reset(self):
        self.save_login()
        self.email.text = ""
        self.password.text = ""

    def save_login(self):
        email = self.email.text
        passwd = self.password.text
        LoginWindow.store.put('credentials', username=email, password=passwd)


class CameraClick(Screen):
    # print("Camera click init........{}".format(ids['camera']))
    # camera = ObjectProperty(None)
    # camera.play = True
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request_android_permissions()

    @staticmethod
    def is_android():
        return platform == 'android'

    def _request_android_permissions(self):
        """
        Requests CAMERA permission on Android.
        """
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    # def on_enter(self, *args):
    #     password, name, created = db.get_user(self.current)
    #     self.n.text = "Account Name: " + name
    #     self.email.text = "Email: " + self.current
    #     self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), CameraClick(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


MyMainApp().run()
