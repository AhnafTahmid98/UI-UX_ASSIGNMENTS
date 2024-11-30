# Exercise 2 PART II

"""
# Counter APP
import flet as ft

def main(page: ft.Page):
    page.title = "Counter App"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    count = ft.Text(value="0", size=50)

    def increment(e):
        count.value = str(int(count.value) + 1)
        page.update()

    def decrement(e):
        count.value = str(int(count.value) - 1)
        page.update()

    page.add(
        count,
        ft.Row(
            controls=[
                ft.ElevatedButton("Increment", on_click=increment),
                ft.ElevatedButton("Decrement", on_click=decrement),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(target=main)

"""
# Modify the code to the increment/decrement to 2^n

import flet as ft

def main(page: ft.Page):
    page.title = "Counter App 2^n"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    count = ft.Text(value="0", size=50)
    n = 0  

    def increment(e):
        nonlocal n
        count.value = str(2**n)
        n += 1
        page.update()

    def decrement(e):
        nonlocal n
        n -= 1
        count.value = str(2**n)
        page.update()

    page.add(
        count,
        ft.Row(
            controls=[
                ft.ElevatedButton("Increment", on_click=increment),
                ft.ElevatedButton("Decrement", on_click=decrement),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(target=main)
