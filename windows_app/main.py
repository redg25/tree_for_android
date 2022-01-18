from kivy.app import App
from kivy.effects.scroll import ScrollEffect
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from postgres_util import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from typing import Dict
from trees import Tree, YoungTree
from postgres_util import *
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

columns: int = 20 #size of grid columns * columns
square_dictionary: Dict[str,Button] = {}  #Contains all the grid positions as key with their Button widget as value.

# creating the App class
class Grid_LayoutApp(App):

    def build(self):
        scrollv = ScrollView(effect_cls= ScrollEffect)
        layout = GridLayout(cols = columns,size_hint_y = None, size_hint_x = columns/25)
        layout.bind(minimum_height=layout.setter('height'))
        trees_collection = get_all_trees()
        for i in range(columns):
            for j in range(columns):
                position = f'{str(j)}-{str(i)}'
                key = [tree for tree in trees_collection if tree['position'] == position]
                if key != []:
                    btn = Button(text =key[0]['tag'],
                                 size = (20,20),
                                 size_hint_y=None,
                                 background_color = [0, 1, 0, 1],
                                 on_release = update_create_tree
                                 )
                    layout.add_widget(btn)
                else:
                    btn = Button(size = (20,20),
                                 size_hint_y=None,
                                 on_release = update_create_tree)
                    layout.add_widget(btn)
                square_dictionary[position]= btn
        scrollv.add_widget(layout)
        return scrollv


def update_create_tree(tree_btn:Button):
    """ Create a Tree instance and generate the popup to create/update tree in the database"""
    tree = create_tree_instance_from_db_values(tree_btn)

    pop_up_size = (root.root.size[0] * 0.8, root.root.size[1] * 0.8)
    popup_screen = ModalView(size_hint=(None, None),size=pop_up_size)
    popup_screen.add_widget(description_screen_layout(tree,tree_btn,popup_screen))
    popup_screen.open()

def get_pictures_of_tree(tag:str) -> list[str]:
    """Takes a tree tag and returns a list of all the urls of teh tree pictures"""
    list_of_treepics = []
    all_tree_pics = get_all_pics_from_a_tag(tag)
    for tree in all_tree_pics:
        list_of_treepics.append(tree['treepic'])
    return list_of_treepics

def create_tree_instance_from_db_values(tree_btn:Button) -> YoungTree:
    """Create a new Tree instance and assign attributes based on case: Update or Create tree"""
    tree = YoungTree()

    if tree_btn.text != '': #Update existing tree
        tree_from_db_dict = get_tree_from_tag(tree_btn.text)[0]
        tree.tag = tree_from_db_dict['tag']
        tree.position = tree_from_db_dict['position']
        tree.type = tree_from_db_dict['tree_type']
        tree.comments = tree_from_db_dict['comments']
    else:   #Create new tree
        tree.tag = ''
        tree.position = get_position_of_button(tree_btn)
        tree.type = ''
        tree.comments = ''
    return tree


# def get_tree_info(tag: str) -> dict:
#     """Get the tree info from the db using the tag parameter.
#     Returns it as a dictionary
#     """
#     query = f"Select * from TREES where TAG = '{tag}'"
#     tree_from_db = get_records(query)
#     return tree_from_db[0]


