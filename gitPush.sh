#echo '*.gz'     >  .gitignore
#echo '*komodo*' >> .gitignore

#git init
#git config user.name saulo
#git config user.email sauloal@gmail.com
#git remote add github git@github.com:sauloal/pythonscripts.git
NAME=`date --rfc-3339=seconds | tr " |,|:|\-|\+" _`

git add .

if [[ ! -z $(git ls-files --deleted) ]]; then
    git rm $(git ls-files --deleted)  2>&1 | tee -a $LOG
fi

git commit -m "$NAME"
git push -u github master:pypeline
