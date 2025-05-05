@echo off
chcp 65001 >nul

echo Запуск проекта Movie Recommendation System...

cd /d "D:\курсач бд"

echo Остановка и удаление существующих контейнеров...
docker-compose down -v

echo Сборка и запуск контейнеров в фоновом режиме...
docker-compose up --build -d

echo Проект запущен. Веб-приложение доступно на http://localhost:5000
echo Для использования консольного приложения нажмите любую клавишу...
pause

echo Проверка логов консольного контейнера...
docker-compose logs console

echo Подключение к консольному контейнеру и запуск inter.py с переменной окружения...
docker exec -it -e DOCKER_ENV=true movie-recommendation-system-console-1 /bin/bash -c "python inter.py"

echo Консольное приложение завершило работу.
echo Остановка всех контейнеров...
docker-compose down -v

echo Нажмите любую клавишу для выхода...
pause