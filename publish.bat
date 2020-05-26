REM 声明采用UTF-8编码
chcp 65001

rd output\水质探头测试\lib /s /q
del output\水质探头测试\*.jar
del output\水质探头测试\*.db

copy ..\wqa_windows_from\dist\*.jar output\水质探头测试\

copy ..\wqa_windows_from\dev_config output\水质探头测试\

xcopy ..\wqa_windows_from\dist\lib output\水质探头测试\lib\ /s /d /a


@echo off
for /f tokens^=2^,3^ delims^=^>^<^" %%a in (.\output\水质探头测试\dev_config) do (
	if %%a == VER set version=%%b
)
@echo on
echo %version%

"C:\Program Files\7-Zip\7z.exe" a "output\水质探头测试标准.%version%.7z" "output\水质探头测试\" 

pause
 