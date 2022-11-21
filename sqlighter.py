import sqlite3
from unittest import result

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    
    def add_subscriber(self, user_id,refBy, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`,refBy) VALUES(?,?,?)", (user_id,status,refBy))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def check_name(self,user_id):
        """Проверяем  имя подписчика в БД"""
        with self.connection:
            result =  self.cursor.execute("SELECT `name` FROM `subscriptions` WHERE `user_id` = ?", (user_id,))
            return (result)
    def up_Login(self,user_id,LOGIN):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `LOGIN` = ? WHERE `user_id` = ?", (user_id,LOGIN))  

    def add_name(self, user_id,name):
        """Обновляем имя подписчика в БД"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `name` = ? WHERE `user_id` = ?", (name,user_id))

    def get_referals(self,refBy):
        """Выводим рефералов"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `refBy` = ?", (refBy,))

    def update_Vozn(self, user_id,Voznagr):
        """Запоминаем адресс кошелька для вывода"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `Voznagr` = ? WHERE `user_id` = ?", (Voznagr,user_id))

    def add_email(self,user_id,EMAIL):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `EMAIL` = ? WHERE `user_id` = ?", (EMAIL,user_id))

    def add_passw(self,user_id,PASSWORD):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `PASSWORD` = ? WHERE `user_id` = ?", (PASSWORD,user_id))  

    def update_month_sub(self,user_id,PASSWORD):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `MONTH` = ? WHERE `user_id` = ?", (PASSWORD,user_id))    

    def update_year_sub(self,user_id,PASSWORD):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `YEAR` = ? WHERE `user_id` = ?", (PASSWORD,user_id))   

    def update_admin(self,user_id,PASSWORD):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `ADMIN` = ? WHERE `user_id` = ?", (PASSWORD,user_id))    

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


        