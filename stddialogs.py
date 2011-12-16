import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qtdefines import *

from armoryengine import *
from armorymodels import *
from qlabelbutton import *

################################################################################
def createToolTipObject(tiptext, iconSz=2):
   lbl = QLabel('<font size=%d color="blue"><u>(?)</u></font>' % iconSz)
   lbl.setToolTip('<u></u>' + tiptext)
   return lbl

################################################################################
class DlgUnlockWallet(QDialog):
   def __init__(self, parent=None):
      super(DlgUnlockWallet, self).__init__(parent)

      lblDescr  = QLabel("Enter your passphrase to unlock this wallet")
      lblPasswd = QLabel("Passphrase:")
      self.edtPasswd = QLineEdit()
      self.edtPasswd.setEchoMode(QLineEdit.Password)
      fm = QFontMetricsF(QFont(self.font()))
      self.edtPasswd.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

      self.btnAccept = QPushButton("Unlock")
      self.btnCancel = QPushButton("Cancel")
      self.connect(self.btnAccept, SIGNAL('clicked()'), self.accept)
      self.connect(self.btnCancel, SIGNAL('clicked()'), self.reject)
      buttonBox = QDialogButtonBox()
      buttonBox.addButton(self.btnAccept, QDialogButtonBox.AcceptRole)
      buttonBox.addButton(self.btnCancel, QDialogButtonBox.RejectRole)

      layout = QGridLayout()
      layout.addWidget(lblDescr,       1, 0, 1, 2)
      layout.addWidget(lblPasswd,      2, 0, 1, 1)
      layout.addWidget(self.edPasswd,  2, 1, 1, 1)
      layout.addWidget(buttonBox,      3, 1, 1, 2)

      self.setLayout(layout)
      #btngrp = self.QButtonGroup()
      #self.QRadioButton()
      #lbl
   

