import socket
import paramiko
import base64
import os
import sys
import random

from multiprocessing import Process

from kivy.lang import Builder
from kivymd.app import *
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from kivymd.uix.floatlayout import *
from kivymd.uix.boxlayout import *
from kivymd.uix.card import *

from kivymd.uix.snackbar import Snackbar

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.taptargetview import *

from kivymd.uix.behaviors import *


debug = True

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def debug_msg(msg):
    if debug == True:
        print("Debug: ", msg)
    else:
        pass


def execute_query(cmd, host, usrname, password):
    Process(target=ssh.connect(hostname=host,
                               username=usrname, password=password))
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.close()
    stderr.close()
    for line in stdout.readlines():
        output = line.replace('\n', '')
        debug_msg('query_extract: '+output)
        return(output)


layout = ("""
#:import Snackbar kivymd.uix.snackbar.Snackbar

Screen:    
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Gerenciador de usuarios'
            left_action_items: [["tune", lambda x: x]]
            right_action_items: [["close", lambda x: app.stopping_app()]]
            elevation: 10
        MDFloatLayout:
            orientation: 'vertical'
            TelaLogin:   
                   


<TelaLogin>:
    MDIconButton:
        on_release: root.credits_button()
        pos_hint: {'center_x':.5,'center_y':.8}
        icon: 'google-downasaur'
        user_font_size: '74sp'
    MDTextField:
        id: HostAddrField        
        hint_text: 'Endereço:'
        icon_right: 'web'
        size_hint_x: .5
        pos_hint: {'center_x':.5,'center_y':.6}
    MDTextField:
        id: UserLoginField        
        hint_text: 'Usuario:'
        icon_right: 'account-circle'
        size_hint_x: .5
        pos_hint: {'center_x':.5,'center_y':.5}
    MDTextField:
        id: PassLoginField
        hint_text: 'Senha:'
        icon_right: 'key-variant'
        password: True
        size_hint_x: .5
        pos_hint: {'center_x':.5,'center_y':.4}
    ButtonFocus:
        text: 'Login'
        on_release: root.abrir_tela_painel(HostAddrField.text,UserLoginField.text,PassLoginField.text)
        focus_color: app.theme_cls.accent_color
        unfocus_color: app.theme_cls.primary_color
        size_hint_x: .5
        pos_hint: {'center_x':.5,'center_y':.3}
    MDLabel:
        text: '2021-v1.0 @raioramalho - ramalho.sit@gmail.com'
        size_hint_x: .5
        pos_hint: {'center_x':.5,'center_y':.1}


<TelaPainel>
    id: card
    orientation: 'vertical'
    size_hint: 1, 1
    pos_hint: {'center_x':.5,'center_y':.5}
    MDBoxLayout:
        size_hint_y: .1
        padding: [25, 0, 25, 0]
        md_bg_color: app.theme_cls.primary_color
        MDLabel:
            text: 'Painel de gerenciamento'        
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
        MDIconButton:
            icon: 'close'
            on_release: root.fechar_tela_painel()
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
    MDFloatLayout:
        orientation: 'vertical'
        MDTextField:
            id: UserSearchField
            hint_text: 'Procurar usuario:'
            size_hint_x: .3
            pos_hint: {'center_x':.2, 'center_y':.9}    
        MDRaisedButton:            
            text: "Verificar"
            size_hint_x: .3
            pos_hint: {"center_x": .2, "center_y": .8}
            on_release: root.verify_user(UserSearchField.text)
        MDRaisedButton:
            disabled: True
            id: ModifyUserButton            
            text: "Modificar"
            size_hint_x: .3
            pos_hint: {"center_x": .2, "center_y": .7}
            on_release: root.modify_user(UserSearchField.text,GetFullNmField.text,GetGroupNmField.text)
        MDRaisedButton:    
            id: AddUserButton        
            text: "Adcionar"
            size_hint_x: .3
            pos_hint: {"center_x": .2, "center_y": .6}
            on_release: root.create_user(UserSearchField.text)
        MDRaisedButton:
            disabled: True
            id: RemoveUserButton            
            text: "Excluir"
            size_hint_x: .3
            pos_hint: {"center_x": .2, "center_y": .5}
            on_release: root.remove_user(UserSearchField.text)
        MDRaisedButton:
            disabled: True            
            id: ChangPassButton
            text: "Mudar Senha"
            size_hint_x: .3
            pos_hint: {"center_x": .2, "center_y": .4}
            on_release: root.show_confirmation_dialog()
        MDTextField:
            disabled: True
            id: GetUserNmField
            hint_text: 'GetUserNmField:'
            size_hint_x: .3
            pos_hint: {'center_x':.7, 'center_y':.9}
        MDCheckbox:
            on_active: root.on_checkbox_active(*args,'GetUserNmField')
            size_hint: None, None
            size: "38dp", "38dp" 
            pos_hint: {'center_x':.5, 'center_y':.9}
        MDTextField:
            disabled: True
            id: GetFullNmField
            hint_text: 'GetFullNmField:'
            size_hint_x: .3
            pos_hint: {'center_x':.7, 'center_y':.8}
        MDCheckbox:
            on_active: root.on_checkbox_active(*args,'GetFullNmField')
            size_hint: None, None
            size: "38dp", "38dp" 
            pos_hint: {'center_x':.5, 'center_y':.8}
        MDTextField:
            disabled: True
            id: GetGroupNmField
            hint_text: 'GetGroupNmField:'
            size_hint_x: .3
            pos_hint: {'center_x':.7, 'center_y':.7}
        MDCheckbox:
            on_active: root.on_checkbox_active(*args,'GetGroupNmField')
            size_hint: None, None
            size: "38dp", "38dp" 
            pos_hint: {'center_x':.5, 'center_y':.7}
        MDTextField:
            disabled: True
            id: GetHomDirNmField
            hint_text: 'GetHomDirNmField:'
            size_hint_x: .3
            pos_hint: {'center_x':.7, 'center_y':.6}
        MDCheckbox:
            on_active: root.on_checkbox_active(*args,'GetHomDirNmField')
            size_hint: None, None
            size: "38dp", "38dp" 
            pos_hint: {'center_x':.5, 'center_y':.6}
        MDTextField:
            disabled: True
            id: GetDomainNmField
            hint_text: 'GetDomainNmField:'
            size_hint_x: .3
            pos_hint: {'center_x':.7, 'center_y':.5}
        MDCheckbox:
            on_active: root.on_checkbox_active(*args,'GetDomainNmField')
            size_hint: None, None
            size: "38dp", "38dp" 
            pos_hint: {'center_x':.5, 'center_y':.5}
        
<DialogContent>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: NewPass
        password: True
        hint_text: "Nova Senha:"

    MDTextField:
        id: NewPassConfirmation
        password: True
        hint_text: "Nova Senha:"                                  

<SenhaCard>:
    orientation: 'vertical'
    size_hint: None, None
    size: "290dp", "220dp"
    pos_hint: {"center_x": .5, "center_y": .5}
    MDBoxLayout:
        size_hint_y: .2
        padding: [25, 0, 25, 0]
        md_bg_color: app.theme_cls.primary_color
        MDLabel:
            text: 'Mudar Senha'            
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
        MDIconButton:
            icon: 'close'
            on_release: root.fechar_senha_card()
            theme_text_color: 'Custom'
            text_color: 1,1,1,1
    MDFloatLayout:
        MDTextField:
            hint_text: 'Nome do usuario:'
            size_hint_x: .5
            pos_hint: {'center_x':.5, 'center_y':.8}
        MDTextField:
            hint_text: 'Nova senha:'
            size_hint_x: .5
            pos_hint: {'center_x':.5, 'center_y':.6}
        MDTextField:
            hint_text: 'Nova senha:'
            size_hint_x: .5
            pos_hint: {'center_x':.5, 'center_y':.4}
        MDRaisedButton:
            text: 'Redefinir senha'                        
            pos_hint: {'center_x':.5, 'center_y':.2}               
                   
""")


