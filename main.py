import flet as ft 
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo App'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_task(_):
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id, task_text))
        
        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, read_only=True)

        def enadle_edit(_):
            task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            page.update()

        return ft.Row([
            task_field, ft.IconButton(icon=ft.Icons.EDIT, on_click=enadle_edit,
                tooltip='Редактировать', icon_color=ft.Colors.BLUE
            ), ft.IconButton(ft.Icons.SAVE_ALT_ROUNDED, tooltip='Сохранить', 
                             on_click=save_task, icon_color=ft.Colors.GREEN),
            ft.IconButton(ft.Icons.DELETE, tooltip='Удалить', 
                          icon_color=ft.Colors.RED, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.START)
    
    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id, task))
            task_input.value = ''
            page.update()

    def delete_task(task_id):
        main_db.delete_task(task_id)
        load_task


    task_input = ft.TextField(label='Введите задачу')
    add_button = ft.TextButton('Добавить', on_click=add_task)

    # page.add(ft.Column([
    #     ft.Row([task_input, add_button],
    #     alignment=ft.MainAxisAlignment.SPACE_EVENLY),
    #     task_list
    # ]))

    content = ft.Column([
        ft.Row([task_input, add_button],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        task_list
    ])

    background_image = ft.Image(
        src='/home/ramzan/Desktop/group_55_2_to_do_list/media/image.png',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack(controls=[background_image, content])

    def on_resize(_):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resize = on_resize

    load_task(None)

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)