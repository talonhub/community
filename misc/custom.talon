well well: insert('laravel')
sequel create database <user.text>: insert('mysql -u root -proot -e "create database {text}"')
sequel run: insert('mysql -u root')

node package install: insert('npm install')
node package run development: insert('npm run dev')

art backpack crud <user.text>: insert('php artisan backpack:crud {text}')

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
composer require generators: insert('composer require backpack/generators --dev && composer require laracasts/generators --dev')
my backpack example: insert('php artisan make:migration:schema create_tags_table --model=0 --schema="name:string:unique" && php artisan migrate')


