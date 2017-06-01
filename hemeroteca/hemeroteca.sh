cd /home/user/github/emijrp.github.io
cd hemeroteca
python3 hemeroteca.py
cd ..
python wiki2html.py --all
git diff hemeroteca/hemeroteca.wiki
git add hemeroteca/hemeroteca.wiki
git add hemeroteca/hemeroteca.html
git commit -m "updating"
#git push https://user:pass@github.com/emijrp/emijrp.github.io.git master
git push