def description_screen_layout(tree: Tree, tree_btn:Button,popup_screen:ModalView)->BoxLayout:
    """Layout for the ModalView screen:
    """
    #values for the labels
    tag = 'tag'
    type = 'type'
    comments = 'commentaires'

    # store the text inputs widgets
    text_input_widgets = {'tag':None,'type':None,'commentaires':None}
    def save_tree(widget):
        """Update the Trees database with the values from the text inputs fields
        and close the popup"""
        new_values = {'tag':text_input_widgets[tag].text,
                      'tree_type':text_input_widgets[type].text,
                      'comments':text_input_widgets[comments].text,
                      'pictures':'http://test.com'}
        update_tree(text_input_widgets[tag].text,new_values)
        tree_btn.text = text_input_widgets[tag].text
        popup_screen.dismiss()

    def create_new_tree(widget):
        values = {
            'position':tree.position,
            'tag':text_input_widgets[tag].text,
            'tree_type':text_input_widgets[type].text,
            'comments':text_input_widgets[comments].text,
            'pictures':'http://test.com'}
        if values['comments']=='':
            values = {
                'position':tree.position,
                'tag':text_input_widgets[tag].text,
                'tree_type':text_input_widgets[type].text,
                'comments':'No comment',
                'pictures':'http://test.com'}
        create_tree(values)
        tree_btn.text = text_input_widgets[tag].text
        tree_btn.background_color = [0, 1, 0, 1]
        popup_screen.dismiss()

    #Boxlayout to contain the full Modalview screen
    description_boxlayout = BoxLayout(orientation='vertical')

    description_boxlayout.add_widget(Label(text=f"Description de l'arbre en position {tree.position}:",size_hint_y = 0.1))

    #values to create dynamically the diffent couple fields.
    #Each tuple contains (label as a string, default value as a string from the tree object)
    values = [(tag,tree.tag),(type,tree.type)]

    #Gridlayout with all the single line field text input
    trees_parameters_layout = GridLayout(cols=1, padding = 10, spacing = 10,size_hint_y = 0.3)
    for value in values:
        para_boxlayout = BoxLayout(orientation='horizontal',  spacing = 60, size_hint_y = 0.3)
        para_boxlayout.add_widget(Label(text=value[0],size_hint_x = 0.3))
        input = TextInput(text=value[1], size_hint_x = 0.56, multiline=False)
        #store the widget in the text_input_widgets dictionary
        text_input_widgets[value[0]]=input
        para_boxlayout.add_widget(input)
        para_boxlayout.add_widget(Label(text='',size_hint_x = 0.04))
        trees_parameters_layout.add_widget(para_boxlayout)

    #Boxlayout with the comments fields
    comment_boxlayout = BoxLayout(orientation='horizontal', spacing = 60, size_hint_y = 0.5)
    comment_boxlayout.add_widget(Label(text=comments,size_hint_x = 0.3))
    input = TextInput(text=tree.comments, size_hint_x = 0.56, multiline=True)
    #store the widget in the text_input_widgets dictionary
    text_input_widgets[comments]=input
    comment_boxlayout.add_widget(input)
    comment_boxlayout.add_widget(Label(text='',size_hint_x = 0.04))
    trees_parameters_layout.add_widget(comment_boxlayout)
    description_boxlayout.add_widget(trees_parameters_layout)

    #Boxlayout with the action buttons buttons
    btn_boxlayout = BoxLayout(orientation='horizontal',  spacing = 60, padding = 20, size_hint_y = 0.1)
    if tree.tag != '':
        btn_boxlayout.add_widget(Button(text="SAVE",on_release=save_tree))
    else:
        btn_boxlayout.add_widget(Button(text="CREATE",on_release=create_new_tree))
    btn_boxlayout.add_widget(Button(text="BACK",on_release=popup_screen.dismiss))
    description_boxlayout.add_widget(btn_boxlayout)
    pics_layout = carousel_layout(get_pictures_of_tree(tree.tag))
    description_boxlayout.add_widget(pics_layout,)
    lb = Label(text ='', size_hint_y = 0.1)
    description_boxlayout.add_widget(lb)
    return description_boxlayout

def carousel_layout(pics:list[str]) -> Carousel:
    carousel = Carousel(direction='right',size_hint_y = 0.4)
    for pic in pics:
        src = f"{pic}"
        image = AsyncImage(source=src, allow_stretch=True)
        carousel.add_widget(image)
    return carousel


def get_position_of_button(btn):
    # list out keys and values separately
    key_list = list(square_dictionary.keys())
    val_list = list(square_dictionary.values())

    # print key with val 100
    position = val_list.index(btn)
    return (key_list[position])

root = Grid_LayoutApp()
root.run()
