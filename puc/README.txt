
##########################################
1. Criacao de usuario no banco de dados:
##########################################

grant all on monitor to monitor@localhost;
GRANT ALL ON monitor.* TO monitor@'%' IDENTIFIED BY 'monitor';
GRANT ALL ON monitor.* TO monitor@localhost IDENTIFIED BY 'monitor';

##########################################
2. Dump dos dados em json
##########################################

python manage.py dumpdata --indent 2 --exclude=sites --exclude=admin --exclude=sessions --exclude=contenttypes

##############################################
3. Carregar dados iniciais para a aplicacao
##############################################

python manage.py loaddata fixtures/initial_data_json