@echo off
chcp 65001 >nul

echo Запуск проекта Movie Recommendation System...

:: Проверка доступности Docker
echo Проверка, запущен ли Docker...
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Ошибка: Docker не запущен или не установлен. Пожалуйста, запустите Docker Desktop и попробуйте снова.
    pause
    exit /b 1
)

cd /d "D:\курсач бд"

echo Остановка и удаление существующих контейнеров...
docker-compose down -v

echo Сборка и запуск контейнеров в фоновом режиме...
docker-compose up --build -d
if %ERRORLEVEL% neq 0 (
    echo Ошибка: Не удалось запустить контейнеры. Проверьте логи с помощью "docker-compose logs".
    pause
    exit /b 1
)

echo Ожидание готовности контейнера movie-recommendation-system-console-1...
:waitloop
docker inspect movie-recommendation-system-console-1 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Контейнер ещё не готов, ждём 5 секунд...
    timeout /t 5 /nobreak >nul
    goto waitloop
)

docker inspect --format="{{.State.Running}}" movie-recommendation-system-console-1 | find "true" >nul
if %ERRORLEVEL% neq 0 (
    echo Ошибка: Контейнер movie-recommendation-system-console-1 не запустился. Проверьте логи с помощью "docker-compose logs".
    pause
    exit /b 1
)

echo Проект запущен. Веб-приложение доступно на http://localhost:5000
echo Для использования консольного приложения нажмите любую клавишу...
pause

echo Проверка логов консольного контейнера...
docker-compose logs console

echo Подключение к консольному контейнеру и запуск inter.py с переменной окружения...
docker exec -it -e DOCKER_ENV=true movie-recommendation-system-console-1 /bin/bash -c "python inter.py"
if %ERRORLEVEL% neq 0 (
    echo Ошибка: Не удалось запустить inter.py. Проверьте логи контейнера.
    pause
    exit /b 1
)

echo Консольное приложение завершило работу.
echo Остановка всех контейнеров...
docker-compose down -v

echo Нажмите любую клавишу для выхода...
pause