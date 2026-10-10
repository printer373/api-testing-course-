# Met2

**Команда 1 (POST /posts):**

```
curl -i -X POST https://jsonplaceholder.typicode.com/posts 
-H "Content-Type: application/json" 
-d '{"title": "Мой пост", "body": "Текст", "userId": 1}'

```

**Вывод:**

```
HTTP/1.1 201 Created
Date: Fri, 09 Oct 2026 03:00:12 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 65
Connection: keep-alive
x-powered-by: Express

{
  "title": "Мой пост",
  "body": "Текст",
  "userId": 1,
  "id": 101
}

```

**Команда 2 (PATCH /users/1):**

```
curl -i -X PATCH https://jsonplaceholder.typicode.com/users/1 
-H "Content-Type: application/json" 
-d '{"name": "Ada"}'

```

**Вывод:**

```
HTTP/1.1 200 OK
Date: Fri, 09 Oct 2026 03:01:47 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
x-powered-by: Express

{
  "id": 1,
  "name": "Ada",
  "username": "Bret",
  "email": "Sincere@april.biz"
}

```

# Met8

**Команда 1 (POST /posts):**

```
curl -i -X POST https://jsonplaceholder.typicode.com/posts 
-H "Content-Type: application/json" 
-d '{"title": "Мой пост", "body": "Текст", "userId": 1}'

```

**Статусная строка:** `HTTP/1.1 201 Created`

**Заголовки ответа:**

* `Content-Type: application/json; charset=utf-8`

* `x-powered-by: Express`

**Вывод целиком:**

```
HTTP/1.1 201 Created
Date: Fri, 09 Oct 2026 03:03:18 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 65
Connection: keep-alive
x-powered-by: Express

{
  "title": "Мой пост",
  "body": "Текст",
  "userId": 1,
  "id": 101
}

```

**Команда 2 (GET /users/3):**

```
curl -i https://jsonplaceholder.typicode.com/users/3

```

**Статусная строка:** `HTTP/1.1 200 OK`

**Заголовки ответа:**

* `Content-Type: application/json; charset=utf-8`

* `Cache-Control: max-age=43200`

**Вывод целиком:**

```
HTTP/1.1 200 OK
Date: Fri, 09 Oct 2026 03:05:02 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
Cache-Control: max-age=43200
x-powered-by: Express

{
  "id": 3,
  "name": "Clementine Bauch",
  "username": "Samantha",
  "email": "Nathan@yesenia.net"
}

```

# Met9

**Команда 1 (С заголовком Accept):**

```
curl -i -H "Accept: application/json" https://jsonplaceholder.typicode.com/users/1

```

**Вывод:**

```
HTTP/1.1 200 OK
Date: Fri, 09 Oct 2026 03:06:41 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
}

```

**Команда 2 (Без заголовка Accept):**

```
curl -i https://jsonplaceholder.typicode.com/users/1

```

**Вывод:**

```
HTTP/1.1 200 OK
Date: Fri, 09 Oct 2026 03:08:15 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
}

```
