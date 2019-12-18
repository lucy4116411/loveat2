import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL


def send_forget_password_email(email, link):
    msg = MIMEMultipart()
    msg["From"] = "loveatsquared@gmail.com"
    msg["To"] = email
    msg["Subject"] = "loveat2密碼重設認證信函"

    body = """
    ＊ 此信件為系統發出信件，請勿直接回覆，感謝您的配合。謝謝！＊

    親愛的會員 您好：

    這封認證信是由loveat2發出，用以處理您忘記密碼，當您收到本「認證信函」後，請直接點選下方連結重新設置您的密碼，無需回信。

    {link}

    為了確保您的會員資料安全，重設密碼的連結將於此信件寄出一小時後失效。
    """.format(
        link=link
    )
    msg.attach(MIMEText(body, "plain"))

    host = socket.gethostbyname("smtp.gmail.com")
    server = smtplib.SMTP(host, 587)
    server.starttls()
    server.login(EMAIL["name"], EMAIL["password"])
    text = msg.as_string()
    server.sendmail(msg["From"], msg["To"], text)
    server.quit()
