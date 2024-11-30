#Exercise 5: Navigation and Routing
import flet as ft


def main(page: ft.Page):
    page.title = "Flet picture viewer app"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    date_value = None 

    def date_picker(e):
        nonlocal date_value
        date_value = e.control.value 
        date_of_birth_field.value = date_value.strftime('%Y-%m-%d')
        page.update()

    def date_picker_dismissal(e):
        page.add(ft.Text("DatePicker dismissed"))

    def show_date_picker(e):
        page.open(
            ft.DatePicker(
                on_change=date_picker,
                on_dismiss=date_picker_dismissal,
            )
        )

    def login(e):
        email_error.value = ""
        password_error.value = ""

        if not email_input.value:
            email_error.value = "!Please write email"
        if not password_input.value:
            password_error.value = "!Please write password"

        if email_input.value and password_input.value:
            navigate_to_home(e)
        else:
            page.update()

    def navigate_to_home(e):
        page.views.append(home_view)
        page.update()

    def navigate_to_form(e):
        page.views.append(form_view)
        page.update()

    def navigate_to_details(e):
        name = name_input.value
        dob = date_of_birth_field.value  
        sex = sex_radio_group.value
        address = address_input.value
        country = country_dropdown.value

        if not name or dob == "Date not selected" or not address or not country:
            show_error_dialog("Please fill in all fields.")
            return

        details_view = ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Details"),
                    leading=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda e: page.views.pop() and page.update()
                    )
                ),
                ft.Card(
                    content=ft.Column([
                        ft.ListTile(
                            title=ft.Text(f"Name: {name}"),
                            subtitle=ft.Text(f"DOB: {dob}\nSex: {sex}\nAddress: {address}\nCountry: {country}"),
                        ),
                    ]),
                )
            ]
        )
        page.views.append(details_view)
        page.update()

    def show_error_dialog(message):
        def close_dialog(e):
            page.overlay.clear()
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        page.overlay.append(dialog)
        page.update()

    email_input = ft.TextField(label="Email", hint_text="Please enter email")
    email_error = ft.Text("", color="red", size=12)
    password_input = ft.TextField(label="Password", hint_text="Please enter password", password=True)
    password_error = ft.Text("", color="red", size=12)

    login_view = ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Login")),
            email_input,
            email_error,
            password_input,
            password_error,
            ft.ElevatedButton(text="Log In", on_click=login)
        ]
    )

    home_view = ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Home"), leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: page.views.pop() and page.update())),
            ft.ElevatedButton(text="Open Form", on_click=navigate_to_form),
        ]
    )

    name_input = ft.TextField(label="NAME", expand=True)
    date_of_birth_field = ft.TextField(label="Date of Birth", expand=True, read_only=True)
    dob_button = ft.ElevatedButton("Select Date", icon=ft.icons.CALENDAR_MONTH, on_click=show_date_picker)

    sex_radio_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Male", label="Male"),
            ft.Radio(value="Female", label="Female"),
            ft.Radio(value="Other", label="Other"),
        ])
    )

    address_input = ft.TextField(label="Address")

    country_dropdown = ft.Dropdown(
        label="Country",
        options=[
            ft.dropdown.Option("Bangladesh"),
            ft.dropdown.Option("Finland"),
            ft.dropdown.Option("Sweden"),
            ft.dropdown.Option("Others")
        ]
    )

    form_view = ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Form"), leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: page.views.pop() and page.update())),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[name_input],
                        expand=1
                    ),
                    ft.Column(
                        controls=[
                            ft.Row([date_of_birth_field, dob_button], spacing=10)
                        ],
                        expand=1
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            ft.Text("Sex"),
            sex_radio_group,  
            address_input,
            country_dropdown,
            ft.ElevatedButton(text="Create", on_click=navigate_to_details),
        ]
    )

    page.views.append(login_view)
    page.update()

ft.app(target=main)
