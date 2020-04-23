Скрипт для мониторинга УТМ от ФСРАР

Мониторинг для Zabbix.
Скрипт извлекает следующие данные из универсального транспортного модуля (ФСРАР)
 - Получает данные о текущей версии УТМ
 - Сколько осталось дней до окончания сертификатов (RSA и ГОСТ)
 - Проверяет, нет ли ошибок чтения RSA сертификата
 - Проверят возраст не отправленных розничных документов

Скрипт на входе ожидает два параметра 
1- тип запрашиваемого параметра
 - version (Получить версию УТМ)
 - rsavalid (Статус RSA)
 - rsadate (осталось дней до окончания сертификата RSA)
 - gostdate (осталось дней до окончания сертификата ГОСТ)
 - docsbuffer (возвраст в часах первого не переданного чека)
2- адрес УТМ
Если второй параметр не будет передан, будет использован http://localhost:8080

Поддержка версии УТМ 3.
