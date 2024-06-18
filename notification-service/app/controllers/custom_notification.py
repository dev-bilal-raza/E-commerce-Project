from app.utils.boto_config import send_email_via_boto


def send_custom_notification_func(user_email: str, subject: str, message: str):
    custom_notification_schema = f"""
    <html>
    <head>
    </head>
    <body>
        <main
            style="height: 100%; padding: 2em; margin: 1em; background-color: rgb(243, 243, 243); display: flex; justify-content: center; align-items: center;">
            <div style="width: 100%;">
                <div style="height: 0.4px; width: 100%; margin-bottom: 10px; background-color: darkgray;">
                </div>
                <div style="display: flex; flex-direction: column; align-items: center; background: rgb(203,192,71); background: linear-gradient(to top, rgb(5, 35, 59)0%,rgb(30, 81, 122)60%,
                    rgb(161, 178, 182) 100%); ">
                    <header style="display: flex; justify-content: center;">
                        <img src="" alt="" srcset="">
                        <h2>
                            E-commerce
                        </h2>
                    </header>
                    <div style="width: 70%; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <p
                            style="text-align: center; color: rgb(142, 169, 173); font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif; font-size: large; letter-spacing: 1px;">
                        {message}
                        </p>
                        <button style="margin: 10px; padding: 10px; border-radius: 15%; background-color: rgb(0, 0, 0);"><a
                                href="https://www.yourwebsite.com" style="text-decoration: none; color: white;">Go to Website</a></button>
                    </div>
                    <div style="height: 0.4px; background-color: #8BA2AC; width: 80%; margin: 5px;"></div>
                    <footer>
                        <p style="color: rgb(142, 169, 173);">
                            © copyright 2024 - 2026
                        </p>
                    </footer>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    response = send_email_via_boto(user_email, subject, custom_notification_schema)
    return response