class ButtonFocus(MDRaisedButton, FocusBehavior):
    pass


class DialogContent(BoxLayout):
    pass


class Screen(MDScreen):
    pass


class SenhaCard(MDCard):
    def modify_password(self, get_user, new_pass, confirmation):
        pass

    def fechar_senha_card(self):
        debug_msg('fechar_senha_card')
        self.parent.remove_widget(self)


class TelaLogin(MDFloatLayout):
    def credits_button(self):
        debug_msg('credits_func')
        os.system('start https://gitlab.com/raioramalho')

    def abrir_tela_painel(self, host, usrname, password):
        global validhost
        validhost = host
        global validuser
        validuser = usrname
        global validpass
        validpass = password
        bpassword = base64.b64encode(password.encode('ascii'))
        debug_msg('try_connect_with:'+usrname+':'+bpassword.decode('ascii'))
        try:
            output = execute_query('whoami', host, usrname, password)
            if output == usrname:
                debug_msg('logged:'+usrname)
                debug_msg('abrir_tela_painel')
                self.add_widget(TelaPainel())
                Snackbar(text="Bem-vindo: "+usrname).show()
                pass
            else:
                debug_msg('error0')
                Snackbar(text="error0").show()

        except paramiko.AuthenticationException:
            debug_msg('auth_error')
            Snackbar(text="Usuário ou senha incorretos!").show()
            pass
        except socket.error:
            debug_msg('connection_error')
            Snackbar(text="Erro de conexão com o servidor!").show()
            pass


