#echo '*.gz'     >  .gitignore
#echo '*komodo*' >> .gitignore

#git init
#git config user.name saulo
#git config user.email sauloal@gmail.com
#git remote add github git@github.com:sauloal/pythonscripts.git
NAME=`date --rfc-3339=seconds | tr " |,|:|\-|\+" _`

git add .
git commit -m "$NAME"
git push -u github master
