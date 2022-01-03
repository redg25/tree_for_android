from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from postgres_util import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.camera import Camera
from kivy.utils import platform
from kivy.graphics import PushMatrix,PopMatrix,Rotate
from kivy.uix.image import AsyncImage
from kivy.core.window import Window


tree_to_search =''
#GLOBALS
tag = ''


class MainWindow(Screen):
    def __init__(self,**kwargs):
        super(MainWindow,self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text="TAG de l'arbre",size_hint_y = 0.1))
        self.input = TextInput(size_hint_y = 0.3, font_size = 60)
        self.layout.add_widget(self.input)
        self.layout.add_widget(Button(text="Get",size_hint_y = 0.6, on_release=self.screen_transition_get))
        self.layout.add_widget(Button(text="Add picture",size_hint_y = 0.6, on_release=self.screen_transition_take_pic))

        self.add_widget(self.layout)

    def screen_transition_get(self, *args):

        def get_tree_info(self,widget) -> dict:
            """Get the tree info from the db using the tag parameter.
            Returns it as a dictionary
            """
        tag = self.input.text
        tree_from_db = get_tree_from_tag(tag)[0]
        # query = f"Select * from TREES where TAG = '{tag}'"
        # tree_from_db = get_records(query)
        self.parent.screens[1].tree_to_search = tree_from_db
        self.parent.screens[1].text_input_widgets['position'].text \
            = f"Description de l'arbre en position {tree_from_db['position']}"
        self.parent.screens[1].text_input_widgets['tag'].text \
            = tree_from_db['tag']
        self.parent.screens[1].text_input_widgets['type'].text \
            = tree_from_db['tree_type']
        self.parent.screens[1].text_input_widgets['comments'].text \
            = tree_from_db['comments']
        self.manager.current = 'view_tree'

    def screen_transition_take_pic(self, *args):
        self.manager.current = 'take_pic'
        self.manager.current_screen.rotate_pic()


class SecondWindow(Screen):


    def __init__(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)
        # self.label_values = ['tag','type',]
        self.text_input_widgets = {'tag':None,'position':None,'type':None,'comments':None}
        self.tree_to_search = None
        #Boxlayout to contain the full Modalview screen
        description_boxlayout = BoxLayout(orientation='vertical')

        #description_boxlayout.add_widget(Label(text=f"Description de l'arbre en position {self.tree_to_search['position']}:",size_hint_y = 0.1))
        title = Label(text="",size_hint_y = 0.1)
        self.text_input_widgets['position']=title
        description_boxlayout.add_widget(title)

        #values to create dynamically the diffent couple fields.
        #Each tuple contains (label as a string, default value as a string from the tree object)

        #Gridlayout with all the single line field text input
        trees_parameters_layout = GridLayout(cols=1, padding = 10, spacing = 10,size_hint_y = 0.5)
        for value in self.text_input_widgets:
            if value != 'position':

                para_boxlayout = BoxLayout(orientation='horizontal',  spacing = 60, size_hint_y = 0.3)
                para_boxlayout.add_widget(Label(text=value,size_hint_x = 0.3))
                if value != 'comments':
                    input = TextInput(text='', size_hint_x = 0.56, multiline=False)
                else:
                    input = TextInput(text='', size_hint_x = 0.56, multiline=True)
                #store the widget in the text_input_widgets dictionary
                self.text_input_widgets[value]=input
                para_boxlayout.add_widget(input)
                para_boxlayout.add_widget(Label(text='',size_hint_x = 0.04))
                trees_parameters_layout.add_widget(para_boxlayout)

        #store the widget in the text_input_widgets dictionary
        # self.text_input_widgets[SecondWindow.comments]=input
        # comment_boxlayout.add_widget(input)
        # comment_boxlayout.add_widget(Label(text='',size_hint_x = 0.04))
        # trees_parameters_layout.add_widget(comment_boxlayout)
        description_boxlayout.add_widget(trees_parameters_layout)

        #Boxlayout with the action buttons buttons
        btn_boxlayout = BoxLayout(orientation='horizontal',  spacing = 60, padding = 20, size_hint_y = 0.2)
        btn_boxlayout.add_widget(Button(text="SAVE",on_release=self.save_tree))
        btn_boxlayout.add_widget(Button(text="BACK",on_release=self.screen_transition))
        description_boxlayout.add_widget(btn_boxlayout)

        lb = Label(text ='', size_hint_y = 0.2)
        description_boxlayout.add_widget(lb)
        self.add_widget(description_boxlayout)

    def screen_transition(self, *args):
        self.manager.current = 'search_tree'

    def save_tree(self, *args):
        """Update the Trees database with the values from the text inputs fields
       and close the popup"""
        new_values = {'tag':self.text_input_widgets['tag'].text,
                      'tree_type':self.text_input_widgets['type'].text,
                      'comments':self.text_input_widgets['comments'].text,
                      'pictures':'http://test.com'}
        update_tree(self.tree_to_search['tag'],new_values)
        self.screen_transition()

