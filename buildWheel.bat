
@echo off

py setup.py sdist bdist_wheel

rem echo Y | rmdir build /s
rem echo Y | rmdir MODULE.egg-info /s

echo,
echo,

set /p install="顺便安装Wheel？任意字符+回车确认，直接回车则取消"
if defined install (
	cd dist
	for /f "delims=" %%i in ('dir /b') do ( 
		if "%%~xi"==".whl" (
			echo,
			echo,
			pip install --force-reinstall %%i
			echo,
			echo,
		)
	)
	cd ..
)



echo 操作结束 & pause 


