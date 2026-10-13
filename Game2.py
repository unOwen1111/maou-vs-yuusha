
import tkinter
import random

player_hp = 250
enemy_hp = 250
player_buff = 1.0
enemy_buff = 1.0
button_num = 0

root = tkinter.Tk()
root.title("魔王VS勇者")
root.geometry("800x600")
root.config(bg="black")

battle_canvas = tkinter.Canvas(root, bg="black", highlightthickness=0)
battle_canvas.pack(fill="both", expand=True)


# ========================================
# ボタン入力
# ========================================

def button_click(action_num):
    global button_num
    button_num = action_num


# ========================================
# 勇者の技
# ========================================

def hyper_slash():
    global enemy_hp, player_buff

    if random.randint(1, 100) <= 90:
        damage = int(10 * player_buff )
        enemy_hp -= damage
        enemy_hp = max(0, enemy_hp)
        show_message("ハイパースラッシュ！\n" + str(damage) + "ダメージ！")
    else:
        show_message("ハイパースラッシュ！\n攻撃が外れた！")

    player_buff = 1.0


def ultra_burst():
    global enemy_hp, player_buff

    if random.randint(1, 100) <= 80:
        damage = int(30 * player_buff)
        show_message("ウルトラバースト！\n" + str(damage) + "ダメージ！")

        enemy_hp -= damage
        enemy_hp = max(0, enemy_hp)
    else:
        show_message("ウルトラバースト！\n攻撃が外れた！")

    player_buff = 1.0


def super_heal():
    global player_hp

    heal_amount = min(40, 250 - player_hp)
    player_hp += heal_amount
    show_message("スーパーヒール！\n" + str(heal_amount) + "の回復！")


def miracle_boost():
    global player_buff

    show_message("ミラクルブースト！\n次の攻撃が2倍になる！")
    player_buff = 2.0


# ========================================
# 魔王の技
# ========================================

def dark_slash():
    global player_hp, enemy_buff

    if random.randint(1, 100) <= 90:
        damage = int(20 * enemy_buff)
        player_hp -= damage
        player_hp = max(0, player_hp)
        show_message("ダークスラッシュ！\n" + str(damage) + "ダメージ！")
    else:
        show_message("ダークスラッシュ！\n攻撃が外れた！")

    enemy_buff = 1.0


def hell_fire():
    global player_hp, enemy_buff

    if random.randint(1, 100) <= 80:
        damage = int(50 * enemy_buff)
        player_hp -= damage
        player_hp = max(0, player_hp)
        show_message("ヘルファイア！\n" + str(damage) + "ダメージ！")
    else:
        show_message("ヘルファイア！\n攻撃が外れた！")

    enemy_buff = 1.0


def dark_drain():
    global player_hp, enemy_hp, enemy_buff

    if random.randint(1, 100) <= 90:
        damage = int(20 * enemy_buff)
        actual_damage = min(player_hp, damage)

        player_hp -= actual_damage
        enemy_hp = min(250, enemy_hp + actual_damage)

        show_message(
            "ダークドレイン！\n"
            + str(actual_damage) + "ダメージ！\n"
            + "魔王は" + str(actual_damage) + "回復！"
        )
    else:
        show_message("ダークドレイン！\n攻撃が外れた！")

    enemy_buff = 1.0


def demonic_boost():
    global enemy_buff

    show_message("デモニックブースト！\n魔王の次の攻撃が2倍になる！")
    enemy_buff = 2.0


# ========================================
# ボタン操作
# ========================================

def enable_buttons():
    slash_button.config(state="normal")
    magic_button.config(state="normal")
    heal_button.config(state="normal")
    buff_button.config(state="normal")


def disable_buttons():
    slash_button.config(state="disabled")
    magic_button.config(state="disabled")
    heal_button.config(state="disabled")
    buff_button.config(state="disabled")


# ========================================
# リスタート
# ========================================

def restart_game():
    global player_hp, enemy_hp
    global player_buff, enemy_buff, button_num

    player_hp = 250
    enemy_hp = 250
    player_buff = 1.0
    enemy_buff = 1.0
    button_num = 0

    update_hp_bars()

    background_label.config(image=battle_background_image)

    message_label.place_forget()

    restart_button.place_forget()

    enable_buttons()

    root.after(100, player_turn)


# ========================================
# HPバー更新
# ========================================

def update_hp_bars():

    player_hp_value_label.config(text=str(player_hp))
    enemy_hp_value_label.config(text=str(enemy_hp))
    
    battle_canvas.coords(player_hp_bar, 70, 45, 70 + player_hp, 65)
    battle_canvas.coords(enemy_hp_bar, 470, 45, 470 + enemy_hp, 65)

    if player_hp <= 50:
        battle_canvas.itemconfig(player_hp_bar, fill="red")
    elif player_hp <= 100:
        battle_canvas.itemconfig(player_hp_bar, fill="yellow")
    else:
        battle_canvas.itemconfig(player_hp_bar, fill="green")

    if enemy_hp <= 50:
        battle_canvas.itemconfig(enemy_hp_bar, fill="red")
    elif enemy_hp <= 100:
        battle_canvas.itemconfig(enemy_hp_bar, fill="yellow")
    else:
        battle_canvas.itemconfig(enemy_hp_bar, fill="green")


# ========================================
# 勝敗判定
# ========================================

