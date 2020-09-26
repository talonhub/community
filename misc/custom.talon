well well: insert('laravel')
sequel create database <user.text>: insert('mysql -u root -proot -e "create database {text}"')
sequel run: insert('mysql -u root')

node package install: insert('npm install')
node package run development: insert('npm run dev')


# my lovely computer setup
hello computer: key(cmd-space)
short cat: key(cmd-shift-space)

focus email: user.switcher_focus('spark')


# custom lines for laravel demo
new well well <user.text>: insert('laravel new {text}')
composer require well well you eye: insert('composer require laravel/ui')
art you eye view authentication: insert('php artisan ui vue --auth')
composer require backpack: insert('composer require backpack/crud:"4.1.*"')
art backpack install: insert('php artisan backpack:install')
composer require generators: insert('composer require backpack/generators --dev && composer require laracasts/generators --dev && composer require sven/artisan-view --dev ')

art backpack crud <user.text>: insert('art backpack:crud {text}')
art make migration <user.text>:
    insert('art make:migration ')
    insert(user.formatted_text(text, "snake"))
art make controller <user.text>:
    insert('art make:controller ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

art make job <user.text>:
    insert('art make:job ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))

art make mail <user.text>:
    insert('art make:mail ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
    insert(' --markdown=emails.')
    insert(user.formatted_text(text, "DOT_SEPARATED"))
    insert(' && art make:view emails.')
    insert(user.formatted_text(text, "DOT_SEPARATED"))

art make middleware <user.text>:
    insert('art make:middleware ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
art make model <user.text>:
    insert('art make:model ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
art make observer <user.text>:
    insert('art make:observer ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
    insert(' --model=Models\\\\')
    insert(user.formatted_text(text, "FIRST_ONE"))1

art make cedar <user.text>:
    insert('art make:seeder ')
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
    insert('Seeder')