class TakeTreePic(Screen):
    def __init__(self,**kwargs):
        super(TakeTreePic,self).__init__(**kwargs)
        if platform != "android":
            print(Window.size)
            self.btn1 = Label(text="label",size_hint_y=0.8)
            self.btn2 = Button(text="btn2", on_press=self.print_width,size_hint_y=0.2)
            print(f'bt2 w is: {self.btn2.width}')
            self.add_widget(self.btn1)
            self.add_widget(self.btn2)

            print(f'bt2 after add box w is: {self.btn2.width}')
        else:
            self.camera = Camera(resolution = (640,480), play = True, size_hint_y=0.8)
            btn2 = Button(text="Take Picture",size_hint_y=0.2)
            self.add_widget(self.camera)
            self.add_widget(btn2)

    def rotate_pic(self):
        if platform != "android":
            x_center = Window.size[0]*3/5
            y_center = Window.size[1]*self.btn1.size_hint_y/2
            with self.btn1.canvas.before:
                PushMatrix()
                Rotate(angle= -90,
                       origin = (500,300))
            with self.btn1.canvas.after:
                PopMatrix()
        else:
            x_center = Window.size[0]/2
            y_center = Window.size[1]*self.camera.size_hint_y/2
            with self.camera.canvas.before:
                PushMatrix()
                Rotate(angle= -90,
                       origin = (x_center,y_center))
            with self.camera.canvas.after:
                PopMatrix()

    def print_width(self,dt):
        print(print(f'bt1 after generated w is: {self.btn1.width}'))
        print(print(f'bt1 after generated w is: {self.btn1.height}'))
        print(print(f'bt1 after generated w is: {self.btn1.center}'))
        print(print(f'bt1 after generated w is: {self.center}'))
        print(print(f'bt1 after generated w is: {self.width}'))
        print(print(f'bt1 after generated w is: {self.height}'))


class rotated_button(Button):

    def __init__(self):
        super().__init__()

        self.text = "test"

        with self.canvas.before:
            PushMatrix()
            Rotate(angle= 50,
                   origin = (300,50))
            print (self.center)
            # self.camera.rot = Rotate()
            # self.camera.rot.angle  = -90
            # self.camera.rot.origin = self.center
        with self.canvas.after:
            PopMatrix()

    # def play(self, dt):
    #     self.camera.play = True

    # def take_picture(self):
    #     self.camera.export_to_png(r"/sdcard/dcim/camera/testtree.png")

# class MyCamera(Camera):
#     def __init__(self):
#         super().__init__()
#         self.resolution = (640,480)
#         self.size_hint_y=0.8
#         self.play = True
#         with self.canvas.before:
#             self.rot = Rotate()
#             self.rot.angle  = -90
#             self.rot.origin = self.center
#         with self.canvas.after:
#             PopMatrix()

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)





class MyMainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow(name='search_tree'))
        sm.add_widget(SecondWindow(name='view_tree'))
        sm.add_widget(TakeTreePic(name='take_pic'))
        return sm

if __name__ == "__main__":
    MyMainApp().run()