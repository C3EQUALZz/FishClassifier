from PySide6.QtCore import QObject, QTimer


class ChatController(QObject):
    def __init__(self, view, model, network, my_name):
        super().__init__()
        self.view = view
        self.model = model
        self.network = network
        self.my_name = my_name

        self.view.message_sent.connect(self.handle_send_message)
        self.view.image_sent.connect(self.handle_send_image)

        self.view.update_user_info(network.network_name, network.network_description)

    def handle_send_message(self, message):
        self.view.display_message(message, "user")
        QTimer.singleShot(10, self.view.scroll_to_end)
        QTimer.singleShot(1000, self.send_friend_message)

    def handle_send_image(self, image_path):
        self.view.add_image_message(image_path, "user")
        QTimer.singleShot(10, self.view.scroll_to_end)

        predicted_class = self.model.predict(image_path)
        friend_message = f"The predicted class of the image is: {predicted_class}"
        QTimer.singleShot(1000, lambda: self.view.display_message(friend_message, "friend"))

    def send_friend_message(self):
        friend_message = "Your friend is analyzing the image..."
        self.view.display_message(friend_message, "friend")
        QTimer.singleShot(10, self.view.scroll_to_end)
