#Exercise 4 : Multi-counter App
import flet as ft

def main(page: ft.Page):
    page.title = "Multi-Counter App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "light"
    page.padding = 20

    counters = []

    def build_counter(counter_name, on_increment, on_decrement, on_delete):
        return ft.Row(
            controls=[
                ft.Text(counter_name, expand=1, text_align="start"),
                ft.IconButton(ft.icons.REMOVE, on_click=on_decrement, tooltip="Decrease"),
                ft.Container(ft.Text("0", ref=ft.Ref(), text_align="center"), width=50, alignment=ft.alignment.center),
                ft.IconButton(ft.icons.ADD, on_click=on_increment, tooltip="Increase"),
                ft.IconButton(ft.icons.DELETE, on_click=on_delete, tooltip="Delete")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=500,
            spacing=20
    )

    def add_counter(e):
        counter_name = input_name.value.strip()
        if counter_name:
            counter = ft.Container(
                build_counter(
                    counter_name,
                    on_increment=lambda _: increment_counter(counter),
                    on_decrement=lambda _: decrement_counter(counter),
                    on_delete=lambda _: delete_counter(counter)
                ),
                alignment=ft.alignment.center
            )
            counters.append(counter)
            page.add(counter)
            page.update()

    def delete_counter(counter):
        counters.remove(counter)
        page.remove(counter)
        page.update()

    def increment_counter(counter):
        value_control = counter.content.controls[2].content
        value = int(value_control.value) + 1
        value_control.value = str(value)
        page.update()

    def decrement_counter(counter):
        value_control = counter.content.controls[2].content
        value = int(value_control.value) - 1
        value_control.value = str(value)
        page.update()

    input_name = ft.TextField(hint_text="Enter counter name", expand=True)

    add_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=add_counter,
        tooltip="Add counter"
    )

    input_row = ft.Row(
        controls=[input_name, add_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=500,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Column(
            controls=[input_row],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)