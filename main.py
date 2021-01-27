import vk_api
import DB
import mysql.connector
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime
import random


token = "be40be0d5cc6cb3b6d69237cf06ba9925cf2b83a972075eb7e96e512b15c7181e93d3ff48e9cbbc291786"
vk_session = vk_api.VkApi(token=token)


session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

handle = open("information.txt","r", encoding='utf-8')
data = handle.read()
handle.close()

handle = open("mailing.txt","r", encoding='utf-8')
mailing_data = handle.read()
handle.close()

handle = open("tournament_message.txt","r", encoding='utf-8')
tournament_data = handle.read()
handle.close()
start_time = datetime.now()

arr_id = DB.extract_data()

def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == "возможные действия с ботом":

        keyboard.add_button('Привет', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Новости по турнирам', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Закрыть', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Регистрация на турнир', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button('Подписаться на рассылку', color=VkKeyboardColor.NEGATIVE)

    elif response == "привет":
        keyboard.add_button('Возможные действия с ботом', color=VkKeyboardColor.POSITIVE)
    elif response == "подписаться на рассылку":
        keyboard.add_button('Закрыть', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Возможные действия с ботом', color=VkKeyboardColor.POSITIVE)

    elif response == "новости по турнирам":
        keyboard.add_button('Возможные действия с ботом', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Новости по турнирам', color=VkKeyboardColor.PRIMARY)

    elif response == "регистрация на турнир":
        keyboard.add_button('Закрыть', color=VkKeyboardColor.DEFAULT)

    elif response == "закрыть":
        print("Закрываю клавиатуру")
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard

def send_message(vk_session, id_type, id, message=None,attachment=None,keyboard=None):
    vk_session.method('messages.send', {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), 'attachment': attachment, 'keyboard': keyboard})

#for i in arr_id:
      #try:
         #vk_session.method('messages.send', {'peer_id': i, 'message': mailing_data, 'random_id': random.randint(-2147483648, +2147483648)})
      #except: pass

while True:
        i = 0
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                print("Сообщение пришло в: " + str(datetime.strftime(datetime.now(), "%d/%m/%y")))
                print("Текст сообщения: " + str(event.text))
                print(event.user_id)
                response = event.text.lower()
                keyboard = create_keyboard(response)



                if event.from_user and not (event.from_me):
                    if response == "возможные действия с ботом":
                        send_message(vk_session, 'user_id', event.user_id, message='Вот список моих возможностей: Новости по турнирам; Регистрация на турнир; Подписаться на рассылку:', keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif response == "привет":
                        send_message(vk_session, 'user_id', event.user_id, message='Приветствую вас!', keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif response == "новости по турнирам":
                        send_message(vk_session, 'user_id', event.user_id, message=data, keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif response == "подписаться на рассылку":
                        DB.add_to_id_table(event.user_id)
                        send_message(vk_session, 'user_id', event.user_id, message="Вы успешно подписались на рассылку", keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif response == "регистрация на турнир":
                        i = 1
                        send_message(vk_session, 'user_id', event.user_id, message='Введите ФИО капитана:',keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif response == "закрыть":
                        send_message(vk_session, 'user_id', event.user_id, message='Закрываюсь', keyboard=keyboard)
                        print(datetime.now() - start_time)
                    elif i == 1:
                        captain = str(event.text)
                        i = 2
                        send_message(vk_session, 'user_id', event.user_id, message='Введите название команды:')
                        print(datetime.now() - start_time)
                    elif i == 2:
                        team = str(event.text)
                        i = 0
                        DB.add_to_table("teams_new", event.user_id, captain, team)
                        if DB.seat_check("teams_new") == True:
                            arr_teams_info = []
                            arr_teams_info = DB.return_data_from_database_by_id("teams_new", event.user_id)
                            message_teams0 = str(arr_teams_info[0])
                            message_teams1 = str(arr_teams_info[1])
                            message_teams = message_teams0 + ", " + message_teams1
                            send_message(vk_session, 'user_id', event.user_id, message=tournament_data)
                            send_message(vk_session, 'user_id', event.user_id, message=message_teams)
                            send_message(vk_session, 'user_id', event.user_id, message='Регистрация прошла успешно')
                        else:
                            send_message(vk_session, 'user_id', event.user_id,
                                         message='Приносим свои извинения, все места на турнир заняты. Вы будете внесены в лист ожидания и сможете принять участие, если какая-то из команд не подтвердит участие в турнире')
                    else:
                        send_message(vk_session, 'user_id', event.user_id, message='Действие не распознано. Пожалуйста, дождитесь ответа администратора или выберите одну из существующих команд: Новости по турнирам; Регистрация на турнир; Подписаться на рассылку')
                        print(datetime.now() - start_time)



