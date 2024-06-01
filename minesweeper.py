from tkinter.messagebox import showerror
from tkinter import Tk, Entry, Label
from random import randint

column, row = 30, 16  # 列数, 行数
bad_grid = 20  # 雷数

# noinspection PyUnusedLocal
def setting(event) -> None:
    # noinspection PyUnusedLocal
    # noinspection PyShadowingNames
    def output_(event):
        g1 = e1.get()
        g2 = e2.get()
        g3 = e3.get()
        if g1 != '' and g2 != '' and g3 != '':
            global column, row, bad_grid
            column = eval(g1)
            row = eval(g2)
            bad_grid = eval(g3)
            ready_game()
    window = Tk()
    window.title('控制器')
    Label(window, text='列数').grid(column=1, row=1)
    e1 = Entry(window, width=10)
    e1.grid(column=1, row=2)
    Label(window, text='行数').grid(column=2, row=1)
    e2 = Entry(window, width=10)
    e2.grid(column=2, row=2)
    Label(window, text='雷数').grid(column=3, row=1)
    e3 = Entry(window, width=10)
    e3.grid(column=3, row=2)
    window.bind_all('<KeyPress-Return>', output_)
    window.mainloop()
# noinspection PyUnusedLocal
def ready_game(*event) -> None:
    root.unbind_all('<KeyPress-Return>')
    global game, flag, bad_grids
    for i in grids:
        grids[i]['lab'].destroy()
    grids.clear()
    show_grids.clear()
    flag, game, bad_grids = 0, True, get_bad_grid()
    root.bind_all('<KeyPress-Return>', setting)
    start_game(_column=column, _row=row, _bad_grid=bad_grid)
def start_game(_column: int, _row: int, _bad_grid: int) -> None:
    """   窗口类   """
    root.title(f'{_column}×{_row}     /{_bad_grid}          Loading...')
    root.resizable(height=False, width=False)  # 固定窗口宽度

    """   标签   """
    row_, column_ = 1, 1
    # 创建格
    lab = ''
    for i in range(_row * _column):
        lab = Label(root, width=2, font=('宋体', 12), bg=colors(text='方格背景色'))
        lab.grid(row=row_, column=column_)

        lab.bind('<ButtonRelease-1>', lambda event, arg=(row_, column_): show_grid(site=arg))  # 左键单击
        lab.bind('<ButtonRelease-3>', lambda event, arg=(row_, column_): show_grid_flag(site=arg))  # 右键单击

        if (row_, column_) in bad_grids:
            bad_grid_ = True
        else:
            bad_grid_ = False
        grids[(row_, column_)] = {'lab': lab, 'text': 0, 'bad_grid': bad_grid_, 'flag': False}

        if row_ == _row:
            row_ = 1
            column_ += 1
        else:
            row_ += 1
    # 为格赋值
    for i in bad_grids:
        for p in [-1, 0, 1]:
            for q in [-1, 0, 1]:
                try:
                    grids[(i[0] + p, i[1] + q)]['text'] += 1
                except KeyError:
                    pass

    """   事件绑定   """
    # noinspection PyUnusedLocal
    def press_shift(event):
        global shift
        if not shift:
            shift = True
            for __i in grids:
                grids[__i]['lab'].configure(relief='raised')
    root.bind_all('<KeyPress-Shift_L>', press_shift)  # Shift按下
    # noinspection PyUnusedLocal
    def release_shift(event):
        global shift
        if shift:
            shift = False
            for __i in grids:
                grids[__i]['lab'].configure(relief='flat')
    root.bind_all('<KeyRelease-Shift_L>', release_shift)  # Shift松开

    """   窗口大小设定   """
    root.update()
    root.geometry(f'{lab.winfo_height() * _column}x{lab.winfo_width() * row}')
    root.title(f'{_column}×{row}    0/{_bad_grid}')

    # 循环
    root.mainloop()
