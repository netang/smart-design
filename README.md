## Установка
`python3 -m pip install -r requirements.txt`

## Запуск
`python3 app.py`

### Создание товара
```curl --location --request POST 'http://0.0.0.0:8080/items' \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Товар 1",
	"description": "Это товар 1",
	"parameters": [
	{
		"key": "key1",
		"value": "value1"
	},
	{
		"key": "key2",
		"value": "value2"
	}]
}'
```

### Поиск товара
```
curl --location --request GET 'http://0.0.0.0:8080/items?parameter[key1]=value1&name=%D0%A2%D0%BE%D0%B2%D0%B0%D1%80%201'
```

### Получение информации о товаре по id
```
curl --location --request GET 'http://0.0.0.0:8080/items/5e9eb144988fc4d6a19d6984'
```