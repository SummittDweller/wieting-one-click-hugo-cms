# Making /site a Sub-Tree

```
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹empty-site›
╰─$ git checkout -b wieting-site-added
Switched to a new branch 'wieting-site-added'
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-site git@github.com:SummittDweller/wieting-theatre-DO
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-site main
prefix 'site' already exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ rm -fr site                   
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-site main
git fetch wieting-site main
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-site https://github.com/SummittDweller/wieting-theatre-DO   
fatal: remote wieting-site already exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-theatre-DO https://github.com/SummittDweller/wieting-theatre-DO 
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-theatre-DO main
git fetch wieting-theatre-DO main
warning: no common commits
remote: Enumerating objects: 370, done.
remote: Counting objects: 100% (370/370), done.
remote: Compressing objects: 100% (310/310), done.
remote: Total 370 (delta 48), reused 364 (delta 42), pack-reused 0
Receiving objects: 100% (370/370), 19.52 MiB | 13.64 MiB/s, done.
Resolving deltas: 100% (48/48), done.
From https://github.com/SummittDweller/wieting-theatre-DO
 * branch            main       -> FETCH_HEAD
 * [new branch]      main       -> wieting-theatre-DO/main
Added dir 'site'
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
```
