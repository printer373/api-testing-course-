import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

from models import (
    all_users,
    find_user,
    user_by_login,
    login_exists,
    add_user,
    update_user,
    delete_user,
    unlock_user,
    register_fail,
    reset_attempts,
)

CURRENT_USER = None
CURRENT_EDIT = None
ENTRY_LOGIN = None

# Colors
BG = "#365F88"
FIELD_BG = "#FFFFFF"
FIELD_FG = "#FFFFFF"

FONT_TITLE = ("Segoe UI", 16, "bold italic")
FONT_LABEL = ("Segoe UI", 10, "italic")
FONT_LABEL_NORMAL = ("Segoe UI", 11, "bold")
FONT_BUTTON = ("Segoe UI", 11, "bold")

root = tk.Tk()
root.title("Учебное приложение")

window_width = 720
window_height = 640
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.configure(bg=BG)

container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True, padx=20, pady=20)


def clear_screen():
    for widget in container.winfo_children():
        widget.destroy()


def make_title(text):
    return tk.Label(container, text=text, bg=BG, fg=FIELD_FG, font=FONT_TITLE)


def make_label(text, italic=False):
    f = FONT_LABEL if italic else FONT_LABEL_NORMAL
    return tk.Label(
        container, text=text, bg=BG, fg=FIELD_FG, font=f, anchor="w"
    )


def make_entry(password=False):
    entry = tk.Entry(
        container,
        font=FONT_BUTTON,
        bg=FIELD_BG,
        fg=FIELD_FG,
        insertbackground=FIELD_FG,
        relief="solid",
        borderwidth=1,
    )
    if password:
        entry.configure(show="*")
    return entry


def make_button(text, command, parent=None):
    host = container if parent is None else parent
    return tk.Button(host, text=text, command=command, font=FONT_BUTTON)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTCHA_DIR = os.path.join(BASE_DIR, "captcha")
CORRECT_ORDER = [1, 2, 3, 4]
PIECE_SIZE = 90

captcha_images = {}
captcha_empty = None
captcha_host = None
captcha_slots = []
captcha_piece_buttons = {}
captcha_placed = []
captcha_shuffled = []
captcha_passed = False
captcha_fails = 0

dragging_piece = None
drag_feedback_label = None


def load_captcha_images():
    global captcha_images, captcha_empty
    captcha_images = {}
    for piece in (1, 2, 3, 4):
        path = os.path.join(CAPTCHA_DIR, "piece_" + str(piece) + ".png")
        captcha_images[piece] = tk.PhotoImage(file=path).subsample(8)
    captcha_empty = tk.PhotoImage(width=PIECE_SIZE, height=PIECE_SIZE)