################################################################################
class DlgNewWallet(QDialog):

   def __init__(self, parent=None):
      super(DlgNewWallet, self).__init__(parent)

      # Options for creating a new wallet
      lblDlgDescr = QLabel('Create a new wallet for managing your funds.\n'
                           'The name and description can be changed at any time.')
      lblDlgDescr.setWordWrap(True)

      self.edtName = QLineEdit()
      self.edtName.setMaxLength(32)
      lblName = QLabel("Wallet &name:")
      lblName.setBuddy(self.edtName)


      self.edtDescr = QTextEdit()
      self.edtDescr.setMaximumHeight(75)
      lblDescr = QLabel("Wallet &description:")
      lblDescr.setAlignment(Qt.AlignVCenter)
      lblDescr.setBuddy(self.edtDescr)

      buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | \
                                   QDialogButtonBox.Cancel)


      
      # Advanced Encryption Options
      lblComputeDescr = QLabel('Armory will test your system\'s speed to determine the most '
                               'challenging encryption settings that can be performed '
                               'in a given amount of time.  High settings make it extremely difficult '
                               'for someone to guess your passphrase. This is used for all '
                               'encrypted wallets, but the default parameters can be changed below.\n')
      lblComputeDescr.setWordWrap(True)
      timeDescrTip = createToolTipObject(
                               'This is the amount of time it will take for your computer '
                               'to unlock your wallet after you enter your passphrase. '
                               '(the actual time will be between T/2 and T).  ')
      
      
      # Set maximum compute time
      self.edtComputeTime = QLineEdit()
      self.edtComputeTime.setText('250 ms')
      self.edtComputeTime.setMaxLength(12)
      lblComputeTime = QLabel('Target compute &time (s, ms):')
      memDescrTip = createToolTipObject(
                               'This is the <b>maximum</b> memory that will be '
                               'used as part of the encryption process.  The actual value used '
                               'may be lower, depending on your system\'s speed.  If a '
                               'low value is chosen, Armory will compensate by chaining '
                               'together more calculations to meet the target time.  High '
                               'memory target will make GPU-acceleration useless for '
                               'guessing your passphrase.')
      lblComputeTime.setBuddy(self.edtComputeTime)


      # Set maximum memory usage
      self.edtComputeMem = QLineEdit()
      self.edtComputeMem.setText('32.0 MB')
      self.edtComputeMem.setMaxLength(12)
      lblComputeMem  = QLabel('Max &memory usage (kB, MB):')
      lblComputeMem.setBuddy(self.edtComputeMem)

      self.chkForkOnline = QCheckBox('Create an "&online" copy of this wallet')

      onlineToolTip = createToolTipObject(
                             'An "online" wallet is a copy of your primary wallet, but '
                             'without any sensitive data that would allow an attacker to '
                             'obtain access to your funds.  An "online" wallet can '
                             'generate new addresses and verify incoming payments '
                             'but cannot be used to spend any of the funds.')
      # Fork watching-only wallet


      cryptoLayout = QGridLayout()
      cryptoLayout.addWidget(lblComputeDescr,     0, 0, 1, 3)
      cryptoLayout.addWidget(lblComputeTime,      1, 0, 1, 1)
      cryptoLayout.addWidget(lblComputeMem,       2, 0, 1, 1)
      cryptoLayout.addWidget(self.edtComputeTime, 1, 1, 1, 1)
      cryptoLayout.addWidget(timeDescrTip,        1, 3, 1, 1)
      cryptoLayout.addWidget(self.edtComputeMem,  2, 1, 1, 1)
      cryptoLayout.addWidget(memDescrTip,         2, 3, 1, 1)
      cryptoLayout.addWidget(self.chkForkOnline,  3, 0, 1, 1)
      cryptoLayout.addWidget(onlineToolTip,       3, 1, 1, 1)

      self.cryptoFrame = QFrame()
      self.cryptoFrame.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
      self.cryptoFrame.setLayout(cryptoLayout)
      self.cryptoFrame.setVisible(False)

      #self.chkWatchOnly = QCheckBox("Make this a watching-only wallet\n(no private key data)")
      self.chkUseCrypto = QCheckBox("Use wallet &encryption")
      self.chkUseCrypto.setChecked(True)
      usecryptoTooltip = createToolTipObject(
                                 'Encryption prevents anyone who accesses your computer '
                                 'from being able to spend your funds, but does require '
                                 'typing in a passphrase before you can send money. '
                                 'You can choose to encrypt your wallet at a later time '
                                 'through the wallet options by double clicking the wallet '
                                 'on the dashboard.')


      
      self.btnAccept    = QPushButton("Accept")
      self.btnCancel    = QPushButton("Cancel")
      self.btnAdvCrypto = QPushButton("Adv. Encrypt Options>>>")
      self.btnAdvCrypto.setCheckable(True)
      self.btnbox = QDialogButtonBox()
      self.btnbox.addButton(self.btnAdvCrypto, QDialogButtonBox.ActionRole)
      self.btnbox.addButton(self.btnCancel,    QDialogButtonBox.RejectRole)
      self.btnbox.addButton(self.btnAccept,    QDialogButtonBox.AcceptRole)

      self.connect(self.btnAdvCrypto, SIGNAL('toggled(bool)'), \
                   self.cryptoFrame,  SLOT('setVisible(bool)'))
      self.connect(self.btnAccept,    SIGNAL('clicked()'), \
                   self.verifyInputsBeforeAccept)
      self.connect(self.btnCancel,    SIGNAL('clicked()'), \
                   self,              SLOT('reject()'))


      self.btnImportWlt = QPushButton("Import wallet...")
      self.connect( self.btnImportWlt, SIGNAL("clicked()"), \
                    self.getImportWltPath)
      
      masterLayout = QGridLayout()
      masterLayout.addWidget(lblDlgDescr,       1, 0, 1, 2)
      masterLayout.addWidget(self.btnImportWlt, 1, 2, 1, 1)
      masterLayout.addWidget(lblName,           2, 0, 1, 1)
      masterLayout.addWidget(self.edtName,      2, 1, 1, 2)
      masterLayout.addWidget(lblDescr,          3, 0, 1, 2)
      masterLayout.addWidget(self.edtDescr,     3, 1, 2, 2)
      masterLayout.addWidget(self.chkUseCrypto, 5, 0, 1, 1)
      masterLayout.addWidget(usecryptoTooltip,  5, 1, 1, 1)
      masterLayout.addWidget(self.cryptoFrame,  7, 0, 3, 3)
   
      masterLayout.addWidget(self.btnbox,      10, 0, 1, 2)

      masterLayout.setVerticalSpacing(15)
     
      self.setLayout(masterLayout)

      self.layout().setSizeConstraint(QLayout.SetFixedSize)

      self.connect(self.chkUseCrypto, SIGNAL("clicked()"), \
                   self.cryptoFrame,  SLOT("setEnabled(bool)"))

      self.setWindowTitle('Create/Import Armory wallet')
      self.setWindowIcon(QIcon('icons/armory_logo_32x32.png'))



   def verifyInputsBeforeAccept(self):

      ### Confirm that the name and descr are within size limits #######
      wltName  = self.edtName.text()
      wltDescr = self.edtDescr.toPlainText()
      if len(wltName)<1:
         QMessageBox.warning(self, 'Invalid wallet name', \
                  'You must enter a name for this wallet, up to 32 characters.', \
                  QMessageBox.Ok)
         return False
         
      if len(wltDescr)>256:
         reply = QMessageBox.warning(self, 'Input too long', \
                  'The wallet description is limited to 256 characters.  Only the first '
                  '256 characters will be used.', \
                  QMessageBox.Ok | QMessageBox.Cancel)
         if reply==QMessageBox.Ok:
            self.edtDescr.setText( wltDescr[:256])
         else:
            return False

      ### Check that the KDF inputs are well-formed ####################
      try:
         kdfT, kdfUnit = str(self.edtComputeTime.text()).split(' ') 
         if kdfUnit.lower()=='ms':
            self.kdfSec = float(kdfT)/1000.
         elif kdfUnit.lower() in ('s', 'sec', 'seconds'):
            self.kdfSec = float(kdfT)

         kdfM, kdfUnit = str(self.edtComputeMem.text()).split(' ')
         if kdfUnit.lower()=='mb':
            self.kdfBytes = round(float(kdfM))*(1024.0**2) 
         if kdfUnit.lower()=='kb':
            self.kdfBytes = round(float(kdfM))*(1024.0)

         print self.kdfSec, self.kdfBytes
      except:
         raise
         QMessageBox.critical(self, 'Invalid KDF Parameters', \
            'The KDF parameters that you entered are not valid.  Please '
            'specify KDF time in seconds or milliseconds, such as '
            '"250 ms" or "2.1 s".  And specify memory as kB or MB, such as '
            '"32 MB" or "256 kB". ', QMessageBox.Ok)
         return False
         
      
      self.accept()
            
            
   def getImportWltPath(self):
      self.importFile = QFileDialog.getOpenFileName(self, 'Import Wallet File', \
          ARMORY_HOME_DIR, 'Wallet files (*.wallet);; All files (*)') 
      if self.importFile:
         print self.importFile
         self.accept()
      



