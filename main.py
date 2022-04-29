import pygame
pygame.init()
import GTlib as gt
import tkinter.filedialog as tk
import shutil
import os

#---------------------- Credit --------------------
#WhiskyLeFou and GalTech
#----------------- Global constante ---------------

SCREEN = (900,600)
FPS = 60

#---------------------- Class ---------------------


#----------------- Main Window Class --------------

class main_window:
    def __init__(self):
        # PARAMETER
        pygame.display.set_caption(".exe creator")
        self.screen = pygame.display.set_mode(SCREEN) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()

        # NETWORK

        # GROUPS
        self.all_sprites = pygame.sprite.Group()

        # RUNNING
        self.is_running=True

        # OBJECTS
        self.background = gt.Image(0,0,"Image/black.png")
        self.title = gt.Text(330,40,58,58,".exe Creator",font=pygame.font.Font(None,58),hidden=True)
        self.text_file = gt.Text(7,120,58,58,"Select File:",hidden=True)
        self.text_dep = gt.Text(7,220,58,58,"Select Depository:",hidden=True)
        self.text_icon = gt.Text(7,320,58,58,"Select Icon:",hidden=True)
        self.text_option = gt.Text(650,120,58,58,"Options:",hidden=True)
        self.text_option1 = gt.Text(650,175,58,58,"One file ?",hidden=True)
        self.text_option2 = gt.Text(650,225,58,58,"No console ?",hidden=True)
        self.text_build_statut = gt.Text(550,503,58,58,"Waiting for build...", hidden=True)

        self.ckeckbox_option1 = gt.Checkbox(850,175,30)
        self.ckeckbox_option2 = gt.Checkbox(850,225,30)

        self.inputbox_file = gt.InputBox(10,150,250,30,default_text="Path")
        self.inputbox_dep = gt.InputBox(10,250,250,30,default_text="Path")
        self.inputbox_icon = gt.InputBox(10,350,250,30,default_text="Path")

        self.boutton_file = gt.Boutton(300,150,gt.Square(0,0,"white",110,30),gt.Text(15,0,100,30,"Select",hidden=True, color="black"),color_hover=(220, 220, 220))
        self.boutton_dep1 = gt.Boutton(300,245,gt.Square(0,0,"white",110,20),gt.Text(17,0,100,20,"Add files",hidden=True, color="black",font=pygame.font.Font(None, 22)),color_hover=(220, 220, 220))
        self.boutton_dep2 = gt.Boutton(300,270,gt.Square(0,0,"white",110,20),gt.Text(0,0,100,20,"Add directory",hidden=True, color="black",font=pygame.font.Font(None, 22)),color_hover=(220, 220, 220))
        self.boutton_icon = gt.Boutton(300,350,gt.Square(0,0,"white",110,30),gt.Text(15,0,100,30,"Select",hidden=True, color="black"),color_hover=(220, 220, 220))
        self.boutton_build = gt.Boutton(370,500,gt.Square(0,0,"red",150,40),gt.Text(35,3,100,30,"BUILD",hidden=True, color="white"),color_hover=(180, 0, 0))

        self.all_sprites.add(self.background)
        self.all_sprites.add(self.ckeckbox_option1.square)
        self.all_sprites.add(self.ckeckbox_option2.square)
        self.all_sprites.add(self.boutton_file.square)
        self.all_sprites.add(self.boutton_dep1.square)
        self.all_sprites.add(self.boutton_dep2.square)
        self.all_sprites.add(self.boutton_icon.square)
        self.all_sprites.add(self.boutton_build.square)
        
        self.file = ""
        self.dep = []
        self.ico = ""
    def run(self):
        '''WinLoop'''
        while self.is_running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        self.all_sprites.update()

    
    def events(self):
        all_events = pygame.event.get()

        self.ckeckbox_option1.event(all_events)
        self.ckeckbox_option2.event(all_events)

        self.inputbox_file.event(all_events)
        self.inputbox_dep.event(all_events)
        self.inputbox_icon.event(all_events)

        self.boutton_file.event(all_events)
        self.boutton_dep1.event(all_events)
        self.boutton_dep2.event(all_events)
        self.boutton_icon.event(all_events)
        self.boutton_build.event(all_events)

        if self.boutton_file.clicked:
            self.file = tk.askopenfilename(filetypes=[("python files", "*.py *.pyw")], title="Select main file")
        if self.boutton_dep1.clicked:
            file = tk.askopenfilename(title="Select dependente file")
            if not file=="":
                self.dep.append((False,file))
        if self.boutton_dep2.clicked:
            dir = tk.askdirectory(title="Select dependente folder")
            if not dir=="":
                self.dep.append((True,dir))
        if self.boutton_icon.clicked:
            self.ico = tk.askopenfilename(filetypes=[("Icon", "*.ico")], title="Select icon")
        
        if self.boutton_build.clicked:
            if not self.file=="":
                output_dir = tk.askdirectory(title="Save at")
                if not output_dir=="":
                    self.text_build_statut.color = "white"
                    self.text_build_statut.set_text("Building")
                    self.draw()
                    os.system(f"pyinstaller {self.file} {f'--icon={self.ico}' if not self.ico=='' else ''} --noconfirm --specpath {output_dir} --distpath {output_dir} {'--onefile' if self.ckeckbox_option1.is_check else ''} {'--noconsole' if self.ckeckbox_option2.is_check else ''}")
                    for dep in self.dep:
                        if dep[0]:
                            shutil.copytree(dep[1], f"{output_dir}/{dep[1].split('/')[-1]}")
                        else:
                            shutil.copy(dep[1], f"{output_dir}/{dep[1].split('/')[-1]}")
                    self.text_build_statut.color = "green"
                    self.text_build_statut.set_text("Builded")
                else:
                    self.text_build_statut.color = "white"
                    self.text_build_statut.set_text("Waiting for build...")
            else:
                self.text_build_statut.color = "red"
                self.text_build_statut.set_text("No file selected")

        for event in all_events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def draw(self):
        self.all_sprites.draw(self.screen) # actualise les sprites

        self.title.draw(self.screen)
        self.text_file.draw(self.screen)
        self.text_dep.draw(self.screen)
        self.text_icon.draw(self.screen)
        self.text_option.draw(self.screen)
        self.text_option1.draw(self.screen)
        self.text_option2.draw(self.screen)
        self.text_build_statut.draw(self.screen)

        self.ckeckbox_option1.draw(self.screen)
        self.ckeckbox_option2.draw(self.screen)

        self.inputbox_file.draw(self.screen)
        self.inputbox_dep.draw(self.screen)
        self.inputbox_icon.draw(self.screen)

        self.boutton_file.draw(self.screen)
        self.boutton_dep1.draw(self.screen)
        self.boutton_dep2.draw(self.screen)
        self.boutton_icon.draw(self.screen)
        self.boutton_build.draw(self.screen)    

        pygame.display.flip()


test_mode=True
if __name__ == '__main__':
    if test_mode:
        root=main_window()
        root.run()
    else:
        try:
            root=main_window()
            root.run()
        except:
            None