del /S /F /Q release
del /S /F /Q out
python dvertkeygen.py --generateexe --compressexe
mkdir release
cd out
tar.exe -cvzf ..\release\dvertkey.zip *.*
cd ..
