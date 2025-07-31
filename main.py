import flet as ft 
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo App'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enadle_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_task(e):
            main_db.update_task(task_id, task_field.value)
            page.update()
        
        return ft.Row([
            task_checkbox,
            task_field,
            ft.IconButton(ft.Icons.EDIT, on_click=enadle_edit, tooltip='Редактировать', icon_color=ft.Colors.ORANGE),
            ft.IconButton(ft.Icons.SAVE_ALT_ROUNDED, tooltip='Сохранить',
                          on_click=save_task, 
                          icon_color=ft.Colors.GREEN),
            ft.IconButton(ft.Icons.DELETE, tooltip='Удалить', 
                          on_click=lambda e: delete_task(task_id),
                          icon_color=ft.Colors.RED)
        ], alignment=ft.MainAxisAlignment.START)
    
    def add_task(e):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(
                create_task_row(task_id, task, None))
            task_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    def delete_task(task_id):
        main_db.delete_task(task_id)
        load_task()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    theme_toggle = ft.IconButton(
        icon=ft.Icons.BRIGHTNESS_6,
        tooltip="Переключить тему",
        on_click=toggle_theme
    )

    def clear_completed_tasks(e):
        main_db.clear_completed()
        load_task()

    clear_button = ft.IconButton(
        icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
        tooltip="Удалить выполненные",
        icon_color=ft.Colors.ORANGE,
        on_click=clear_completed_tasks
    )

    def clear_all_tasks(e):
        main_db.clear_all()
        load_task()

    clear_all_button = ft.IconButton(
        icon=ft.Icons.CLEANING_SERVICES_ROUNDED,
        tooltip="Удалить все продукты",
        icon_color=ft.Colors.RED,
        on_click=clear_all_tasks
    )

    task_input = ft.TextField(label='Введите задачу')
    add_button = ft.ElevatedButton("Добавить", on_click=add_task)

    filter_buttons = ft.Row(
        controls = [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Выполненные", on_click=lambda e: set_filter('completed')),
            ft.ElevatedButton("Не выполненные", on_click=lambda e: set_filter('uncompleted')),
            ft.ElevatedButton("В работе", on_click=lambda e: set_filter('in_work')),
            clear_button,
            clear_all_button
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    content = ft.Column([
        ft.Row([task_input, add_button, theme_toggle], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        filter_buttons,
        task_list
    ])

    background_image = ft.Image(
        src='/home/ramzan/Desktop/group_55_2_to_do_list/media/image copy.png',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack(controls=[background_image, content]) 

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resize = on_resize

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