################################################################################
class DlgChangePassphrase(QDialog):
   def __init__(self, parent=None, noPrevEncrypt=True):
      super(DlgChangePassphrase, self).__init__(parent)


      layout = QGridLayout()
      if noPrevEncrypt:
         lblDlgDescr = QLabel('Please enter an passphrase for wallet encryption.\n\n'
                              'A good passphrase consists of at least 8 or more\n'
                              'random letters, or 5 or more random words.\n')
         lblDlgDescr.setWordWrap(True)
         layout.addWidget(lblDlgDescr, 0, 0, 1, 2)
      else:
         lblDlgDescr = QLabel("Change your wallet encryption passphrase")
         layout.addWidget(lblDlgDescr, 0, 0, 1, 2)
         self.edtPasswdOrig = QLineEdit()
         self.edtPasswdOrig.setEchoMode(QLineEdit.Password)
         lblCurrPasswd = QLabel('Current Passphrase:')
         layout.addWidget(lblCurrPasswd,       1, 0)
         layout.addWidget(self.edtPasswdOrig,  1, 1)



      lblPwd1 = QLabel("New Passphrase:")
      lblPwd2 = QLabel("Again:")
      self.edtPasswd1 = QLineEdit()
      self.edtPasswd2 = QLineEdit()
      self.edtPasswd1.setEchoMode(QLineEdit.Password)
      self.edtPasswd2.setEchoMode(QLineEdit.Password)

      layout.addWidget(lblPwd1, 2,0)
      layout.addWidget(lblPwd2, 3,0)
      layout.addWidget(self.edtPasswd1, 2,1)
      layout.addWidget(self.edtPasswd2, 3,1)

      self.lblMatches = QLabel(' '*20)
      self.lblMatches.setTextFormat(Qt.RichText)
      layout.addWidget(self.lblMatches, 4,1)


      self.chkDisableCrypt = QCheckBox('Disable encryption for this wallet')
      if not noPrevEncrypt:
         self.connect(self.chkDisableCrypt, SIGNAL('clicked()'), \
                      self,                 SLOT('disablePassphraseBoxes(bool)'))
         layout.addWidget(self.chkDisableCrypt, 4,0)
         

      
         

      self.btnAccept = QPushButton("Accept")
      self.btnCancel = QPushButton("Cancel")
      buttonBox = QDialogButtonBox()
      buttonBox.addButton(self.btnAccept, QDialogButtonBox.AcceptRole)
      buttonBox.addButton(self.btnCancel, QDialogButtonBox.RejectRole)
      layout.addWidget(buttonBox, 5, 0, 1, 2)

      if noPrevEncrypt:
         self.setWindowTitle("Set Encryption Passphrase")
      else:
         self.setWindowTitle("Change Encryption Passphrase")

      self.setWindowIcon(QIcon('icons/armory_logo_32x32.png'))

      self.setLayout(layout)

      self.connect(self.edtPasswd1, SIGNAL('textChanged(QString)'), \
                   self.checkPassphrase)
      self.connect(self.edtPasswd2, SIGNAL('textChanged(QString)'), \
                   self.checkPassphrase)

      self.connect(self.btnAccept, SIGNAL('clicked()'), \
                   self.checkPassphraseFinal)

      self.connect(self.btnCancel, SIGNAL('clicked()'), \
                   self,           SLOT('reject()'))


   def disablePassphraseBoxes(self, noEncrypt=True):
      self.edtPasswd1.setEnabled(not noEncrypt) 
      self.edtPasswd2.setEnabled(not noEncrypt) 


   def checkPassphrase(self):
      p1 = self.edtPasswd1.text()
      p2 = self.edtPasswd2.text()
      if not p1==p2:
         self.lblMatches.setText('<font color="red"><b>Passphrases do not match!</b></font>')
         return False
      if len(p1)<5 and not self.chkDisableCrypt.isChecked():
         self.lblMatches.setText('<font color="red"><b>Passphrase is too short!</b></font>')
         return False
      self.lblMatches.setText('<font color="green"><b>Passphrases match!</b></font>')
      return True
      

   def checkPassphraseFinal(self):
      if self.checkPassphrase():
         reply = QMessageBox.warning(self,  \
            'WARNING!', \
            '!!!  DO NOT FORGET YOUR PASSPHRASE  !!!\n\n'
            'Bitcoin Armory wallet encryption is designed to be extremely difficult to '
            'crack, even with GPU-acceleration.  No one can help you recover your coins '
            'if you forget your passphrase, not even the developers of this software. '
            'If you are inclined to forget your passphrase, please write it down and '
            'store it in a secure location.\n\nAre you sure you will remember you passphrase?', \
            QMessageBox.Yes | QMessageBox.No)

         if reply == QMessageBox.Yes:
            self.accept()