def check_game_end() -> bool:
    if player_hp <= 0:
        disable_buttons()
        background_label.config(image=demon_win_image)
        restart_button.place(relx=0.5, rely=0.6, anchor="center")
        return True

    if enemy_hp <= 0:
        disable_buttons()
        background_label.config(image=hero_win_image)
        restart_button.place(relx=0.5, rely=0.6, anchor="center")
        return True

    return False


# ========================================
# バフリセット
# ========================================

def player_buff_reset():
    global player_buff
    player_buff = 1.0


def enemy_buff_reset():
    global enemy_buff
    enemy_buff = 1.0


# ========================================
# メッセージ
# ========================================

def show_message(message):
    message_label.config(text=message)
    message_label.place(relx=0.5, rely=0.5, anchor="center")


def hide_message():
    message_label.place_forget()


# ========================================
# メイン処理
# ========================================

def player_turn():
    global button_num

    ### 勇者ターン ###

    enable_buttons()

    # ボタンが押されるまで待機
    if button_num == 0:
        root.after(100, player_turn)
        return

    disable_buttons()

    select_action = button_num
    button_num = 0

    if select_action == 1:
        hyper_slash()
    elif select_action == 2:
        ultra_burst()
    elif select_action == 3:
        super_heal()
    elif select_action == 4:
        miracle_boost()

    # 3秒後に次の処理
    root.after(3000, after_player_turn)


def after_player_turn():

    update_hp_bars()

    # メッセージを消す
    hide_message()

    # 勝敗判定
    if check_game_end():
        return

    # 魔王のターン
    enemy_turn()


def enemy_turn():
    ### 魔王ターン ###

    dice = random.randint(1, 6)

    if dice == 1:
        hell_fire()
    elif dice == 2 or dice == 3:
        dark_slash()
    elif dice == 4 or dice == 5:
        dark_drain()
    else:
        demonic_boost()

    root.after(3000, after_enemy_turn)


def after_enemy_turn():

    update_hp_bars()

    hide_message()

    # 勝敗判定
    if check_game_end():
        return

    # 次の勇者ターン
    player_turn()


# ========================================
# 背景画像
# ========================================

battle_background_image = tkinter.PhotoImage(file="battle_background.png")
battle_background_image = battle_background_image.subsample(3, 3)
hero_win_image = tkinter.PhotoImage(file="hero_win.png")
hero_win_image = hero_win_image.subsample(3, 3)
demon_win_image = tkinter.PhotoImage(file="demon_win.png")
demon_win_image = demon_win_image.subsample(3, 3)

background_label = tkinter.Label(root, image=battle_background_image)
background_label.place(x=120, y=100)


# ========================================
# ボタン
# ========================================

slash_button = tkinter.Button(
    root,
    text="ハイパースラッシュ(10ダメージ, 90%命中)",
    command=lambda: button_click(1),
    width=50,
    height=3
)
slash_button.place(x=40, y=450)

magic_button = tkinter.Button(
    root,
    text="ウルトラバースト(30ダメージ, 80%命中)",
    command=lambda: button_click(2),
    width=50,
    height=3
)
magic_button.place(x=400, y=450)

heal_button = tkinter.Button(
    root,
    text="スーパーヒール(40回復)",
    command=lambda: button_click(3),
    width=50,
    height=3
)
heal_button.place(x=40, y=500)

buff_button = tkinter.Button(
    root,
    text="ミラクルブースト(次の攻撃が2倍)",
    command=lambda: button_click(4),
    width=50,
    height=3
)
buff_button.place(x=400, y=500)

restart_button = tkinter.Button(
    root,
    text="リスタート",
    command=restart_game,
    width=50,
    height=3
)


# ========================================
# ラベルとHPバー
# ========================================

player_hp_label = tkinter.Label(
    root, text="HP", font=("Arial", 16, "bold"),
    fg="white", bg=root["bg"]
)
player_hp_label.place(x=30, y=40)

player_hp_value_label = tkinter.Label(
    root, text="250", font=("Arial", 8),
    fg="white", bg=root["bg"]
)
player_hp_value_label.place(x=180, y=25)


player_name_label = tkinter.Label(
    root, text="勇者", font=("Arial", 16, "bold"),
    fg="white", bg=root["bg"]
)
player_name_label.place(x=10, y=5)

battle_canvas.create_rectangle(
    20, 20, 350, 80,
    fill="", outline="gray", width=5
)

player_hp_bar_back = battle_canvas.create_rectangle(
    70, 45, 320, 65, fill="lightgray"
)
player_hp_bar = battle_canvas.create_rectangle(
    70, 45, 320, 65, fill="green"
)


enemy_hp_label = tkinter.Label(
    root, text="HP", font=("Arial", 16, "bold"),
    fg="white", bg=root["bg"]
)
enemy_hp_label.place(x=430, y=40)

enemy_hp_value_label = tkinter.Label(
    root, text="250", font=("Arial", 8),
    fg="white", bg=root["bg"]
)
enemy_hp_value_label.place(x=580, y=25)

enemy_name_label = tkinter.Label(
    root, text="魔王", font=("Arial", 16, "bold"),
    fg="white", bg=root["bg"]
)
enemy_name_label.place(x=410, y=5)


battle_canvas.create_rectangle(
    420, 20, 750, 80,
    fill="", outline="gray", width=5
)

enemy_hp_bar_back = battle_canvas.create_rectangle(
    470, 45, 720, 65, fill="lightgray"
)
enemy_hp_bar = battle_canvas.create_rectangle(
    470, 45, 720, 65, fill="green"
)

message_label = tkinter.Label(root, text="", font=("Arial", 30, "bold"))
message_label.place_forget()

root.after(100, player_turn)
root.mainloop()