def build_captcha(host):
    global captcha_slots, captcha_piece_buttons, captcha_placed, captcha_shuffled

    for widget in host.winfo_children():
        widget.destroy()

    captcha_slots = []
    captcha_piece_buttons = {}
    captcha_placed = []
    captcha_shuffled = CORRECT_ORDER[:]
    random.shuffle(captcha_shuffled)
    while captcha_shuffled == CORRECT_ORDER:
        random.shuffle(captcha_shuffled)

    make_label("Соберите картинку: перетащите фрагменты мышью в слоты по порядку", italic=True).pack(fill="x", pady=(0, 4))

    board = tk.Frame(host, bg=BG)
    board.pack(pady=(2, 6))
    for index in range(4):
        slot = tk.Label(
            board,
            image=captcha_empty,
            bg=FIELD_BG,
            relief="solid",
            borderwidth=1,
        )
        slot.grid(row=index // 2, column=index % 2, padx=2, pady=2)
        captcha_slots.append(slot)

    pieces = tk.Frame(host, bg=BG)
    pieces.pack(pady=(0, 6))
    for piece in captcha_shuffled:
        btn = tk.Label(
            pieces,
            image=captcha_images[piece],
            bg=FIELD_BG,
            relief="solid",
            borderwidth=1,
            cursor="hand2",
        )
        btn.bind("<Button-1>", lambda event, p=piece: start_drag(event, p))
        btn.bind("<B1-Motion>", do_drag)
        btn.bind("<ButtonRelease-1>", lambda event, p=piece: stop_drag(event, p))
        
        btn.pack(side="left", padx=3)
        captcha_piece_buttons[piece] = btn

    make_button("Сбросить капчу", new_captcha_round, parent=host).pack(
        ipadx=16, ipady=3
    )


def start_drag(event, piece):
    global dragging_piece, drag_feedback_label
    if captcha_passed or len(captcha_placed) >= 4 or piece in captcha_placed:
        return
    dragging_piece = piece
    
    drag_feedback_label = tk.Toplevel(root)
    drag_feedback_label.overrideredirect(True)
    drag_feedback_label.attributes("-topmost", True)
    lbl = tk.Label(drag_feedback_label, image=captcha_images[piece], bg=FIELD_BG, relief="solid", borderwidth=1)
    lbl.pack()
    drag_feedback_label.geometry(f"+{event.x_root+10}+{event.y_root+10}")


def do_drag(event):
    global drag_feedback_label
    if drag_feedback_label:
        drag_feedback_label.geometry(f"+{event.x_root+10}+{event.y_root+10}")


def stop_drag(event, piece):
    global dragging_piece, drag_feedback_label
    if drag_feedback_label:
        drag_feedback_label.destroy()
        drag_feedback_label = None

    if captcha_passed or len(captcha_placed) >= 4 or piece in captcha_placed:
        dragging_piece = None
        return

    x, y = event.x_root, event.y_root
    for index, slot in enumerate(captcha_slots):
        if len(captcha_placed) == index:
            x1 = slot.winfo_rootx()
            y1 = slot.winfo_rooty()
            x2 = x1 + slot.winfo_width()
            y2 = y1 + slot.winfo_height()
            if x1 <= x <= x2 and y1 <= y <= y2:
                captcha_placed.append(piece)
                captcha_piece_buttons[piece].configure(bg=FIELD_BG)
                captcha_piece_buttons[piece].unbind("<Button-1>")
                captcha_piece_buttons[piece].unbind("<B1-Motion>")
                captcha_piece_buttons[piece].unbind("<ButtonRelease-1>")
                slots_index = len(captcha_placed) - 1
                captcha_slots[slots_index].configure(image=captcha_images[piece])
                
                if len(captcha_placed) == 4:
                    check_captcha()
                break
    dragging_piece = None


def new_captcha_round():
    global captcha_passed
    captcha_passed = False
    build_captcha(captcha_host)


def place_piece(piece):
    if captcha_passed or len(captcha_placed) >= 4:
        return
    captcha_placed.append(piece)
    captcha_piece_buttons[piece].configure(state="disabled")
    captcha_slots[len(captcha_placed) - 1].configure(image=captcha_images[piece])
    if len(captcha_placed) == 4:
        check_captcha()


def check_captcha():
    global captcha_passed, captcha_fails

    login = ENTRY_LOGIN.get().strip()

    if captcha_placed == CORRECT_ORDER:
        captcha_passed = True
        messagebox.showinfo(
            "Капча", "Пазл собран верно. Теперь можно нажимать «Войти»."
        )
        return

    if login_exists(login):
        became_locked = register_fail(login)
        if became_locked:
            messagebox.showerror(
                "Блокировка", "Вы заблокированы. Обратитесь к администратору"
            )
        else:
            messagebox.showerror(
                "Капча",
                "Пазл собран неверно. Попробуйте собрать ещё раз, "
                "ориентируясь на продолжение рисунка.",
            )
    else:
        captcha_fails = captcha_fails + 1
        if captcha_fails >= 3:
            messagebox.showerror(
                "Блокировка",
                "Третья неверная сборка капчи подряд. "
                "При входе учётная запись будет заблокирована.",
            )
        else:
            messagebox.showerror(
                "Капча",
                "Пазл собран неверно. Попробуйте собрать ещё раз, "
                "ориентируясь на продолжение рисунка.",
            )

    new_captcha_round()


def try_login(login, password):
    global CURRENT_USER, captcha_fails

    login = login.strip()
    password = password.strip()

    if not login or not password:
        messagebox.showwarning("Внимание", "Заполните логин и пароль.")
        return

    if captcha_fails > 0:
        if login_exists(login):
            for _ in range(captcha_fails):
                register_fail(login)
            captcha_fails = 0

    if not captcha_passed:
        messagebox.showwarning(
            "Капча", "Сначала соберите капчу, затем нажимайте «Войти»."
        )
        return

    user = find_user(login, password)
    if user is None:
        became_locked = register_fail(login)
        if became_locked:
            messagebox.showerror(
                "Блокировка", "Вы заблокированы. Обратитесь к администратору"
            )
        else:
            messagebox.showerror(
                "Ошибка входа",
                "Вы ввели неверный логин или пароль. "
                "Пожалуйста проверьте ещё раз введенные данные",
            )
        return

    if user["locked"]:
        messagebox.showerror(
            "Блокировка", "Вы заблокированы. Обратитесь к администратору"
        )
        return

    reset_attempts(login)
    CURRENT_USER = user
    messagebox.showinfo("Авторизация", "Вы успешно авторизовались")
    new_captcha_round()

    if user["role"] == "Администратор":
        open_admin()
    else:
        open_user()


def toggle_password_visibility(entry_pass, var):
    if var.get():
        entry_pass.configure(show="")
    else:
        entry_pass.configure(show="*")


def open_login():
    global ENTRY_LOGIN, captcha_host

    clear_screen()
    make_title("Вход в систему").pack(pady=(0, 10))

    make_label("Логин").pack(fill="x")
    ENTRY_LOGIN = make_entry()
    ENTRY_LOGIN.pack(fill="x", pady=(0, 8))

    make_label("Пароль").pack(fill="x")
    entry_pass = make_entry(password=True)
    entry_pass.pack(fill="x", pady=(0, 4))

    show_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        container,
        text="Показать пароль",
        variable=show_var,
        command=lambda: toggle_password_visibility(entry_pass, show_var),
        bg=BG,
        fg=FIELD_FG,
        activebackground=BG,
        activeforeground=FIELD_FG,
        selectcolor=FIELD_BG,
        font=FONT_LABEL_NORMAL,
        anchor="w",
    ).pack(fill="x", pady=(0, 10))

    captcha_host = tk.Frame(container, bg=BG)
    captcha_host.pack(fill="x", pady=(0, 10))
    build_captcha(captcha_host)

    make_button(
        "Войти", lambda: try_login(ENTRY_LOGIN.get(), entry_pass.get())
    ).pack(fill="x", ipady=6)


