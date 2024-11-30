#Exercise 6 : Async Countdown Timer
import asyncio
import flet as ft


class CountdownTab:
    def __init__(self, label, seconds, page):
        self.label = label
        self.total_seconds = seconds
        self.seconds = seconds
        self.running = False
        self.cancel_requested = False
        self.page = page
        self.task = None

        # Timer UI components
        self.progress = ft.ProgressRing(value=0, width=100, height=100)
        self.timer_text = ft.Text(self._format_time(self.seconds), size=30)
        self.start_button = ft.ElevatedButton("Start", on_click=self.start_timer)
        self.pause_button = ft.ElevatedButton(
            "Pause", on_click=self.pause_timer, disabled=True
        )
        self.reset_button = ft.ElevatedButton(
            "Reset", on_click=self.reset_timer, disabled=True
        )

        # Layout for each timer tab
        self.content = ft.Column(
            [
                ft.Text(self.label, size=40, weight="bold"),
                self.timer_text,
                self.progress,
                ft.Row(
                    [self.start_button, self.pause_button, self.reset_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def _format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    async def update_timer(self):
        try:
            while self.running and self.seconds > 0:
                await asyncio.sleep(1)
                if self.cancel_requested:
                    break
                self.seconds -= 1
                self.timer_text.value = self._format_time(self.seconds)
                self.progress.value = 1 - (self.seconds / self.total_seconds)
                self.page.update()

            if self.seconds == 0:
                self.running = False
                self.start_button.disabled = False
                self.pause_button.disabled = True
                self.reset_button.disabled = False
                self.page.update()
        except asyncio.CancelledError:
            # Suppress the CancelledError to prevent propagation
            pass
        finally:
            # Ensure the task reference is cleared
            self.task = None

    def start_timer(self, e):
        if not self.running:
            self.running = True
            self.start_button.disabled = True
            self.pause_button.disabled = False
            self.reset_button.disabled = False
            self.cancel_requested = False  # Allow timer to continue running
            if not self.task:  # Create a new task if not already running
                self.task = self.page.run_task(self.update_timer)
            self.page.update()

    def pause_timer(self, e):
        if self.running:
            self.running = False  # Stop the timer logic
            self.cancel_requested = True  # Ensure the loop in `update_timer` breaks
            self.start_button.disabled = False
            self.pause_button.disabled = True
            self.page.update()

    def reset_timer(self, e):
        self.running = False
        self.cancel_task()  # Fully cancel the task
        self.seconds = self.total_seconds
        self.timer_text.value = self._format_time(self.seconds)
        self.progress.value = 0
        self.start_button.disabled = False
        self.pause_button.disabled = True
        self.reset_button.disabled = True
        self.page.update()

    def cancel_task(self):
        """Safely cancel the current task."""
        if self.task:
            try:
                self.cancel_requested = True
                self.task.cancel()
            except asyncio.CancelledError:
                pass
            finally:
                self.task = None


def main(page: ft.Page):
    page.title = "Multi Countdown Timer App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Create timer instances
    timer1 = CountdownTab("Timer 1", 120, page)
    timer2 = CountdownTab("Timer 2", 180, page)
    timer3 = CountdownTab("Timer 3", 300, page)

    timers = [timer1, timer2, timer3]

    # Navigation Drawer functionality
    def show_timer(index):
        # Pause all other timers when switching
        for i, timer in enumerate(timers):
            if i != index and timer.running:
                timer.pause_timer(None)

        # Clear previous content
        if len(page.controls) > 1:
            page.controls.pop(-1)

        # Add the selected timer content
        page.add(timers[index].content)
        page.update()

    # Define Navigation Drawer
    drawer = ft.NavigationDrawer(
        on_change=lambda e: show_timer(e.control.selected_index),
        controls=[
            ft.NavigationDrawerDestination(label="Timer 1", icon=ft.icons.TIMER),
            ft.NavigationDrawerDestination(label="Timer 2", icon=ft.icons.TIMER),
            ft.NavigationDrawerDestination(label="Timer 3", icon=ft.icons.TIMER),
        ],
    )

    # Add Menu Button and Default Timer
    page.add(
        ft.ElevatedButton("Open Menu", on_click=lambda e: page.open(drawer)),
        timer1.content,  # Default tab to display first
    )
    page.update()


ft.app(main)
