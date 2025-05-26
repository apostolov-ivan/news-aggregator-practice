@echo off
setlocal

set BASE_URL=http://localhost:8000
set STUDENT_ID=Apostolov_47b86c25

rem Масив URLів RSS-джерел
set RSS_URLS[0]=https://www.bbc.com/ukrainian/rss.xml
set RSS_URLS[1]=https://www.ukrinform.ua/rss
set RSS_URLS[2]=http://feeds.reuters.com/reuters/topNews

rem Додати джерела
for /L %%i in (0,1,2) do (
    echo Додаємо джерело: !RSS_URLS[%%i]!
    curl -X POST %BASE_URL%/sources/%STUDENT_ID% -H "Content-Type: application/json" -d "{\"url\":\"!RSS_URLS[%%i]!\"}"
    echo.
)

rem Запустити завантаження новин
curl -X POST %BASE_URL%/fetch/%STUDENT_ID%

echo Готово!

endlocal
pause
