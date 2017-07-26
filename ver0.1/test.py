import fbchat


class Bot(Client):
    Black_List = []
    with open("./Meal_List/Meal_List.txt", "rb") as f:
        Meal = pickle.load(f)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        def send(self, message):
            self.sendMessage(message, thread_id=thread_id, thread_type=thread_type)

        # send('', thread_id=thread_id, thread_type=thread_type)
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