#class DlgDispWltProperties(QDialog):
   #def __init__(self, parent=None):
      #super(DlgDispWltProperties, self).__init__(parent)


################################################################################
class DlgChangeLabels(QDialog):
   def __init__(self, currName='', currDescr='', parent=None):
      super(DlgChangeLabels, self).__init__(parent)

      self.edtName = QLineEdit()
      self.edtName.setMaxLength(32)
      lblName = QLabel("Wallet &name:")
      lblName.setBuddy(self.edtName)

      self.edtDescr = QTextEdit()
      fm = QFontMetricsF(QFont(self.edtDescr.font()))
      self.edtDescr.setMaximumHeight(fm.height()*4.2)
      lblDescr = QLabel("Wallet &description:")
      lblDescr.setAlignment(Qt.AlignVCenter)
      lblDescr.setBuddy(self.edtDescr)

      self.edtName.setText(currName)
      self.edtDescr.setText(currDescr)

      buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | \
                                   QDialogButtonBox.Cancel)
      self.connect(buttonBox, SIGNAL('accepted()'), self.accept)
      self.connect(buttonBox, SIGNAL('rejected()'), self.reject)

      layout = QGridLayout()
      layout.addWidget(lblName,         1, 0, 1, 1)
      layout.addWidget(self.edtName,    1, 1, 1, 1)
      layout.addWidget(lblDescr,        2, 0, 1, 1)
      layout.addWidget(self.edtDescr,   2, 1, 2, 1)
      layout.addWidget(buttonBox,       4, 0, 1, 2)
      self.setLayout(layout)
   
      self.setWindowTitle('Wallet Descriptions')

      