class TelaPainel(MDCard):
    def test_func(self):
        debug_msg('test_func')
        Snackbar(text="test_func").show()

    def on_checkbox_active(self, checkbox, value, chkids):
        if value:
            print('The checkbox', chkids, 'is active',
                  'and', checkbox.state, 'state')
            self.ids[chkids].disabled = False
        else:
            print('The checkbox', chkids, 'is inactive',
                  'and', checkbox.state, 'state')
            self.ids[chkids].disabled = True

    def abrir_senha_card(self):
        debug_msg('abrir_senha_card')
        self.add_widget(SenhaCard())

    def fechar_tela_painel(self):
        debug_msg('fechar_tela_painel')
        self.parent.remove_widget(self)

    def verify_user(self, get_user):
        debug_msg('verify_user:'+get_user)
        execute_query("> smb.info", validhost, validuser, validpass)
        execute_query("rm smb.info&&pdbedit -u "+get_user +
                      " -L -v > smb.info", validhost, validuser, validpass)
        GetUsrName = execute_query(
            "cat smb.info | grep ^Unix | awk -F: '{printf $2}' | sed 's/^ *//g'", validhost, validuser, validpass)
        self.ids.GetUserNmField.text = str(GetUsrName)
        GetFullName = execute_query(
            "cat smb.info | grep ^Full | awk -F: '{printf $2}' | sed 's/^ *//g'", validhost, validuser, validpass)
        self.ids.GetFullNmField.text = str(GetFullName)
        GetGrpName = execute_query(
            "groups "+get_user+" | awk -F: '{print $2}' | sed 's/^ *//g' | sed 's/ /,/g'", validhost, validuser, validpass)
        self.ids.GetGroupNmField.text = str(GetGrpName)
        GetHomeDir = execute_query(
            "cat smb.info | grep ^Home | head -n1 | awk -F: '{print $2}' | sed 's/^ *//g'", validhost, validuser, validpass)
        self.ids.GetHomDirNmField.text = str(GetHomeDir)
        GetDomain = execute_query(
            "cat smb.info | grep ^Domain | head -n1 | awk -F: '{print $2}' | sed 's/^ *//g'", validhost, validuser, validpass)
        self.ids.GetDomainNmField.text = str(GetDomain)
        if GetUsrName == get_user:
            Snackbar(text="Usuario '"+get_user+"' encontrado!").show()
            self.ids.ModifyUserButton.disabled = False
            self.ids.AddUserButton.disabled = True
            self.ids.RemoveUserButton.disabled = False
            self.ids.ChangPassButton.disabled = False
            global validget_user
            validget_user = str(get_user)
        else:
            Snackbar(text="Usuario '"+get_user+"' não encontrado!").show()
            self.ids.ModifyUserButton.disabled = True
            self.ids.AddUserButton.disabled = False
            self.ids.RemoveUserButton.disabled = True
            self.ids.ChangPassButton.disabled = True

    def modify_user(self, get_user, get_full_name, get_grp):
        execute_query("""pdbedit -u """+get_user+""" -r --fullname='""" +
                      get_full_name+"""'""", validhost, validuser, validpass)
        execute_query(
            f"usermod -G {str(get_grp)} {get_user}", validhost, validuser, validpass)
        Snackbar(text="Modificação executada, favor verificar para confirmar!").show()

    def remove_user(self, get_user):
        execute_query("""smbpasswd -x """+get_user +
                      """ """, validhost, validuser, validpass)
        debug_msg('remove_from_samba')
        execute_query("""userdell """+get_user+""" """,
                      validhost, validuser, validpass)
        debug_msg('remove_from_users')              
        execute_query("""groupdell """+get_user+""" """,
                      validhost, validuser, validpass)
        debug_msg('remove_from_groups')              
        Snackbar(text="Usuario '"+get_user+"' removido com Sucesso!").show()

    def create_user(sef, get_user):
        debug_msg("create_user")
        out = execute_query("""( echo '1q2w3e'; echo '1q2w3e' ) | adduser -a """ +
                            get_user+"""""", validhost, validuser, validpass)
        execute_query("""( echo '1q2w3e'; echo '1q2w3e' ) | smbpasswd -a """ +
                      get_user+"""""", validhost, validuser, validpass)
        if out == "Adding user `"+get_user+"' ...":
            Snackbar(text="Usuario: '"+get_user+"' criado com Sucesso!").show()
        else:
            Snackbar(text="Erro ao criar usuario: '"+get_user+"'").show()

    dialog = None

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Digite uma nova senha para: '"+validget_user+"'",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDRaisedButton(
                        text="CANCELAR", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDRaisedButton(
                        text="CONFIRMAR", text_color=self.theme_cls.accent_color, on_release=self.grabText
                    ),
                ],
            )
        debug_msg('open_dialog')
        self.dialog.set_normal_height()
        self.dialog.open()

    def grabText(self, inst):
        NewPass = self.dialog.content_cls.ids.NewPass.text
        NewPassConfirmation = self.dialog.content_cls.ids.NewPassConfirmation.text
        if NewPass == NewPassConfirmation:
            execute_query('(echo "'+NewPass+'"; echo "'+NewPassConfirmation +
                          '") | smbpasswd -s -a '+validget_user+'', validhost, validuser, validpass)
            Snackbar(text="Senha Alterada com Sucesso!").show()
        else:
            Snackbar(text="A senha inserida não é compativel!").show()
            debug_msg('error390')
        debug_msg('close_dialog')
        self.dialog.dismiss()

    def closeDialog(self, inst):
        debug_msg('close_dialog')
        self.dialog.dismiss()


class SmbManager(MDApp):
    def stopping_app(self):
        debug_msg('stopping_app')
        sys.exit(0)

    def build(self):
        self.title = 'SMB Manager'
        self.icon = 'icon.png'
        colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal',
                  'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

        self.theme_cls.primary_palette = f'{str(random.choice(colors))}'
        self.theme_cls.primary_hue = '700'
        self.theme_cls.accent_palette = f'{str(random.choice(colors))}'
        #self.theme_cls.theme_style = 'Dark'
        Window.size = (750, 600)
        debug_msg("stating_app")
        return Builder.load_string(layout)


SmbManager().run()
