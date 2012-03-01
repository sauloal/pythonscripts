#echo '*.gz'     >  .gitignore
#echo '*komodo*' >> .gitignore

#git init
#git config user.name saulo
#git config user.email sauloal@gmail.com
#git remote add github git@github.com:sauloal/pythonscripts.git

git add .
git commit -m `date`
git push -u github master