################################################################################
class DlgWalletDetails(QDialog):
   """ For displaying the details of a specific wallet, with options """ 

   #############################################################################
   def __init__(self, wlt, usermode=USERMODE.Standard, parent=None):
      super(DlgWalletDetails, self).__init__(parent)
      self.setAttribute(Qt.WA_DeleteOnClose)

      self.wlt = wlt
      self.usermode = usermode
      self.main = parent
      self.wlttype, self.typestr = determineWalletType(wlt, parent)

      self.labels = [wlt.labelName, wlt.labelDescr]
      self.passphrase = ''
      self.setMinimumSize(800,400)
      
      w,h = relaxedSizeNChar(self,60)
      viewWidth,viewHeight  = w, 10*h
      
      self.frm = getWltDetailsFrame(wlt, self.typestr, self.main.usermode)


      # Address view
      lblAddrList = QLabel('Addresses in Wallet:')
      self.wltAddrModel = WalletAddrDispModel(wlt, self)
      self.wltAddrView  = QTableView()
      self.wltAddrView.setModel(self.wltAddrModel)
      self.wltAddrView.setSelectionBehavior(QTableView.SelectRows)
      self.wltAddrView.setSelectionMode(QTableView.SingleSelection)
      self.wltAddrView.horizontalHeader().setStretchLastSection(True)
      self.wltAddrView.verticalHeader().setDefaultSectionSize(20)
      self.wltAddrView.setMinimumWidth(800)
      initialColResize(self.wltAddrView, [0.2, 0.7, 64, 0.3])

   
      uacfv = lambda x: self.main.updateAddressCommentFromView(self.wltAddrView, self.wlt)
      self.connect(self.wltAddrView, SIGNAL('doubleClicked(QModelIndex)'), uacfv)
                   
      #self.connect(self.wltAddrView, SIGNAL('doubleClicked(QModelIndex)'), \
                   #self.main,        SLOT('addrViewDblClicked(QModelIndex)'))
      #clip = QApplication.clipboard()
      #def copyAddrToClipboard()


      # Now add all the options buttons, dependent on the type of wallet.

      lbtnChangeLabels = QLabelButton('Change Wallet Name/Description');
      self.connect(lbtnChangeLabels, SIGNAL('clicked()'), self.changeLabels)

      s = ''
      if self.wlt.useEncryption:
         s = 'Change or Remove Passphrase'
      else:
         s = 'Encrypt Wallet'
      lbtnChangeCrypto = QLabelButton(s)
      self.connect(lbtnChangeCrypto, SIGNAL('clicked()'), self.changeEncryption)

      lbtnGenAddr = QLabelButton('Get New Address')
      lbtnForkWlt = QLabelButton('Fork Watching-Only Wallet Copy')
      lbtnIsMyWlt = QLabelButton('This is my wallet!')
      lbtnMkPaper = QLabelButton('Make Paper Backup')
      lbtnExport  = QLabelButton('Export wallet backup')
      lbtnRemove  = QLabelButton('Delete/Remove wallet')


      optFrame = QFrame()
      optFrame.setFrameStyle(QFrame.Box|QFrame.Sunken)
      optLayout = QVBoxLayout()
      optLayout.addWidget(lbtnChangeLabels)
      optLayout.addWidget(lbtnChangeCrypto)
      optLayout.addWidget(lbtnGenAddr)
      optLayout.addWidget(lbtnForkWlt)
      optLayout.addWidget(lbtnIsMyWlt)
      optLayout.addWidget(lbtnMkPaper)
      optLayout.addWidget(lbtnExport)
      optLayout.addWidget(lbtnRemove)
      optLayout.addStretch()
      optFrame.setLayout(optLayout)

      #buttonBox = QDialogButtonBox()

      #btn1 = QPushButton('Change Labels')
      #self.connect(btn1, SIGNAL('clicked()'), self.changeLabels)
      #buttonBox.addButton(btn1, QDialogButtonBox.ActionRole)

      #if not self.wlttype==WLTTYPES.WatchOnly:
         #btn2 = QPushButton('Change Encryption')
         #self.connect(btn2, SIGNAL('clicked()'), self.changeEncryption)
         #buttonBox.addButton(btn2, QDialogButtonBox.ActionRole)

      #if self.wlttype==WLTTYPES.Crypt and usermode==USERMODE.Advanced:
         #btn3 = QPushButton('Change KDF Params')
         #self.connect(btn3, SIGNAL('clicked()'), self.changeKdf)
         #buttonBox.addButton(btn3, QDialogButtonBox.ActionRole)


      btn4 = QPushButton('<<< Go Back')
      self.connect(btn4, SIGNAL('clicked()'), self.accept)

      layout = QGridLayout()
      layout.addWidget(self.frm,              0, 0, 3, 4)
      layout.addWidget(self.wltAddrView,      4, 0, 2, 4)
      layout.addWidget(btn4,                  6, 0, 1, 1)
      #layout.addWidget(buttonBox,             7, 2, 1, 2)
      layout.addWidget(QLabel("Available Actions:"), \
                                              0, 4)
      layout.addWidget(optFrame,              1, 4, 8, 2)
      self.setLayout(layout)
      
      self.setWindowTitle('Wallet Details')

      
   def changeLabels(self):
      dlgLabels = DlgChangeLabels(self.wlt.labelName, self.wlt.labelDescr, self)
      if dlgLabels.exec_():
         # Make sure to use methods like this which not only update in memory,
         # but guarantees the file is updated, too
         self.wlt.setWalletLabels(str(dlgLabels.edtName.text()), 
                                  str(dlgLabels.edtDescr.toPlainText()))

         self.frm = getWltDetailsFrame(self.wlt, self.typestr, self.main.usermode)


   def changeEncryption(self):
      dlgCrypt = DlgChangePassphrase(self, not self.wlt.useEncryption)
      if dlgCrypt.exec_():
         self.disableEncryption = dlgCrypt.chkDisableCrypt.isChecked()
         newPassphrase = SecureBinaryData(str(dlgCrypt.edtPasswd1.text()))

         if self.wlt.useEncryption:
            origPassphrase = SecureBinaryData(str(dlgCrypt.edtPasswdOrig.text()))
            if self.wlt.verifyPassphrase(origPassphrase):
               self.wlt.unlock(securePassphrase=origPassphrase)
            else:
               # Even if the wallet is already unlocked, enter pwd again to change it
               QMessageBox.critical(self, 'Invalid Passphrase', \
                     'Previous passphrase is not correct!  Could not unlock wallet.', \
                     QMessageBox.Ok)
         
         
         if self.disableEncryption:
            self.wlt.changeWalletEncryption(None, None)
         else:
            if not self.wlt.useEncryption:
               kdfParams = self.wlt.computeSystemSpecificKdfParams(0.2)
               self.wlt.changeKdfParams(*kdfParams)
            self.wlt.changeWalletEncryption(securePassphrase=newPassphrase)
            self.accept()
      

   def getNewAddress(self):
      pass 

   def changeKdf(self):
      """ 
      This is a low-priority feature.  I mean, the PyBtcWallet class has this
      feature implemented, but I don't have a GUI for it
      """
      pass


