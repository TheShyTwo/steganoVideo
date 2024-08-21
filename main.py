import sys
from PyQt5.QtWidgets import *
from library import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.padding = 'long-'
        self.key_en = None
        self.key_de = None
        self.length_block_aes = 128
        self.length_key = 16
        self.input_video_path_en = ''
        self.input_text_path = ''
        self.input_video_path_de = ''
        self.text_en = ''
        self.output_video_path_en = ''
        self.max_length = 0
        self.input_video_path_pl = ''
        self.encrypted_pad_data = ''
        self.encoded_pad_data = ''
        self.data_embed_pad_de = ''
        self.decoded_hamm_data_pad_de = ''
        self.org_data = ''
        self.type_video_en = ''

        self.setWindowTitle('видео-стеганографическая программа')
        self.setGeometry(100,100,800,800)
        #create menu
        self.menu=self.menuBar().addMenu('Меню')
        self.ac_encode=QAction('Встраивание')
        self.ac_encode.triggered.connect(self.switch_page_encode)
        self.menu.addAction(self.ac_encode)   
        self.ac_decode=QAction('Извлечение')
        self.ac_decode.triggered.connect(self.switch_page_decode)
        self.menu.addAction(self.ac_decode)
        self.ac_play_video=QAction('Проиграть видео')
        self.menu.addAction(self.ac_play_video)
        self.ac_play_video.triggered.connect(self.switch_page_play)
        #create stack page
        self.stk_page=QStackedWidget()
        self.setCentralWidget(self.stk_page)
        self.create_page_encode()
        self.create_page_decode()
        self.create_page_play()

    def create_page_encode(self):
        self.page_encode=QWidget()
        self.stk_page.addWidget(self.page_encode)

        self.grid_en=QGridLayout()
        self.page_encode.setLayout(self.grid_en)

        self.le_path_video_en=QLineEdit()
        self.le_path_video_en.setReadOnly(True)
        self.btn_select_video_en=QPushButton('Выбрать видео')
        self.btn_select_video_en.clicked.connect(self.select_video_en)
        self.te_text_input_en=QTextEdit()
        self.te_text_input_en.setReadOnly(True)
        self.btn_import_text_en=QPushButton('Выбрать текстовой файл')
        self.btn_import_text_en.clicked.connect(self.import_text_en)
        self.btn_embed=QPushButton('Встраивать')
        self.btn_embed.clicked.connect(self.embed_en)
        self.btn_clear_en=QPushButton('Очистить')
        self.btn_clear_en.clicked.connect(self.clear_en)
        self.lb_max_lenth_en=QLabel('Мак-размер: 0 kb')
        self.te_key_en = QTextEdit()
        self.te_key_en.setReadOnly(True)
        self.btn_create_key = QPushButton('Создать ключ')
        self.btn_create_key.clicked.connect(self.create_key)
        self.btn_save_key = QPushButton('Сохранить ключ')
        self.btn_save_key.clicked.connect(self.save_key_en)
        self.te_aes_en = QTextEdit()
        self.te_aes_en.setReadOnly(True)
        self.btn_encrypt_en = QPushButton('Шифровать')
        self.btn_encrypt_en.clicked.connect(self.encrypt_en)
        self.te_hamming_en = QTextEdit()
        self.te_hamming_en.setReadOnly(True)
        self.btn_encode_hamm_en = QPushButton('Кодировать Хэмминг')
        self.btn_encode_hamm_en.clicked.connect(self.encode_hamm_en)
        self.cb_key_length = QComboBox()
        self.cb_key_length.addItem('128 битов')
        self.cb_key_length.addItem('192 битов')
        self.cb_key_length.addItem('256 битов')
        self.cb_key_length.activated[str].connect(self.choose_key_length)

        self.grid_en.addWidget(QLabel('ВСТРАИВАНИЕ'),0,2)
        self.grid_en.addWidget(QLabel('Путь Видео:'),1,0)
        self.grid_en.addWidget(self.le_path_video_en,1,1,1,3)
        self.grid_en.addWidget(self.btn_select_video_en,1,4)
        self.grid_en.addWidget(self.cb_key_length,2,4)
        self.grid_en.addWidget(self.te_key_en,2,1,3,3)
        self.grid_en.addWidget(QLabel('Ключ AES:'),3,0)
        self.grid_en.addWidget(self.btn_create_key,3,4)
        self.grid_en.addWidget(QLabel('Текст:'),5,0)
        self.grid_en.addWidget(self.te_text_input_en,5,1,1,3)
        self.grid_en.addWidget(self.btn_import_text_en,5,4)
        self.grid_en.addWidget(QLabel('Шифрование AES:'),6,0)
        self.grid_en.addWidget(self.btn_encrypt_en,6,4)
        self.grid_en.addWidget(self.te_aes_en,6,1,1,3)
        self.grid_en.addWidget(QLabel('Кодирование Хэмминга:'),7,0)
        self.grid_en.addWidget(self.te_hamming_en,7,1,1,3)
        self.grid_en.addWidget(self.btn_encode_hamm_en,7,4)
        self.grid_en.addWidget(self.btn_embed,8,1)
        self.grid_en.addWidget(self.btn_clear_en,8,3)
        self.grid_en.addWidget(self.lb_max_lenth_en,8,4)
        self.grid_en.addWidget(self.btn_save_key,4,4)

    def create_page_decode(self):
        self.page_decode=QWidget()
        self.stk_page.addWidget(self.page_decode)

        self.grid_de=QGridLayout()
        self.page_decode.setLayout(self.grid_de)

        self.le_path_video_de=QLineEdit()
        self.le_path_video_de.setReadOnly(True)
        self.btn_select_video_de=QPushButton('Выбрать видео')
        self.btn_select_video_de.clicked.connect(self.select_video_de)
        self.te_text_de=QTextEdit()
        self.te_text_de.setReadOnly(True)
        self.btn_save_text=QPushButton('Сохранить текст')
        self.btn_save_text.clicked.connect(self.save_text_de)
        self.btn_decrypt=QPushButton('Дешифровать')
        self.btn_decrypt.clicked.connect(self.decrypt_de)
        self.btn_clear_de=QPushButton('Очистить')
        self.btn_clear_de.clicked.connect(self.clear_de)
        self.te_aes_de = QTextEdit()
        self.te_aes_de.setReadOnly(True)
        self.btn_import_key_de = QPushButton('Выбрать ключ')
        self.btn_import_key_de.clicked.connect(self.import_key)
        self.te_extract_data = QTextEdit()
        self.te_extract_data.setReadOnly(True)
        self.btn_extract_data = QPushButton('Извлекать')
        self.btn_extract_data.clicked.connect(self.extract_de)
        self.te_decode_hamm = QTextEdit()
        self.te_decode_hamm.setReadOnly(True)
        self.btn_decode_hamm = QPushButton('Декодировать Хэмминг')
        self.btn_decode_hamm.clicked.connect(self.decode_hamm_de)

        self.grid_de.addWidget(QLabel('ИЗВЛЕЧЕНИЕ'),0,2)
        self.grid_de.addWidget(QLabel('Путь Видео:'),1,0)
        self.grid_de.addWidget(self.le_path_video_de,1,1,1,3)
        self.grid_de.addWidget(self.btn_select_video_de,1,4)
        self.grid_de.addWidget(self.te_aes_de,2,1,1,3)
        self.grid_de.addWidget(QLabel('Ключ AES:'),2,0)
        self.grid_de.addWidget(self.btn_import_key_de,2,4)
        self.grid_de.addWidget(QLabel('Извлекаеммые данные'),3,0)
        self.grid_de.addWidget(self.te_extract_data,3,1,1,3)
        self.grid_de.addWidget(self.btn_extract_data,3,4)
        self.grid_de.addWidget(QLabel('Декодирование Хэмминга:'),4,0)
        self.grid_de.addWidget(self.te_decode_hamm,4,1,1,3)
        self.grid_de.addWidget(self.btn_decode_hamm,4,4)

        self.grid_de.addWidget(QLabel('Текст:'),5,0)
        self.grid_de.addWidget(self.te_text_de,5,1,1,3)
        self.grid_de.addWidget(self.btn_decrypt,5,4)
        self.grid_de.addWidget(self.btn_save_text,6,1)
        self.grid_de.addWidget(self.btn_clear_de,6,3)

    def create_page_play(self):
        self.page_play=QWidget()
        self.stk_page.addWidget(self.page_play)

        self.grid_pl=QGridLayout()
        self.page_play.setLayout(self.grid_pl)

        self.le_path_video_pl=QLineEdit()
        self.le_path_video_pl.setReadOnly(True)
        self.btn_select_video_pl=QPushButton('Выбрать видео')
        self.btn_select_video_pl.clicked.connect(self.select_video_pl)
        self.btn_play=QPushButton('Проиграть')
        self.btn_play.clicked.connect(self.play_video)
        self.btn_clear_pl=QPushButton('Очистить')
        self.btn_clear_pl.clicked.connect(self.clear_pl)

        self.grid_pl.addWidget(QLabel('ПРОИГРАТЬ ВИДЕО'),0,2)
        self.grid_pl.addWidget(QLabel('Путь Видео:'),1,0)
        self.grid_pl.addWidget(self.le_path_video_pl,1,1,1,3)
        self.grid_pl.addWidget(self.btn_select_video_pl,1,4)
        self.grid_pl.addWidget(self.btn_play,2,2,2,1)
        self.grid_pl.addWidget(self.btn_clear_pl,4,2,2,1)

    def switch_page_encode(self):
        self.stk_page.setCurrentIndex(0)

    def switch_page_decode(self):
        self.stk_page.setCurrentIndex(1)

    def switch_page_play(self):
        self.stk_page.setCurrentIndex(2)

    def select_video_en(self):
        try:
            file_dialog=QFileDialog()
            file_dialog.setNameFilter("AVI MOV Files (*.avi *.mov)")
            self.input_video_path_en, _ = file_dialog.getOpenFileName(self, 'Выбрать .avi .mov Файл', '', 'Видео файл (*.avi *mov)')
            if '.avi' in self.input_video_path_en:
                self.type_video_en = 'avi'
            elif '.mov' in self.input_video_path_en:
                self.type_video_en = 'mov'
            self.le_path_video_en.setText(self.input_video_path_en)
            self.max_length=count_volume(self.input_video_path_en)
            text_max_length='Мак-размер:'
            kb=self.max_length/8/1024/1.5
            if kb/1024 >=1 :
                mb=round(kb/1024,2)
                text_max_length=text_max_length+str(mb)+' mb'
            else:
                kb=round(kb,2)
                text_max_length=text_max_length+str(kb)+' kb'
            self.lb_max_lenth_en.setText(text_max_length)

        except:
            QMessageBox.about(self,"Ошибки!!!","Не может выбрать файл")

    def select_video_de(self):
        try:
            file_dialog=QFileDialog()
            file_dialog.setNameFilter("Video Files (*.avi *.mov)")
            self.input_video_path_de, _ = file_dialog.getOpenFileName(self, 'Выбрать .avi .mov Файл', '', 'Видео файл (*.avi *mov)')
            self.le_path_video_de.setText(self.input_video_path_de)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не может выбрать файл")

    def select_video_pl(self):
        try:
            file_dialog=QFileDialog()
            file_dialog.setNameFilter("Video Files (*.avi *mov)")
            self.input_video_path_pl, _ = file_dialog.getOpenFileName(self, 'Выбрать .avi .mov Файл', '', 'Видео файл (*.avi *.mov)')
            self.le_path_video_pl.setText(self.input_video_path_pl)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не может выбрать файл")

    def import_text_en(self):
        try:
            file_dialog=QFileDialog()
            file_dialog.setNameFilter("Text Files (*.txt)")
            self.input_text_path, _ = file_dialog.getOpenFileName(self, 'Выбрать .txt Файл', '', 'Текстовой файл (*.txt)')
            if self.input_text_path:
                with open(self.input_text_path,'r', encoding='utf-8') as f:
                    self.text_en=f.read()
                    self.te_text_input_en.setText(self.text_en)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не может выбрать файл")

    def choose_key_length(self,text):
        if '128' in text:
            self.length_key = 16
        if '192' in text:
            self.length_key = 24
        if '256' in text:
            self.length_key = 32

    def create_key(self):
        self.key_en = get_random_bytes(self.length_key)
        self.te_key_en.setText(str(self.key_en))

    def save_key_en(self):
        if self.key_en == None:
            QMessageBox.about(self,"Ошибки!!!","Надо создать ключ!")
        else:
            file_name=QFileDialog.getSaveFileName(self)
            try:
                write_bytes_to_file(self.key_en, file_name[0]+".txt")
                QMessageBox.about(self,"ok","Сохранить успешно!!!")
            except:
                QMessageBox.about(self,"Ошибки!","Не может сохранить ключ")
    
    def encrypt_en(self):
        if self.text_en == '':
            QMessageBox.about(self,"Ошибки!!!","Надо выбрать текст !")
        elif self.key_en == None:
            QMessageBox.about(self,"Ошибки!!!","Надо создать ключ !")
        else:
            self.encrypted_pad_data = encrypt_padding_data(self.text_en, self.padding, self.key_en)
            self.te_aes_en.setText(self.encrypted_pad_data)

    def encode_hamm_en(self):
        if self.encrypted_pad_data == '':
            QMessageBox.about(self,"Ошибки!!!","Надо шифровать данные !")
        else:
            self.encoded_pad_data = encode_hamm_padding_data(self.encrypted_pad_data)
            self.te_hamming_en.setText(self.encoded_pad_data)

    def embed_en(self):
        self.input_video_path_en=self.le_path_video_en.text()
        if self.encoded_pad_data == '':
            QMessageBox.about(self,"Ошибки!!!","Сделайте по порядку")
        elif self.input_video_path_en=='':
            QMessageBox.about(self,"Ошибки!!!","Надо выбрать видео")
        else:
            if len(self.encoded_pad_data) > int(self.max_length):
                QMessageBox.about(self,"Ошибки!!!","Размер файла .txt превышает допустимый предел!!!")
            else:
                try:
                    file_dialog = QFileDialog()
                    if self.type_video_en == 'avi':
                        file_dialog.setNameFilter("AVI Files (*.avi)")
                        self.output_video_path_en, _ = file_dialog.getSaveFileName(self, 'сохранить видео *.avi', '', 'AVI файл (*.avi)')
                    else:
                        file_dialog.setNameFilter("MOV Files (*.mov)")
                        self.output_video_path_en, _ = file_dialog.getSaveFileName(self, 'сохранить видео *.mov', '', 'MOV файл (*.mov)')           
                    try:
                        stegano_video(self.input_video_path_en, self.encoded_pad_data, self.output_video_path_en)
                        QMessageBox.about(self,'Инфо','Успешно!!!')
                    except cv2.error:
                        QMessageBox.about(self,"Ошибки!!!","Не может встройвать данные в видео!!!")
                except:
                    QMessageBox.about(self,"Ошибки!!!","Не может сохранить файл")
    
    def clear_en(self):
        self.input_video_path_en=''
        self.input_text_path=''
        self.text_en=''
        self.output_video_path_en=''
        self.key_en = None
        self.encrypted_pad_data = ''
        self.encoded_pad_data = ''
        self.type_video_en = ''
        self.le_path_video_en.setText('')
        self.te_text_input_en.setText('')
        self.te_key_en.setText('')
        self.te_aes_en.setText('')
        self.te_hamming_en.setText('')
        self.lb_max_lenth_en.setText('Мак-размер:0 kb')

    def save_text_de(self):
        text=self.te_text_de.toPlainText()
        if text == '' or text == 'Не нашел текст !!!':
            QMessageBox.about(self,"Ошибки!!!","Не может сохранить файл")
        else:
            file_name=QFileDialog.getSaveFileName(self)
            try:
                file=open(file_name[0]+".txt",'w',encoding='utf-8')
                file.write(text)
                file.close()
                QMessageBox.about(self,"ok","Сохранить успешно!!!")
            except:
                QMessageBox.about(self,"Ошибки!","Не может сохранить файл")

    def import_key(self):
        try:
            file_dialog=QFileDialog()
            file_dialog.setNameFilter("Text Files (*.txt)")
            key_path, _ = file_dialog.getOpenFileName(self, 'Выбрать .txt Файл', '', 'Текстовой файл (*.txt)')
            if key_path:
                self.key_de = read_file_as_bytes(key_path)
                self.te_aes_de.setText(str(self.key_de))
        except:
            QMessageBox.about(self,"Ошибки!!!","Не может выбрать файл")

    def extract_de(self):
        if self.input_video_path_de == '':
            QMessageBox.about(self,"Ошибки!!!","Надо выбрать видео")
        elif self.key_de == None:
            QMessageBox.about(self,"Ошибки!!!","Надо выбрать ключ")
        else:
            self.data_embed_pad_de = extract_data_from_video(self.input_video_path_de, self.key_de, self.padding, self.length_block_aes)
            self.te_extract_data.setText(self.data_embed_pad_de)

    def decode_hamm_de(self):
        try:
            if self.data_embed_pad_de == '':
                QMessageBox.about(self,"Ошибки!!!","Сделайте по порядку !")
            elif self.data_embed_pad_de == 'Не нашел текст !!!':
                self.decoded_hamm_data_pad_de = 'Не нашел текст !!!'
                self.te_decode_hamm.setText(self.decoded_hamm_data_pad_de)
            else:
                self.decoded_hamm_data_pad_de = decode_hamm(self.data_embed_pad_de)
                self.te_decode_hamm.setText(self.decoded_hamm_data_pad_de)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не нашел текст !!!")

    def decrypt_de(self):
        try:
            if self.decoded_hamm_data_pad_de == '':
                QMessageBox.about(self,"Ошибки!!!","Сделайте по порядку !")
            elif self.data_embed_pad_de == 'Не нашел текст !!!':
                self.org_data = self.data_embed_pad_de
                self.te_text_de.setText(self.org_data)
            else:
                self.org_data = decrypt_data(self.decoded_hamm_data_pad_de, self.length_block_aes, self.key_de)
                self.te_text_de.setText(self.org_data)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не нашел текст !!!")

    def clear_de(self):
        self.key_de = None
        self.input_video_path_de = ''
        self.data_embed_pad_de = ''
        self.decoded_hamm_data_pad_de = ''
        self.org_data = ''
        self.le_path_video_de.setText('')
        self.te_text_de.setText('')
        self.te_aes_de.setText('')
        self.te_extract_data.setText('')
        self.te_decode_hamm.setText('')
        self.te_text_de.setText('')

    def play_video(self):
        try:
            self.input_video_path_pl=self.le_path_video_pl.text()
            if self.input_video_path_pl=='':
                QMessageBox.about(self,"Ошибки!!!","Надо выбрать видео")
            else:
                play_video_lib(self.input_video_path_pl)
        except:
            QMessageBox.about(self,"Ошибки!!!","Не может играть видео!!!")

    def clear_pl(self):
        self.input_video_path_pl=''
        self.le_path_video_pl.setText('')



#--------------main-------------

app=QApplication(sys.argv)
win=Window()
win.show()
sys.exit(app.exec_())