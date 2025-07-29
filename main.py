import flet as ft
from db import main_db
from datetime import datetime

def main(page: ft.Page):
    page.title = "ToDo App"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    warning_text = ft.Text(value="", color=ft.Colors.RED)

    sort_by, sort_order = "date", False

    def parse_date(date_str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return datetime.min

    def toggle_status(task_id, is_done):
        main_db.update_status(task_id, int(is_done))
        load_task()

    def load_task(_=None):
        task_list.controls.clear()
        tasks = main_db.get_tasks()
        tasks = [
            (*t[:4], parse_date(t[2]))
            for t in tasks
        ]
        if sort_by == "date":
            tasks.sort(key=lambda x: x[4], reverse=not sort_order)
        else:
            tasks.sort(key=lambda x: x[3], reverse=sort_order)
        for task_id, task_text, created_at, is_done, _ in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, created_at, is_done))
        page.update()

    def create_task_row(task_id, task_text, created_at, is_done):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        date_text = ft.Text(value=created_at[:16], color=ft.Colors.GREY)
        done_checkbox = ft.Checkbox(value=bool(is_done), on_change=lambda e: toggle_status(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        return ft.Row(
            [
                done_checkbox,
                task_field,
                date_text,
                ft.IconButton(ft.Icons.EDIT, on_click=enable_edit, tooltip="Редактировать", icon_color=ft.Colors.BLUE),
                ft.IconButton(ft.Icons.SAVE_ALT_ROUNDED, tooltip="Сохранить", on_click=save_task, icon_color=ft.Colors.GREEN),
                ft.IconButton(ft.Icons.DELETE, tooltip="Удалить", icon_color=ft.Colors.RED, on_click=lambda e: delete_task(task_id)),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def add_task(_):
        text = task_input.value.strip()
        if not text:
            return
        if len(text) > 100:
            page.snack_bar = ft.SnackBar(content=ft.Text("❗Максимум 100 символов!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            return
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_id = main_db.add_task(text, created_at)
        task_list.controls.append(create_task_row(task_id, text, created_at, False))
        task_input.value = ''
        page.update()

    def delete_task(task_id):
        main_db.delete_task(task_id)
        load_task()

    def on_task_input_change(e):
        warning_text.value = "⚠️ Максимум 100 символов!" if len(task_input.value) > 100 else ""
        page.update()

    def change_sort(_):
        nonlocal sort_by, sort_order
        if sort_by == "date":
            if not sort_order:
                sort_order = True
                sort_button.text = "Сортировка: Дата (старые выше)"
            else:
                sort_by = "status"
                sort_order = False
                sort_button.text = "Сортировка: Статус (выполненные внизу)"
        elif sort_by == "status":
            if not sort_order:
                sort_order = True
                sort_button.text = "Сортировка: Статус (выполненные вверху)"
            else:
                sort_by = "date"
                sort_order = False
                sort_button.text = "Сортировка: Дата (новые выше)"
        load_task()

    task_input = ft.TextField(label='Введите задачу', max_length=100, on_change=on_task_input_change)
    add_button = ft.TextButton("Добавить", on_click=add_task)
    sort_button = ft.TextButton("Сортировка: Дата (новые выше)", on_click=change_sort)

    content = ft.Column(
        [
            ft.Row([task_input, add_button, sort_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            warning_text,
            task_list,
        ]
    )

    background_image = ft.Image(
        src="/home/ramzan/Desktop/group_55_2_to_do_list/media/image.png",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height,
    )

    background = ft.Stack(controls=[background_image, content])

    def on_resize(_):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resize = on_resize

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main, view=ft.WEB_BROWSER)
