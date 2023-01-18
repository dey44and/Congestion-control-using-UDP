import sys

from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import *

from Entity import utility as util
from Packets.packet_factory import PacketFactory
from client import *

info = "List of commands\n" \
       "ls - Show files\n" \
       "add [file_name] - Add a file\n" \
       "app [file_name] - Append to a file\n" \
       "rm [file_name] - Remove a file\n"


class Ui_MainWindow(object):
    def __init__(self):
        # Connecting controls to functions
        self.connected_to_server = False
        self.client = None

        # Widgets
        self.centralwidget = None
        self.server_connection_frame = None
        self.connect_button = None
        self.dest_ip_label = None
        self.port_source_label = None
        self.port_dest_label = None
        self.input_ip = None
        self.input_sport = None
        self.input_dport = None
        self.server_connection_title = None
        self.server_connection_frame = None
        self.user_conn_title = None
        self.user_conn_frame = None
        self.input_username = None
        self.username = None
        self.password = None
        self.input_password = None
        self.frame = None
        self.command_line = None
        self.send_request_title = None
        self.command_line_label = None
        self.submit = None
        self.display_instr = None
        self.textEdit = None
        self.statusbar = None

    def setup_ui(self, main_window):
        if main_window.objectName():
            main_window.setObjectName(u"Client App")

        main_window.resize(587, 635)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")

        self.server_connection_frame = QFrame(self.centralwidget)
        self.server_connection_frame.setObjectName(u"server_connection_frame")
        self.server_connection_frame.setGeometry(QRect(10, 30, 281, 171))

        font = QFont()
        font.setStrikeOut(False)
        self.server_connection_frame.setFont(font)
        self.server_connection_frame.setAutoFillBackground(False)
        self.server_connection_frame.setFrameShape(QFrame.Panel)
        self.server_connection_frame.setFrameShadow(QFrame.Raised)

        self.connect_button = QPushButton(self.server_connection_frame)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setGeometry(QRect(80, 130, 93, 28))
        # Connection button command
        self.connect_button.clicked.connect(self.connect_to_server)

        self.dest_ip_label = QLabel(self.server_connection_frame)
        self.dest_ip_label.setObjectName(u"dest_ip_label")
        self.dest_ip_label.setGeometry(QRect(10, 40, 71, 16))

        font1 = QFont()
        font1.setPointSize(10)
        font1.setStrikeOut(False)

        self.dest_ip_label.setFont(font1)
        self.port_source_label = QLabel(self.server_connection_frame)
        self.port_source_label.setObjectName(u"port_source_label")
        self.port_source_label.setGeometry(QRect(10, 70, 111, 21))
        self.port_source_label.setFont(font1)

        self.port_dest_label = QLabel(self.server_connection_frame)
        self.port_dest_label.setObjectName(u"port_dest_label")
        self.port_dest_label.setGeometry(QRect(10, 100, 91, 21))
        self.port_dest_label.setFont(font1)

        self.input_ip = QLineEdit(self.server_connection_frame)
        self.input_ip.setObjectName(u"input_ip")
        self.input_ip.setGeometry(QRect(110, 40, 151, 22))

        self.input_sport = QLineEdit(self.server_connection_frame)
        self.input_sport.setObjectName(u"input_sport")
        self.input_sport.setGeometry(QRect(110, 70, 151, 22))

        self.input_dport = QLineEdit(self.server_connection_frame)
        self.input_dport.setObjectName(u"input_dport")
        self.input_dport.setGeometry(QRect(110, 100, 151, 22))

        self.server_connection_title = QLabel(self.server_connection_frame)
        self.server_connection_title.setObjectName(u"server_connection_title")
        self.server_connection_title.setGeometry(QRect(30, 10, 191, 16))

        font2 = QFont()
        font2.setPointSize(12)
        font2.setStrikeOut(False)

        self.server_connection_title.setFont(font2)
        self.user_conn_frame = QFrame(self.centralwidget)
        self.user_conn_frame.setObjectName(u"user_conn_frame")
        self.user_conn_frame.setGeometry(QRect(300, 30, 281, 111))
        self.user_conn_frame.setFrameShape(QFrame.Panel)
        self.user_conn_frame.setFrameShadow(QFrame.Raised)

        self.username = QLabel(self.user_conn_frame)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(10, 40, 101, 16))

        font3 = QFont()
        font3.setPointSize(10)
        self.username.setFont(font3)

        self.password = QLabel(self.user_conn_frame)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(10, 70, 111, 21))
        self.password.setFont(font3)

        self.input_username = QLineEdit(self.user_conn_frame)
        self.input_username.setObjectName(u"input_username")
        self.input_username.setGeometry(QRect(110, 40, 151, 22))

        self.input_password = QLineEdit(self.user_conn_frame)
        self.input_password.setObjectName(u"input_password")
        self.input_password.setGeometry(QRect(110, 70, 151, 22))

        self.user_conn_title = QLabel(self.user_conn_frame)
        self.user_conn_title.setObjectName(u"user_conn_title")
        self.user_conn_title.setGeometry(QRect(10, 0, 181, 31))

        font4 = QFont()
        font4.setPointSize(12)
        self.user_conn_title.setFont(font4)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 260, 571, 351))
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.command_line = QLineEdit(self.frame)
        self.command_line.setObjectName(u"command_line")
        self.command_line.setGeometry(QRect(160, 40, 241, 22))

        self.send_request_title = QLabel(self.frame)
        self.send_request_title.setObjectName(u"send_request_title")
        self.send_request_title.setGeometry(QRect(210, 10, 141, 21))
        self.send_request_title.setFont(font4)

        self.command_line_label = QLabel(self.frame)
        self.command_line_label.setObjectName(u"command_line_label")
        self.command_line_label.setGeometry(QRect(30, 40, 111, 21))
        self.command_line_label.setFont(font3)

        self.submit = QPushButton(self.frame)
        self.submit.setObjectName(u"submit")
        self.submit.setGeometry(QRect(432, 40, 131, 28))
        # Submit button command
        self.submit.clicked.connect(self.send_request)

        self.display_instr = QPushButton(self.frame)
        self.display_instr.setObjectName(u"display_instr")
        self.display_instr.setGeometry(QRect(430, 80, 131, 28))
        # Add display instruction button
        self.display_instr.clicked.connect(self.display_instructions)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(160, 120, 241, 221))

        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    # retranslateUi
    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", "Client App", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.dest_ip_label.setText(QCoreApplication.translate("MainWindow", u"IP Dest:", None))
        self.port_source_label.setText(QCoreApplication.translate("MainWindow", u"Port Source:", None))
        self.port_dest_label.setText(QCoreApplication.translate("MainWindow", u"Port Dest.:", None))
        self.server_connection_title.setText(QCoreApplication.translate("MainWindow", u"1. Server Connection", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"Username:", None))
        self.password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.user_conn_title.setText(QCoreApplication.translate("MainWindow", u"2. User connection", None))
        self.send_request_title.setText(QCoreApplication.translate("MainWindow", u"3. Send request", None))
        self.command_line_label.setText(QCoreApplication.translate("MainWindow", u"Command line:", None))
        self.submit.setText(QCoreApplication.translate("MainWindow", u"Send request", None))
        self.display_instr.setText(QCoreApplication.translate("MainWindow", u"Display all commands", None))

    def connect_to_server(self):
        self.textEdit.clear()
        if not self.connected_to_server:
            # Realizare validare parametri
            test_passed = True
            if not util.is_valid_ip(self.input_ip.text()):
                test_passed = False
                self.textEdit.append("Error: Invalid IP Address!\n")
            if not util.is_valid_port(self.input_sport.text()):
                test_passed = False
                self.textEdit.append("Error: Invalid Source Port number!\n")
            if not util.is_valid_port(self.input_dport.text()):
                test_passed = False
                self.textEdit.append("Error: Invalid Dest Port number!\n")

            if test_passed:
                try:
                    # Start client on different thread
                    self.client = Client(self.input_sport.text(), self.input_dport.text(), self.input_ip.text(), 0.01)
                    self.client.start()

                    self.connected_to_server = True
                    self.textEdit.append("Info: Interface connected to the server!\n")
                except:
                    self.textEdit.append("Error: Problems while establishing a connection to the server!\n")
                    sys.exit(-1)
        else:
            self.textEdit.append("Warning: Interface already connected to server!")

    def send_request(self):
        # Get command from text box
        command = self.command_line.text()

        # Check command
        arguments = command.split(" ")

        # Add to arguments content if command is app
        if arguments[0] == "app":
            arguments.append(self.textEdit.toPlainText())

        # Generate packet
        packet_generator: PacketFactory = PacketFactory(arguments)
        packet = packet_generator.get_packet()

        # Send packet to client
        self.client.add_packet(packet)

    def display_instructions(self):
        self.textEdit.clear()
        self.textEdit.append(info)