#############################################################################
class DlgImportWallet(QDialog):
   def __init__(self, parent=None):
      super(DlgImportWallet, self).__init__(parent)
      self.setAttribute(Qt.WA_DeleteOnClose)
      self.main = parent

      lblImportDescr = QLabel('Chose the wallet import source:')
      self.btnImportFile  = QPushButton("Import from &file")
      self.btnImportPaper = QPushButton("Import from &paper backup")

      self.btnImportFile.setMinimumWidth(300)
      self.connect( self.btnImportFile, SIGNAL("clicked()"), \
                    self.getImportWltPath)

      self.connect( self.btnImportFile, SIGNAL("clicked()"), \
                    self.execImportPaperDlg)

      ttip1 = createToolTipObject('Import an existing Armory wallet, usually with a '
                                 '.wallet extension.  Any wallet that you import will ' 
                                 'be copied into your settings directory, and maintained '
                                 'from there.  The original wallet file will not be touched.')

      ttip2 = createToolTipObject('If you have previously made a paper backup of '
                                  'a wallet, you can manually enter the wallet '
                                  'data into Armory to recover the wallet.')


      w,h = relaxedSizeStr(ttip1, '(?)') 
      for ttip in (ttip1, ttip2):
         ttip.setMaximumSize(w,h)
         ttip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

      # Set up the layout
      layout = QGridLayout()
      layout.addWidget(lblImportDescr,      0,0, 1, 2)
      layout.addWidget(self.btnImportFile,  1,0, 1, 2); layout.addWidget(ttip1, 1,2,1,1)
      layout.addWidget(self.btnImportPaper, 2,0, 1, 2); layout.addWidget(ttip2, 2,2,1,1)

      if self.main.usermode in (USERMODE.Advanced, USERMODE.Developer):
         lbl = QLabel('You can manually add wallets to armory by copying them '
                      'into your application directory:  ' + ARMORY_HOME_DIR)
         lbl.setWordWrap(True)
         layout.addWidget(lbl, 3,0, 1, 2); 
         if self.main.usermode==USERMODE.Developer:
            lbl = QLabel('Any files in the application data directory above are '
                         'used in the application if the first 8 bytes of the file '
                         'are "\\xbaWALLET\\x00".  Wallets in this directory can be '
                         'ignored by adding an <i>Excluded_Wallets</i> option to the '
                         'ArmorySettings.txt file.  Reference by full path or wallet ID.')
            lbl.setWordWrap(True)
            layout.addWidget(lbl, 4,0, 1, 2); 

      btnCancel = QPushButton('Cancel')
      self.connect(btnCancel, SIGNAL('clicked()'), self.reject)
      layout.addWidget(btnCancel, 5,0, 1,1);

      self.setLayout(layout)
      self.setWindowTitle('Import Wallet')
      

   def getImportWltPath(self):
      self.importFile = QFileDialog.getOpenFileName(self, 'Import Wallet File', \
          ARMORY_HOME_DIR, 'Wallet files (*.wallet);; All files (*.*)') 
      if self.importFile:
         print 'Importing:', self.importFile
         self.importType_file = True
         self.importType_paper = False
         self.accept()

      
   def execImportPaperDlg(self):
      self.importType_file = False
      self.importType_paper = True
      



#############################################################################
class DlgImportPaperWallet(QDialog):
   def __init__(self, parent=None):
      super(DlgImportWallet, self).__init__(parent)
      