def get_bad_grid() -> list:
    if row < 1:
        showerror(title='Error:', message='  行数不得小于1' + ' ' * 25)
    elif column < 1:
        showerror(title='Error:', message='  列数不得小于1' + ' ' * 25)
    elif row * column < bad_grid:
        showerror(title='Error:', message='  雷数超出限制' + ' ' * 25)
    else:
        bad_grid_list = []
        while len(bad_grid_list) < bad_grid:
            r = randint(1, row)
            c = randint(1, column)
            if (r, c) not in bad_grid_list:
                bad_grid_list.append((r, c))
        return bad_grid_list
def colors(text: str | int) -> str:
    match text:
        case '方格背景色':
            return 'LightSkyBlue'
        case '?':
            return 'White'
        case 1:
            return 'DarkViolet'
        case 2:
            return 'ForestGreen'
        case 3:
            return 'DarkSlateBlue'
        case 4:
            return 'Navy'
        case 5:
            return 'Red'
        case 6:
            return 'MediumSpringGreen'
        case 7:
            return 'LightPink'
        case _:
            return 'DarkMagenta'
def show_grid(site: tuple) -> None:
    if game and site not in show_grids and not grids[site]['flag']:
        show_grids.append(site)
        item = grids[site]
        if item['bad_grid']:  # 踩雷
            game_over(is_=False, lab_=item['lab'])
        else:
            null = []
            if item['text'] == 0:
                text = ''
                null.append(site)
            else:
                text = item['text']
            item['lab'].configure(text=str(text), fg=colors(text), bg='White')

            # 关联空白格
            while null:
                r, c = null.pop(0)
                for p in [-1, 0, 1]:
                    for q in [-1, 0, 1]:
                        site = (r + p, c + q)
                        try:
                            if site not in show_grids:  # 避免重复计算
                                if grids[site]['text'] == 0:  # 空格
                                    if site not in show_grids:
                                        null.append(site)
                                        grids[site]['lab'].configure(text='', bg='White')
                                        show_grids.append(site)
                                else:
                                    grids[site]['lab'].configure(text=grids[site]['text'], fg=colors(grids[site]['text']), bg='White')
                                    if site not in show_grids:
                                        show_grids.append(site)
                                if grids[site]['flag']:
                                    global flag
                                    flag -= 1
                                    root.title(f'{column}×{row}    {flag}/{bad_grid}')
                        except KeyError:
                            pass

            if row * column - len(show_grids) == bad_grid:
                game_over(is_=True)
def show_grid_flag(site: tuple) -> None:
    if game and site not in show_grids:
        global flag
        if grids[site]['flag']:
            grids[site]['flag'] = False
            grids[site]['lab'].configure(text='')
            flag -= 1
        else:
            grids[site]['flag'] = True
            grids[site]['lab'].configure(text='?', fg=colors(text='?'))
            flag += 1
        root.title(f'{column}×{row}    {flag}/{bad_grid}')
def game_over(is_: bool, lab_: Label = None) -> None:
    global bad_grids, game, flag
    if is_:
        for i in bad_grids:
            grids[i]['lab'].configure(text='x', fg='LimeGreen', bg='Wheat')
        root.title('恭喜！')
    else:
        flag_ = 0
        for i in bad_grids:
            item = grids[i]
            if item['flag']:
                item['lab'].configure(text='x', fg='LimeGreen', bg='Wheat')
                flag_ += 1
            else:
                if item['lab'] != lab_:
                    item['lab'].configure(text='x', fg='Gold')
                else:
                    item['lab'].configure(text='x', fg='red')
        root.title(f'Game Over ！  —排除  {flag_} (总{bad_grid})个雷')

    game = False
    root.bind_all('<KeyPress-Return>', ready_game)


game, shift, flag = True, False, 0
grids, bad_grids, show_grids = {}, get_bad_grid(), []
root = Tk()
if __name__ == '__main__':
    root.bind_all('<KeyPress-Return>', setting)
    start_game(_column=column, _row=row, _bad_grid=bad_grid)
