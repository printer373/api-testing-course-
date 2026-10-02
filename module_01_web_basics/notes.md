web 3

метод: get
статус: 200
значение заголовка: application/json
тел:10
нет

web 4
 вернулось 5
5:5

web5
да их было 3 
id: 1
id: 2
id:3
web6

5, 5
postEd:id для каждого поста

web7
параметр _limit - создает ограничение объектов в ответе
_limit2 – 2
_limit7 – 7

Web8 

смотреть в urls.md

Web9 
 Вывод: одни и те же данные получены двумя разными дорогами

Web10 
 /users/1 - 200 OK /users/11 - 404 Not Found /users/1?foo=bar - 200 OK Ломает: неверный id в path (/users/11) Не ломает: ?foo=bar

Web11 
 Content-Type: application/json; charset=utf-8 Content-Length: -

Web12 
 /todos?_limit=5&_page=1 - 5 объектов, id первого = 1 /todos?_limit=5&_page=2 - 5 объектов, id первого = 6 Параметр _page задаёт номер страницы

