import random,ast,math
import dearpygui.dearpygui as dpg
dpg.create_context()

with open('data.json') as f:
    data = ast.literal_eval(f.read())
print(data) 
current_table={
"name":'NESSUNA TABELLA APERTA',
"group":[],
"size":(0,0),
"table":[],
}
group_list=[]


def save(sender,app_data):
    global data
    new_file={
    "name":'',
    "group":[],
    "size":(0,0),
    "table":[],
    }
    new_file["name"]=dpg.get_value("table_name")
    new_file["group"]=dpg.get_value("group").split('\n')
    new_file["size"]=(dpg.get_value("table_width"),dpg.get_value("table_height"))
    for i in range(dpg.get_value("table_height")):
        for j in range(dpg.get_value("table_width")):
            new_file["table"].append(dpg.get_value(f"{i},{j}"))

    data.append(new_file)
    print(data)
    dpg.delete_item("table_configuration")
    dpg.delete_item("new")
    dpg.delete_item("selection")

def pick_random():
    dpg.delete_item("pick_random")
    with dpg.window(label="sorteggio casuale",tag="pick_random"):
        with dpg.group(horizontal=True):
            dpg.add_text("numero di persone da sorteggiare:")
            dpg.add_slider_int(width=150,min_value=1,default_value=1,max_value=len(current_table["group"]))
        dpg.add_text("lista di sorteggio:")
        with dpg.popup(dpg.last_item()):
            dpg.add_text("fancy ahh tooltip")
            """
            for p in current_table["group"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(p)
                    dpg.add_checkbox(default_value=True)"""

def open_table(sender,app_data,user_data):  
    global current_table,group_list
    current_table=data[user_data]
    group_list=['??????' for i in range(len(current_table["group"]))]
    selection()
    main()

def delete_table(sender,app_data,user_data):
    global data
    del data[user_data]
    selection()

def refresh():
    global current_table,group_list
    group_list=random.sample(current_table["group"],k=len(current_table["group"]))
    dpg.delete_item("table_configuration")
    dpg.delete_item("new")
    dpg.delete_item("selection")
    main()

def table_configuration():
    dpg.delete_item("table_configuration")
    with dpg.window(label="configura tabella",tag="table_configuration"):
        with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,
            borders_outerH=True, borders_innerV=True, borders_outerV=True):
            for i in range(dpg.get_value("table_width")):
                dpg.add_table_column()
            for i in range(dpg.get_value("table_height")):
                with dpg.table_row():
                    for j in range(dpg.get_value("table_width")):
                        dpg.add_checkbox(tag=f"{i},{j}")  
def new_table():
    dpg.delete_item("new")
    with dpg.window(label="nuovo",tag="new",autosize=True):
        with dpg.group(horizontal=True):
            dpg.add_text("nome schema:")
            dpg.add_input_text(tag="table_name")
        dpg.add_text("aggiungi nomi degli studenti:")
        dpg.add_input_text(multiline=True,tag="group")
        with dpg.group(horizontal=True):
            dpg.add_text("inserisci dimensioni schema:")
            dpg.add_slider_int(width=50,min_value=3,default_value=10,max_value=20,tag="table_width")
            dpg.add_slider_int(width=50,min_value=3,default_value=10,max_value=20,tag="table_height")
            dpg.add_button(label="configura tabella",callback=table_configuration)
        dpg.add_button(label="conferma e salva",callback=save)

def selection():
    dpg.delete_item("selection")
    with dpg.window(label="seleziona schema",tag="selection",autosize=True):
        if len(data)>0:
            for i,item in enumerate(data):
                with dpg.group(horizontal=True):
                    dpg.add_button(label=item["name"],width=500,callback=open_table,user_data=i)
                    dpg.add_button(label="elimina",callback=delete_table,user_data=i)
        else:
            dpg.add_text("nessuno schema presente!")     

def main():
    global current_table,data,group_list
    dpg.delete_item("main")
    with dpg.window(tag="main"):
        with dpg.menu_bar():
            dpg.add_button(label="apri schema",callback=selection)
            dpg.add_button(label="nuovo schema",callback=new_table)
            dpg.add_button(label="sorteggio casuale",callback=pick_random)

        dpg.add_text("\nschema: "+current_table["name"])
        dpg.add_button(label="genera nuovi posti",callback=refresh)
        with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,borders_outerH=True, borders_innerV=True, borders_outerV=True):
            iter=0
            for i in range(current_table["size"][0]):
                dpg.add_table_column()
            for i in range(current_table["size"][1]):
                with dpg.table_row():
                    for j in range(current_table["size"][0]):
                        if current_table["table"][current_table["size"][0]*i+j]:
                            dpg.add_text(group_list[iter])
                            iter+=1
                        else:
                            dpg.add_checkbox()
    dpg.set_primary_window("main", True)

try:
    with dpg.font_registry():
        default_font=dpg.add_font("AtomicMd-OVJ4A.otf",21)
    dpg.bind_font(default_font)
except:
    pass
main()
viewport=dpg.create_viewport(title='generatore posti',width=1200,height=500,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
with open('data.json','w') as f:
    f.write(str(data))