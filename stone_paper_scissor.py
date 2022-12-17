#Stone Paper Scissor

import random
import tkinter as tk
import pygame

class StonePaperScissor:
    def __init__(self):
        self.GAME_FOLDER = 'D:/batches/Python_1/stone_paper_scissor/'
        #Create a window and set primary attributes
        self.window = tk.Tk()
        self.window.title('Stone Paper Scissor')
        self.window.geometry('400x500') #'wxh'
        self.window.resizable(False,False)
        self.window.iconbitmap(self.GAME_FOLDER + 'game_icon.ico')

        #image list
        self.images = [
            None,
            tk.PhotoImage(file= self.GAME_FOLDER + 'stone.png'),
            tk.PhotoImage(file=self.GAME_FOLDER + 'paper.png'),
            tk.PhotoImage(file=self.GAME_FOLDER + 'scissor.png'),
        ]

        #Frames for players and play area
        frame_computer = tk.Frame(master=self.window, bg='#FFAEC9', height=100)
        frame_play_area = tk.Frame(master=self.window, bg='#FFF200', height=300)
        frame_player = tk.Frame(master=self.window, bg='#99D9EA', height=100)

        #widgets for super computer
        lbl_sc_title = tk.Label(master=frame_computer, text = 'Super Computer : ', bg = frame_computer['bg'])
        self.lbl_sc_score = tk.Label(master=frame_computer, text='0', bg=frame_computer['bg'])
        lbl_sc_stone = tk.Label(master=frame_computer, image= self.images[1], bg= frame_computer['bg'] )
        lbl_sc_paper = tk.Label(master=frame_computer, image=self.images[2], bg=frame_computer['bg'])
        lbl_sc_scissor = tk.Label(master=frame_computer, image=self.images[3], bg=frame_computer['bg'])

        #widgets for master player
        lbl_mp_title = tk.Label(master=frame_player, text='Master Player : ', bg=frame_player['bg'])
        self.lbl_mp_score = tk.Label(master=frame_player, text='0', bg=frame_player['bg'])
        self.bttn_mp_stone = tk.Button(master=frame_player, image=self.images[1], bg=frame_player['bg'], command=self.play_stone)
        self.bttn_mp_paper = tk.Button(master=frame_player, image=self.images[2], bg=frame_player['bg'], command=self.play_paper)
        self.bttn_mp_scissor = tk.Button(master=frame_player, image=self.images[3], bg=frame_player['bg'], command=self.play_scissor)

        #widgets for play_area
        self.canvas = tk.Canvas(master=frame_play_area, bg = frame_play_area['bg'])
        self.computers_stroke_index = 0
        self.computers_stroke_coords = [200,30]
        self.players_stroke_index = 0
        self.players_stroke_coords = [200,250]

        self.computers_stroke = self.canvas.create_image(self.computers_stroke_coords, image = self.images[self.computers_stroke_index])
        self.players_stroke = self.canvas.create_image(self.players_stroke_coords, image=self.images[self.players_stroke_index])

        #Add the frames to the window
        frame_computer.pack(expand=True, fill=tk.X, padx=0 )
        frame_play_area.pack(expand=True, fill=tk.X, padx=0, ipady=18)
        frame_player.pack(expand=True, fill=tk.X, padx=0)

        #Add the widgets to the containers (frame/window)
        lbl_sc_title.grid(row= 0, column =0)
        self.lbl_sc_score.grid(row=0, column= 1)
        lbl_sc_stone.grid(row=1, column=0, padx=25)
        lbl_sc_paper.grid(row=1, column=1, padx=25)
        lbl_sc_scissor.grid(row=1, column=2, padx=25)

        self.bttn_mp_stone.grid(row=0, column=0, padx=25)
        self.bttn_mp_paper.grid(row=0, column=1, padx=25)
        self.bttn_mp_scissor.grid(row=0, column=2, padx=25)

        lbl_mp_title.grid(row= 1, column =0)
        self.lbl_mp_score.grid(row=1, column= 1)

        self.canvas.pack(expand=True, fill=tk.BOTH)

        pygame.init()
        self.computer_wins = pygame.mixer.Sound(self.GAME_FOLDER + 'super_computer_wins.mp3')
        self.player_wins = pygame.mixer.Sound(self.GAME_FOLDER + 'master_player_wins.mp3')
        self.round_tied = pygame.mixer.Sound(self.GAME_FOLDER + 'round_tied.mp3')

        #window mainloop keeps the window alive and listening-responding to events.
        self.window.mainloop()

    def __del__(self):
        pygame.quit()

    def computer_plays(self):
        self.computers_stroke_index = random.choice([1,2,3])

    def play_stone(self):
        self.players_stroke_index = 1
        self.play()

    def play_paper(self):
        self.players_stroke_index = 2
        self.play()

    def play_scissor(self):
        self.players_stroke_index = 3
        self.play()

    def play(self):
        self.disable_play()
        self.computer_plays()
        self.canvas.itemconfig(self.players_stroke, image = self.images[self.players_stroke_index])
        self.canvas.itemconfig(self.computers_stroke, image=self.images[self.computers_stroke_index])
        self.window.after(0, self.clash)

    def clash(self):
        #change the coords of the strokes
        self.computers_stroke_coords[1] +=10
        self.players_stroke_coords[1] -= 10
        #redraw
        self.canvas.coords(self.computers_stroke, self.computers_stroke_coords)
        self.canvas.coords(self.players_stroke, self.players_stroke_coords)

        if self.players_stroke_coords[1] - self.computers_stroke_coords[1] > 72:
            self.window.after(200, self.clash)
        else:
            self.round_result()
            self.computers_stroke_coords[1] = 20
            self.players_stroke_coords[1] = 250

    def round_result(self):
        if self.players_stroke_index == 1: # stone
            if self.computers_stroke_index == 1: #stone
                #tie
                self.round_tied.play()
                self.window.after(1000, self.enable_play)
            elif self.computers_stroke_index == 2: #paper
                #computer wins the round
                self.computer_wins.play()
                self.increase_computers_score()
                self.window.after(2000, self.enable_play)
            elif self.computers_stroke_index == 3: #scissor
                #player wins the round
                self.player_wins.play()
                self.increase_players_score()
                self.window.after(2000, self.enable_play)

        elif self.players_stroke_index ==2: #paper
            if self.computers_stroke_index == 1:  # stone
                # player wins the round
                self.player_wins.play()
                self.increase_players_score()
                self.window.after(2000, self.enable_play)
            elif self.computers_stroke_index == 2:  # paper
                # round tied
                self.round_tied.play()
                self.window.after(1000, self.enable_play)
            elif self.computers_stroke_index == 3:  # scissor
                # computer wins the round
                self.computer_wins.play()
                self.increase_computers_score()
                self.window.after(2000, self.enable_play)


        elif self.players_stroke_index == 3: #scissor
            if self.computers_stroke_index == 1:  # stone
                # computer wins the round
                self.computer_wins.play()
                self.increase_computers_score()
                self.window.after(2000, self.enable_play)
            elif self.computers_stroke_index == 2:  # paper
                # player wins the round
                self.player_wins.play()
                self.increase_players_score()
                self.window.after(2000, self.enable_play)
            elif self.computers_stroke_index == 3:  # scissor
                # round tied
                self.round_tied.play()
                self.window.after(1000, self.enable_play)

    def increase_computers_score(self):
        self.lbl_sc_score['text'] = str(int(self.lbl_sc_score['text']) +1)

    def increase_players_score(self):
        self.lbl_mp_score['text'] = str(int(self.lbl_mp_score['text']) +1)

    def enable_play(self):
        self.bttn_mp_stone['state'] = 'normal'
        self.bttn_mp_paper['state'] = 'normal'
        self.bttn_mp_scissor['state'] = 'normal'

    def disable_play(self):
        self.bttn_mp_stone['state'] = 'disabled'
        self.bttn_mp_paper['state'] = 'disabled'
        self.bttn_mp_scissor['state'] = 'disabled'
def main():
    sps = StonePaperScissor()

main()