#############################################################################
def getWltDetailsFrame(wlt, typestr, usermode=USERMODE.Standard):

   dispCrypto = wlt.useEncryption and (usermode==USERMODE.Advanced or \
                                       usermode==USERMODE.Developer)
   if dispCrypto:
      kdftimestr = "%0.3f seconds" % wlt.testKdfComputeTime()
      mem = wlt.kdf.getMemoryReqtBytes()
      kdfmemstr = str(mem/1024)+' kB'
      if mem >= 1024*1024:
         kdfmemstr = str(mem/(1024*1024))+' MB'

   FIELDS = enum('Name', 'Descr', 'WltID', 'NumAddr', 'Secure', 'Crypto', 'Time', 'Mem')

   tooltips = [[]]*9

   tooltips[FIELDS.Name] = createToolTipObject(
         'This is the name stored with the wallet file.  Click on the '
         '"Change Labels" button at the bottom of this '
         'window to change this field' )

   tooltips[FIELDS.Descr] = createToolTipObject(
         'This is the description of the wallet stored in the wallet file.  '
         'Press the "Change Labels" button at the bottom of this '
         'window to change this field' )

   tooltips[FIELDS.WltID] = createToolTipObject(
         'This is a unique identifier for this wallet, based on the root key.  '
         'No other wallet can have the same ID '
         'unless it is a copy of this one, regardless of whether '
         'the name and description match.')

   tooltips[FIELDS.NumAddr] = createToolTipObject(
         'The number of addresses generated so far for this wallet.  '
         'This includes addresses imported manually')

   if typestr=='Offline':
      tooltips[FIELDS.Secure] = createToolTipObject(
         'Offline:  This is a "Watching-Only" wallet that you have identified '
         'belongs to you, but you cannot spend any of the wallet funds '
         'using this wallet.  This kind of wallet '
         'is usually stored on an internet-connected computer, to manage '
         'incoming transactions, but the private keys needed '
         'to spend the money are stored on an offline computer.')
   elif typestr=='Watching-Only':
      tooltips[FIELDS.Secure] = createToolTipObject(
         'Watching-Only:  You can only watch addresses in this wallet '
         'but cannot spend any of the funds.')
   elif typestr=='No Encryption':
      tooltips[FIELDS.Secure] = createToolTipObject(
         'No Encryption: This wallet contains private keys, and does not require '
         'a passphrase to spend funds available to this wallet.  If someone '
         'else obtains a copy of this wallet, they can also spend your funds!  '
         '(You can click the "Change Encryption" button at the bottom of this '
         'window to enabled encryption)')
   elif typestr=='Encrypted':
      tooltips[FIELDS.Secure] = createToolTipObject(
         'This wallet contains the private keys needed to spend this wallet\'s '
         'funds, but they are encrypted on your harddrive.  The wallet must be '
         '"unlocked" with the correct passphrase before you can spend any of the '
         'funds.  You can still generate new addresses and monitor incoming '
         'transactions, even with a locked wallet.')

   tooltips[FIELDS.Crypto] = createToolTipObject(
         'The encryption used to secure your wallet keys' )

   tooltips[FIELDS.Time] = createToolTipObject(
         'This is exactly how long it takes your computer to unlock your '
         'wallet after you have entered your passphrase.  If someone got '
         'ahold of your wallet, this is approximately how long it would take '
         'them to for each guess of your passphrase.')

   tooltips[FIELDS.Mem] = createToolTipObject(
         'This is the amount of memory required to unlock your wallet. '
         'Memory values above 2 MB pretty much guarantee that GPU-acceleration '
         'will be useless for guessing your passphrase')

   labelNames = [[]]*9
   labelNames[FIELDS.Name]    = QLabel('Wallet Name:')
   labelNames[FIELDS.Descr]   = QLabel('Description:')

   labelNames[FIELDS.WltID]   = QLabel('Wallet ID:')
   labelNames[FIELDS.NumAddr] = QLabel('#Addresses:')
   labelNames[FIELDS.Secure]  = QLabel('Security:')

   # TODO:  Add wallet path/location to this!

   if dispCrypto:
      labelNames[FIELDS.Crypto] = QLabel('Encryption:')
      labelNames[FIELDS.Time]   = QLabel('Unlock Time:')
      labelNames[FIELDS.Mem]    = QLabel('Unlock Memory:')

   labelValues = [[]]*9
   labelValues[FIELDS.Name]    = QLabel(wlt.labelName)
   labelValues[FIELDS.Descr]   = QLabel(wlt.labelDescr)

   labelValues[FIELDS.WltID]   = QLabel(wlt.wltUniqueIDB58)
   labelValues[FIELDS.NumAddr] = QLabel(str(len(wlt.addrMap)-1))
   labelValues[FIELDS.Secure]  = QLabel(typestr)


   if dispCrypto:
      labelValues[FIELDS.Crypto] = QLabel('AES256')
      labelValues[FIELDS.Time]   = QLabel(kdftimestr)
      labelValues[FIELDS.Mem]    = QLabel(kdfmemstr)

   for ttip in tooltips:
      try:
         ttip.setAlignment(Qt.AlignRight | Qt.AlignTop)
         w,h = relaxedSizeStr(ttip, '(?)') 
         ttip.setMaximumSize(w,h)
      except AttributeError:
         pass

   for lbl in labelNames:
      try:
         lbl.setTextFormat(Qt.RichText)
         lbl.setText( '<b>' + lbl.text() + '</b>')
         lbl.setContentsMargins(0, 0, 0, 0)
         w,h = tightSizeStr(lbl, '9'*14)
         lbl.setMaximumSize(w,h)
      except AttributeError:
         pass


   for lbl in labelValues:
      try:
         lbl.setText( '<i>' + lbl.text() + '</i>')
         lbl.setContentsMargins(10, 0, 10, 0)
         lbl.setTextInteractionFlags(Qt.TextSelectableByMouse | \
                                     Qt.TextSelectableByKeyboard)
      except AttributeError:
         pass

   labelNames[FIELDS.Descr].setAlignment(Qt.AlignLeft | Qt.AlignTop)
   labelValues[FIELDS.Descr].setWordWrap(True)
   labelValues[FIELDS.Descr].setAlignment(Qt.AlignLeft | Qt.AlignTop)

   lblEmpty = QLabel(' '*20)

   layout = QGridLayout()
   layout.addWidget(tooltips[FIELDS.Name],        0, 0); 
   layout.addWidget(labelNames[FIELDS.Name],      0, 1); 
   layout.addWidget(labelValues[FIELDS.Name],     0, 2)

   layout.addWidget(tooltips[FIELDS.Descr],       1, 0); 
   layout.addWidget(labelNames[FIELDS.Descr],     1, 1); 
   layout.addWidget(labelValues[FIELDS.Descr],    1, 2, 3, 1)

   layout.addWidget(tooltips[FIELDS.WltID],       0, 3); 
   layout.addWidget(labelNames[FIELDS.WltID],     0, 4); 
   layout.addWidget(labelValues[FIELDS.WltID],    0, 5)

   layout.addWidget(tooltips[FIELDS.NumAddr],     1, 3); 
   layout.addWidget(labelNames[FIELDS.NumAddr],   1, 4); 
   layout.addWidget(labelValues[FIELDS.NumAddr],  1, 5)

   layout.addWidget(tooltips[FIELDS.Secure],      2, 3); 
   layout.addWidget(labelNames[FIELDS.Secure],    2, 4); 
   layout.addWidget(labelValues[FIELDS.Secure],   2, 5)


   if dispCrypto:
      layout.addWidget(tooltips[FIELDS.Crypto],    0, 6); 
      layout.addWidget(labelNames[FIELDS.Crypto],  0, 7); 
      layout.addWidget(labelValues[FIELDS.Crypto], 0, 8)

      layout.addWidget(tooltips[FIELDS.Time],      1, 6); 
      layout.addWidget(labelNames[FIELDS.Time],    1, 7); 
      layout.addWidget(labelValues[FIELDS.Time],   1, 8)

      layout.addWidget(tooltips[FIELDS.Mem],       2, 6); 
      layout.addWidget(labelNames[FIELDS.Mem],     2, 7); 
      layout.addWidget(labelValues[FIELDS.Mem],    2, 8)
   else:
      layout.addWidget(lblEmpty, 0, 4); layout.addWidget(lblEmpty, 0, 5)
      layout.addWidget(lblEmpty, 1, 4); layout.addWidget(lblEmpty, 1, 5)
      layout.addWidget(lblEmpty, 2, 4); layout.addWidget(lblEmpty, 2, 5)
      pass
      

   infoFrame = QFrame()
   infoFrame.setFrameStyle(QFrame.Box|QFrame.Sunken)
   infoFrame.setLayout(layout)
   
   return infoFrame


