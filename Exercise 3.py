#Exercise 3 : Textfields, Buttons, and Dialogs
import flet as ft

def main(page: ft.Page):
    page.title = "Page Title"
    page.theme_mode = "light"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    name_field = ft.TextField(label="Name", width=300, autofocus=True)
    university_field = ft.TextField(label="University", width=300)
    
    output_list = ft.Column(spacing=5)

    def on_print_list_click(e):
        if name_field.value and university_field.value:
            output_list.controls.append(
                ft.Text(f"Hello {name_field.value} from {university_field.value}")
            )
            name_field.value = "" 
            university_field.value = ""
            page.update() 

    def on_print_dialog_click(e):
        if name_field.value and university_field.value:
            dlg = ft.AlertDialog(
                title=ft.Text(f"Hello {name_field.value} from {university_field.value}"),
                on_dismiss=lambda e: print("Dialog dismissed!"),
            )
            page.overlay.append(dlg)  
            dlg.open = True
            page.update()  
            
    page.add(
        ft.Column(
            [
                name_field,
                university_field,
                ft.Row(
                    [
                        ft.ElevatedButton(text="Print List", on_click=on_print_list_click),
                        ft.ElevatedButton(text="Print Dialog", on_click=on_print_dialog_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                output_list  
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
        )
    )

ft.app(target=main)
