import os
import smtplib
import win32file
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import win32con

# set up SMTP server
server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.ehlo()
server.starttls()
server.login('mileshiggins7@gmail.com', 'kavjgagwwbphugww')

# compose email
address = 'mileshiggins7@gmail.com'
msg = MIMEMultipart()  # create message object
msg['From'] = address
msg['To'] = address
msg['Subject'] = 'New File'


# set up directory

ACTIONS = {
  1: "Created",
  2: "Deleted",
  3: "Updated",
  4: "Renamed from something",
  5: "Renamed to something"
}
FILE_LIST_DIRECTORY = 0x0001
path_to_watch = r"C:\Users\Miles\Documents\Miles\Automatic email"
hdir = win32file.CreateFile(  # what does this do?
    path_to_watch,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
)

# wait for change in dir
while 1:
    results = win32file.ReadDirectoryChangesW(
        hdir,
        2048,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
        win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
        win32con.FILE_NOTIFY_CHANGE_SIZE |
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
        win32con.FILE_NOTIFY_CHANGE_SECURITY,
        None,
        None
    )
    for action, file in results:
        full_filename = os.path.join(path_to_watch, file)
        # attach file
        with open(full_filename, "rb") as f:
            attachment = MIMEApplication(f.read())

        attachment.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(attachment)

        # send email
        server.send_message(msg)
        del msg


# how to limit files to ones that have been created or updated?