def open_user():
    clear_screen()
    make_title("Рабочее место пользователя").pack(pady=(0, 10))
    make_label("Вы вошли как: " + CURRENT_USER["login"]).pack(
        fill="x", pady=(0, 6)
    )
    make_label("Роль: " + CURRENT_USER["role"]).pack(fill="x", pady=(0, 20))
    make_button("Выйти", open_login).pack(ipadx=24, ipady=4)


def open_edit_user(login):
    global CURRENT_EDIT

    user = user_by_login(login)
    if user is None:
        messagebox.showwarning("Внимание", "Сначала выберите строку в таблице.")
        return

    CURRENT_EDIT = login
    clear_screen()
    make_title("Изменение пользователя").pack(pady=(0, 10))
    make_label("Логин: " + login).pack(fill="x", pady=(0, 10))

    make_label("ФИО").pack(fill="x")
    e_name = make_entry()
    e_name.insert(0, user["full_name"])
    e_name.pack(fill="x", pady=(0, 8))

    make_label("Пароль").pack(fill="x")
    e_pass = make_entry()
    e_pass.insert(0, user["password"])
    e_pass.pack(fill="x", pady=(0, 8))

    make_label("Роль").pack(fill="x")
    combo_role = ttk.Combobox(
        container,
        values=["Пользователь", "Администратор"],
        state="readonly",
        font=FONT_BUTTON,
    )
    combo_role.set(user["role"])
    combo_role.pack(fill="x", pady=(0, 10))

    lock_text = "Заблокирован: да" if user["locked"] else "Заблокирован: нет"
    lock_label = make_label(lock_text)
    lock_label.pack(fill="x", pady=(0, 10))

    def refresh_lock():
        current = user_by_login(CURRENT_EDIT)
        lock_label.configure(
            text="Заблокирован: да" if current["locked"] else "Заблокирован: нет"
        )

    def do_unlock():
        unlock_user(CURRENT_EDIT)
        refresh_lock()
        messagebox.showinfo(
            "Готово", "Пользователь " + CURRENT_EDIT + " разблокирован."
        )

    def do_save():
        name = e_name.get().strip()
        password = e_pass.get().strip()
        if not name or not password:
            messagebox.showwarning(
                "Внимание", "ФИО и пароль не могут быть пустыми."
            )
            return
        update_user(CURRENT_EDIT, password, combo_role.get(), name)
        messagebox.showinfo("Готово", "Данные пользователя сохранены.")
        open_admin()

    def do_delete():
        if CURRENT_EDIT == "admin":
            messagebox.showerror(
                "Ошибка", "Учётную запись администратора удалять нельзя."
            )
            return
        if messagebox.askyesno(
            "Удаление", "Удалить пользователя " + CURRENT_EDIT + "?"
        ):
            delete_user(CURRENT_EDIT)
            messagebox.showinfo("Готово", "Пользователь удалён.")
            open_admin()

    row = tk.Frame(container, bg=BG)
    row.pack(fill="x")
    make_button("Сохранить", do_save, parent=row).pack(
        side="left", padx=(0, 6)
    )
    make_button("Разблокировать", do_unlock, parent=row).pack(
        side="left", padx=(0, 6)
    )
    make_button("Удалить", do_delete, parent=row).pack(
        side="left", padx=(0, 6)
    )
    make_button("Отмена", open_admin, parent=row).pack(side="right")