################################################################################
class DlgSetComment(QDialog):
   """ This will be a dumb dialog for retrieving a comment from user """

   #############################################################################
   def __init__(self, currComment='', ctype='', parent=None):
      super(DlgSetComment, self).__init__(parent)

      self.setWindowTitle('Add/Change Comment')
      self.setWindowIcon(QIcon('icons/armory_logo_32x32.png'))

      buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | \
                                   QDialogButtonBox.Cancel)
      self.connect(buttonBox, SIGNAL('accepted()'), self.accept)
      self.connect(buttonBox, SIGNAL('rejected()'), self.reject)

      layout = QGridLayout()
      lbl = None
      if     ctype and     currComment: lbl = QLabel('Change %s comment:'%ctype)
      if not ctype and     currComment: lbl = QLabel('Change comment:')
      if     ctype and not currComment: lbl = QLabel('Add %s comment:'%ctype)
      if not ctype and not currComment: lbl = QLabel('Add comment:')
      self.edtComment = QLineEdit()
      self.edtComment.setText(currComment)
      h,w = relaxedSizeNChar(self, 50)
      self.edtComment.setMinimumSize(h,w)
      #h = self.edtComment.height()
      #self.edtComment.setMinimumSize(h, 200)
      layout.addWidget(lbl,             0,0)
      layout.addWidget(self.edtComment, 1,0)
      layout.addWidget(buttonBox,       2,0)
      self.setLayout(layout)


if __name__=='__main__':
   app = QApplication(sys.argv)
   app.setApplicationName("DumbDialogs")

   form = DlgNewWallet()
   #form = DlgChangePassphrase(noPrevEncrypt=True)

   form.show()
   app.exec_()