def open_admin():
    clear_screen()
    make_title("Панель администратора").pack(pady=(0, 5))
    make_label("Вы вошли как: " + CURRENT_USER["login"]).pack(
        fill="x", pady=(0, 10)
    )

    tree = ttk.Treeview(
        container,
        columns=("login", "full_name", "role", "locked"),
        show="headings",
        height=8,
    )
    tree.heading("login", text="Логин")
    tree.heading("full_name", text="ФИО")
    tree.heading("role", text="Роль")
    tree.heading("locked", text="Заблокирован")
    tree.column("login", width=120, anchor="w")
    tree.column("full_name", width=180, anchor="w")
    tree.column("role", width=130, anchor="w")
    tree.column("locked", width=110, anchor="center")

    for user in all_users():
        tree.insert(
            "",
            "end",
            values=(
                user["login"],
                user["full_name"],
                user["role"],
                "да" if user["locked"] else "нет",
            ),
        )

    tree.pack(fill="both", expand=True, pady=(0, 10))

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(
                "Внимание", "Сначала выберите строку в таблице."
            )
            return
        open_edit_user(tree.item(selected[0])["values"][0])

    row = tk.Frame(container, bg=BG)
    row.pack(fill="x")
    make_button("Добавить", open_add_user, parent=row).pack(
        side="left", padx=(0, 6)
    )
    make_button("Изменить", edit_selected, parent=row).pack(
        side="left", padx=(0, 6)
    )
    make_button("Выйти", open_login, parent=row).pack(side="right")


def save_user(login, password, role, full_name):
    login = login.strip()
    password = password.strip()

    if not login or not password or not full_name.strip():
        messagebox.showwarning(
            "Внимание", "Логин, пароль и ФИО не могут быть пустыми."
        )
        return

    if login_exists(login):
        messagebox.showerror("Ошибка", "Такой логин уже существует.")
        return

    add_user(login, password, role, full_name.strip())
    messagebox.showinfo("Готово", "Пользователь " + login + " добавлен.")
    open_admin()


def open_add_user():
    clear_screen()
    make_title("Новый пользователь").pack(pady=(0, 15))

    make_label("Логин").pack(fill="x")
    e_login = make_entry()
    e_login.pack(fill="x", pady=(0, 10))

    make_label("ФИО").pack(fill="x")
    e_name = make_entry()
    e_name.pack(fill="x", pady=(0, 10))

    make_label("Пароль").pack(fill="x")
    e_pass = make_entry()
    e_pass.pack(fill="x", pady=(0, 10))

    make_label("Роль").pack(fill="x")
    combo_role = ttk.Combobox(
        container,
        values=["Пользователь", "Администратор"],
        state="readonly",
        font=FONT_BUTTON,
    )
    combo_role.current(0)
    combo_role.pack(fill="x", pady=(0, 15))

    make_button(
        "Сохранить",
        lambda: save_user(
            e_login.get(), e_pass.get(), combo_role.get(), e_name.get()
        ),
    ).pack(fill="x", ipady=6)

    make_button("Отмена", open_admin).pack(fill="x", pady=(8, 0), ipady=4)


load_captcha_images()
open_login()
root.mainloop()